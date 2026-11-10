"""Regression checks for preprocessing, artifact integrity and both inference routes.

The small synthetic fixture checks mechanics, not Fashion-MNIST model quality.
The documented CPU rehearsal uses the verified research dataset separately.
"""

import csv
from pathlib import Path

from fastapi.testclient import TestClient
import numpy as np
from PIL import Image
import pytest
import torch

from src.artifacts import bytes_digest, read_json
from src.evaluation import score_predictions
from src.inference import Predictor, predict_batch
from src.model import TrainingConfig
from src.preprocessing import preprocess, validate_images
from src.service import create_app
from src.training import train, verify_run


@pytest.fixture
def run(tmp_path, monkeypatch):
    from src import training
    rng = np.random.default_rng(22)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.tile(np.arange(10, dtype=np.uint8), 4)
    manifest = {"name": "synthetic-mechanics-fixture", "split_sha256": "test-split",
                "partitions": {"train": list(range(20)), "validation": list(range(20, 40))}}
    monkeypatch.setattr(training, "verify_data", lambda _: manifest)
    monkeypatch.setattr(training, "load_arrays", lambda _: (images, labels))
    output = tmp_path / "run"
    train(tmp_path / "data", output, TrainingConfig(epochs=1, cpu_threads=1))
    return output, images


def test_preprocessing_preserves_source_and_scales_once():
    raw = np.zeros((2, 28, 28), dtype=np.uint8)
    raw[0, 0, 0] = 255
    raw[1, -1, -1] = 200
    original = raw.copy()
    result = preprocess(raw)
    assert result.shape == (2, 1, 28, 28)
    assert result.dtype == torch.float32
    assert result[0, 0, 0, 0] == 1
    assert torch.isfinite(result).all()
    assert np.array_equal(raw, original)
    result.zero_()
    assert raw[0, 0, 0] == 255
    with pytest.raises(ValueError, match="uint8"):
        preprocess(original.astype(np.float32) / 255)


@pytest.mark.parametrize("raw", [np.zeros((0, 28, 28), dtype=np.uint8),
                                 np.zeros((1, 28, 28, 3), dtype=np.uint8),
                                 np.zeros((1, 32, 32), dtype=np.uint8)])
def test_input_shape_failures_are_explicit(raw):
    with pytest.raises(ValueError, match="shape"):
        validate_images(raw)


def test_raw_predictions_define_metrics():
    truth = np.arange(10)
    predicted = truth.copy()
    predicted[0] = 1
    report = score_predictions(truth, predicted)
    assert report["accuracy"] == 0.9
    assert report["confusion_matrix"][0][1] == 1
    assert report["per_class"]["T-shirt/top"]["recall"] == 0
    assert report["per_class"]["Trouser"]["precision"] == 0.5


def test_batch_and_http_share_saved_model_and_normalization(run, tmp_path):
    run_dir, images = run
    intake = tmp_path / "intake"
    intake.mkdir()
    Image.fromarray(images[0]).save(intake / "first.png")
    Image.fromarray(images[1]).save(intake / "second.png")
    manifest = intake / "manifest.csv"
    manifest.write_text("image_id,path\nitem-B,first.png\nitem-A,second.png\n")
    output = tmp_path / "batch"
    batch = predict_batch(run_dir, manifest, output)
    with (output / "predictions.csv").open() as stream:
        predictions = list(csv.DictReader(stream))
    assert [row["image_id"] for row in predictions] == ["item-B", "item-A"]
    with TestClient(create_app(run_dir)) as client:
        response = client.post("/predict", json={"image_id": "item-B", "pixels": images[0].tolist()})
        assert response.status_code == 200
        actual = response.json()
        assert actual["prediction"]["class_id"] == int(predictions[0]["class_id"])
        assert actual["prediction"]["top_score"] == pytest.approx(float(predictions[0]["top_score"]), abs=1e-6)
        assert actual["model"] == batch["model"]
        assert client.get("/health").json()["model"] == batch["model"]


def test_http_rejects_pixels_before_uint8_cast(run):
    run_dir, images = run
    invalid = images[0].astype(int).tolist()
    invalid[0][0] = 256
    floating = images[0].astype(float).tolist()
    with TestClient(create_app(run_dir)) as client:
        for pixels in (invalid, floating, [[0]], []):
            assert client.post("/predict", json={"image_id": "bad", "pixels": pixels}).status_code == 422


def test_duplicate_identifiers_and_failed_batch_do_not_publish_partial_output(run, tmp_path):
    run_dir, images = run
    predictor = Predictor(run_dir)
    with pytest.raises(ValueError, match="distinct"):
        predictor.predict(images[:2], ["duplicate", "duplicate"])
    manifest = tmp_path / "bad.csv"
    manifest.write_text("image_id,path\nmissing,not-there.png\n")
    output = tmp_path / "failed-batch"
    with pytest.raises(FileNotFoundError):
        predict_batch(run_dir, manifest, output)
    assert not output.exists()


def test_changed_model_bytes_cannot_be_silently_loaded(run):
    run_dir, _ = run
    assert verify_run(run_dir)["checkpoint_reload_exact"]
    with (run_dir / "model.pt").open("ab") as stream:
        stream.write(b"changed")
    with pytest.raises(ValueError, match="checksum"):
        Predictor(run_dir)


def test_existing_run_is_preserved_on_retry(run):
    run_dir, _ = run
    original = read_json(run_dir / "run.json")
    with pytest.raises(FileExistsError, match="already exists"):
        train(Path("unused"), run_dir, TrainingConfig())
    assert read_json(run_dir / "run.json") == original


def test_predictions_distinguish_training_code_from_current_inference_code(run, monkeypatch):
    from src import inference
    run_dir, _ = run
    monkeypatch.setattr(inference, "runtime_source_sha256", lambda: "current-inference-code")
    identity = Predictor(run_dir).identity
    assert identity["inference_source_sha256"] == "current-inference-code"
    assert identity["training_source_sha256"] == read_json(run_dir / "run.json")["source"]["source_sha256"]


def test_batch_hashes_consumed_bytes_when_supplier_changes_files(run, tmp_path, monkeypatch):
    from src import inference
    run_dir, images = run
    image_path = tmp_path / "thumbnail.png"
    Image.fromarray(images[0]).save(image_path)
    original_image = image_path.read_bytes()
    manifest = tmp_path / "manifest.csv"
    manifest.write_text("image_id,path\nfirst,thumbnail.png\n")
    original_manifest = manifest.read_bytes()
    original_decoder = inference.decode_thumbnail
    original_reader = inference.read_batch_manifest

    def decode_and_change_supplier(content, name):
        decoded = original_decoder(content, name)
        Image.fromarray(255 - images[0]).save(image_path)
        return decoded

    def read_and_change_manifest(path, content=None):
        rows = original_reader(path, content)
        path.write_text("image_id,path\nchanged,other.png\n")
        return rows

    monkeypatch.setattr(inference, "decode_thumbnail", decode_and_change_supplier)
    monkeypatch.setattr(inference, "read_batch_manifest", read_and_change_manifest)
    report = predict_batch(run_dir, manifest, tmp_path / "batch")
    assert report["inputs"][0] == {"image_id": "first", "sha256": bytes_digest(original_image)}
    assert report["manifest_sha256"] == bytes_digest(original_manifest)
    assert bytes_digest(image_path.read_bytes()) != report["inputs"][0]["sha256"]


def test_history_corruption_is_detected(run):
    run_dir, _ = run
    with (run_dir / "history.json").open("a") as stream:
        stream.write(" ")
    with pytest.raises(ValueError, match="history.json"):
        verify_run(run_dir)


def test_failed_sample_export_can_be_retried(run, tmp_path, monkeypatch):
    from src import inference
    _, images = run
    monkeypatch.setattr(inference, "verify_data", lambda _: {"partitions": {"current": list(range(20))}})
    monkeypatch.setattr(inference, "load_arrays", lambda _: (images, np.zeros(40)))
    original_save = Image.Image.save

    def failed_save(*args, **kwargs):
        raise OSError("simulated storage interruption")

    monkeypatch.setattr(Image.Image, "save", failed_save)
    output = tmp_path / "export"
    with pytest.raises(OSError, match="storage interruption"):
        inference.export_samples(tmp_path, "current", 2, output)
    assert not output.exists()
    monkeypatch.setattr(Image.Image, "save", original_save)
    assert inference.export_samples(tmp_path, "current", 2, output)["count"] == 2
