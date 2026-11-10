"""Verify model identity through a reload of fitted tree state."""

import joblib
import numpy as np
import pandas as pd
from PIL import Image
import pytest

from src import inference, sklearn_model
from src.preprocessing import validate_images
from src.sklearn_model import build_model
from src.training import model_state_sha256, train


def test_random_forest_identity_tracks_predictions_across_reload(tmp_path):
    rng = np.random.default_rng(426)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.arange(len(images)) % 2
    model = build_model({
        "estimator": "random_forest",
        "params": {"n_estimators": 3, "max_depth": 3},
        "seed": 426,
    }).fit(images, labels)
    path = tmp_path / "model.joblib"
    joblib.dump(model, path)
    restored = joblib.load(path)

    assert model_state_sha256(restored) == model_state_sha256(model)
    np.testing.assert_array_equal(restored.predict_proba(images), model.predict_proba(images))
    restored[-1].estimators_[0].tree_.value[0, 0, 0] += 1
    assert model_state_sha256(restored) != model_state_sha256(model)


def test_batch_report_keeps_predictions_and_input_errors_in_manifest_order(tmp_path, monkeypatch):
    rng = np.random.default_rng(426)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.tile(np.arange(10), 4)
    split = {"split_sha256": "test", "partitions": {"train": list(range(20)), "validation": list(range(20, 40))}}
    monkeypatch.setattr(sklearn_model, "verify_data", lambda _: split)
    monkeypatch.setattr(sklearn_model, "load_arrays", lambda _: (images, labels))
    run = tmp_path / "run"
    train(tmp_path, run, {"estimator": "random_forest", "params": {"n_estimators": 3}, "seed": 426})

    def validate_contrast(batch):
        batch = validate_images(batch)
        if (np.ptp(batch, axis=(1, 2)) < 20).any():
            raise ValueError("Insufficient contrast")
        return batch

    monkeypatch.setattr(inference, "validate_intake", validate_contrast)
    Image.fromarray(images[0]).save(tmp_path / "valid.png")
    Image.fromarray(np.zeros((28, 28), dtype=np.uint8)).save(tmp_path / "flat.png")
    (tmp_path / "corrupt.png").write_text("not an image")
    manifest = tmp_path / "manifest.csv"
    manifest.write_text("image_id,path\n001,valid.png\nflat,flat.png\nmissing,absent.png\ncorrupt,corrupt.png\nNA,valid.png\n")

    output = tmp_path / "report"
    receipt = inference.predict_batch(run, manifest, output, report_errors=True)
    results = pd.read_csv(output / "results.csv", dtype={"image_id": "string"}, keep_default_na=False)
    assert results["image_id"].tolist() == ["001", "flat", "missing", "corrupt", "NA"]
    assert results["path"].tolist() == ["valid.png", "flat.png", "absent.png", "corrupt.png", "valid.png"]
    assert results["has_error"].tolist() == [False, True, True, True, False]
    assert results["prediction"].ne("").tolist() == [True, False, False, False, True]
    assert results.loc[results["has_error"], "error"].str.len().gt(0).all()
    assert results.loc[1, "error"] == "Insufficient contrast"
    assert (receipt["count"], receipt["prediction_count"], receipt["error_count"]) == (5, 2, 3)

    def broken_model(*_):
        raise ValueError("Invalid model state")

    monkeypatch.setattr(inference, "classify", broken_model)
    rejected_manifest = tmp_path / "rejected.csv"
    rejected_manifest.write_text("image_id,path\nflat,flat.png\nmissing,absent.png\n")
    rejected = inference.predict_batch(run, rejected_manifest, tmp_path / "rejected", report_errors=True)
    assert (rejected["count"], rejected["prediction_count"], rejected["error_count"]) == (2, 0, 2)

    failed_output = tmp_path / "failed"
    with pytest.raises(ValueError, match="Invalid model state"):
        inference.predict_batch(run, manifest, failed_output, report_errors=True)
    assert not failed_output.exists()
