"""Distinguish known quality changes from distribution signals using consumed inputs."""

import csv
from pathlib import Path

import numpy as np
from PIL import Image
import pytest

from catalog_mlops.artifacts import bytes_digest
from catalog_mlops.data import CLASS_NAMES
from catalog_mlops.inference import deliver_batch
from catalog_mlops.monitoring import (
    compare_cohorts,
    compare_model_quality,
    observe_delivery,
)


class FixedPredictions:
    def __init__(self, shift=0):
        self.shift = shift
        self.identity = {
            "model_sha256": f"weights-{shift}",
            "training_source_sha256": "training",
            "inference_source_sha256": "preparation",
        }

    def predict(self, images, ids):
        return [
            {
                "image_id": identity,
                "class_id": (int(identity) + self.shift) % 10,
                "class_name": CLASS_NAMES[(int(identity) + self.shift) % 10],
                "top_score": 0.9,
            }
            for identity in ids
        ]


def intake(root: Path, brightness: float = 1):
    root.mkdir()
    with (
        (root / "manifest.csv").open("w", newline="") as stream,
        (root / "labels.csv").open("w", newline="") as label_stream,
    ):
        writer = csv.writer(stream)
        writer.writerow(["image_id", "path"])
        labels = csv.writer(label_stream)
        labels.writerow(["image_id", "label"])
        for index in range(10):
            values = np.full((28, 28), 130 + index * 2, dtype=np.uint8)
            values[0, 0] = 0
            values[-1, -1] = 255
            values = np.rint(values * brightness).astype(np.uint8)
            Image.fromarray(values).save(root / f"{index}.png")
            writer.writerow([str(index), f"{index}.png"])
            labels.writerow([str(index), index])
    return root / "manifest.csv"


def test_drift_has_no_accuracy_without_labels_and_requires_fixed_model(tmp_path):
    first = intake(tmp_path / "reference")
    shifted = intake(tmp_path / "current", 0.45)
    delivery = deliver_batch(FixedPredictions(), first, tmp_path / "batch-reference")
    deliver_batch(FixedPredictions(), shifted, tmp_path / "batch-current")
    reference = observe_delivery(tmp_path / "batch-reference")
    current = observe_delivery(tmp_path / "batch-current")
    report = compare_cohorts(reference, current)
    assert report["brightness_total_variation"] == 1
    assert report["brightness_alert"] and not report["quality_comparison_available"]
    assert (
        "quality" not in current
        and "quality_alert" not in report
        and "macro_f1_drop" not in report
    )
    assert report["predicted_category_total_variation"] == 0
    labeled = observe_delivery(
        tmp_path / "batch-current", tmp_path / "current/labels.csv"
    )
    assert labeled["quality"]["macro_f1"] == 1
    deliver_batch(FixedPredictions(1), first, tmp_path / "other-model")
    other = observe_delivery(
        tmp_path / "other-model", tmp_path / "reference/labels.csv"
    )
    with pytest.raises(ValueError, match="same model"):
        compare_cohorts(reference, other)
    assert len(delivery["image_observations"]) == 10
    assert sum(current["mean_brightness_counts"]) == 10


def test_paired_model_quality_needs_same_consumed_bytes_and_labels(tmp_path):
    manifest = intake(tmp_path / "images")
    deliver_batch(FixedPredictions(), manifest, tmp_path / "first")
    deliver_batch(FixedPredictions(1), manifest, tmp_path / "second")
    first = observe_delivery(tmp_path / "first", tmp_path / "images/labels.csv")
    second = observe_delivery(tmp_path / "second", tmp_path / "images/labels.csv")
    report = compare_model_quality(first, second)
    assert report["macro_f1_change"] == -1 and report["quality_regression_alert"]
    shifted = intake(tmp_path / "shifted", 0.45)
    deliver_batch(FixedPredictions(1), shifted, tmp_path / "different-inputs")
    changed = observe_delivery(
        tmp_path / "different-inputs", tmp_path / "shifted/labels.csv"
    )
    with pytest.raises(ValueError, match="identical input bytes"):
        compare_model_quality(first, changed)
    with pytest.raises(ValueError, match="known labels"):
        compare_model_quality(first, observe_delivery(tmp_path / "second"))
    (tmp_path / "images/labels.csv").write_text("image_id,label\nmissing,0\n")
    with pytest.raises(ValueError, match="exactly the delivered"):
        observe_delivery(tmp_path / "first", tmp_path / "images/labels.csv")
    second["mean_brightness_counts"][0] += 1
    with pytest.raises(ValueError, match="Observation changed"):
        compare_model_quality(first, second)


def test_monitoring_describes_consumed_image_even_if_file_changes(tmp_path):
    manifest = intake(tmp_path / "images")
    image = tmp_path / "images/0.png"
    original = image.read_bytes()
    original_mean = np.asarray(Image.open(image)).mean() / 255
    predictor = FixedPredictions()
    predict = predictor.predict

    def replace_after_consumption(images, ids):
        Image.fromarray(np.full((28, 28), 30, dtype=np.uint8)).save(image)
        return predict(images, ids)

    predictor.predict = replace_after_consumption
    delivery = deliver_batch(predictor, manifest, tmp_path / "batch")
    observed = observe_delivery(tmp_path / "batch")
    assert observed["inputs"][0]["sha256"] == bytes_digest(original)
    assert bytes_digest(image.read_bytes()) != observed["inputs"][0]["sha256"]
    assert delivery["image_observations"][0]["mean_brightness"] == original_mean
    (tmp_path / "batch/predictions.csv").write_text("changed")
    with pytest.raises(ValueError, match="predictions changed"):
        observe_delivery(tmp_path / "batch")


@pytest.mark.parametrize("target", ["predictions.csv", "batch.json"])
def test_published_files_are_hashed_and_parsed_from_one_consumed_snapshot(
    tmp_path, monkeypatch, target
):
    import io
    import json

    manifest = intake(tmp_path / "images")
    directory = tmp_path / "batch"
    deliver_batch(FixedPredictions(), manifest, directory)
    target_path = directory / target
    original = target_path.read_bytes()
    if target == "predictions.csv":
        rows = list(csv.DictReader(io.StringIO(original.decode())))
        for row in rows:
            row["class_id"] = str((int(row["class_id"]) + 1) % 10)
            row["class_name"] = CLASS_NAMES[int(row["class_id"])]
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        replacement = stream.getvalue().encode()
    else:
        batch = json.loads(original)
        batch["image_observations"][0]["mean_brightness"] = 0.99
        replacement = json.dumps(batch).encode()
    open_file = Path.open
    replaced = False

    def replace_after_open(path, mode="r", *args, **kwargs):
        nonlocal replaced
        handle = open_file(path, mode, *args, **kwargs)
        if path == target_path and mode in ("r", "rb") and not replaced:
            replaced = True
            temporary = directory / "replacement.tmp"
            temporary.write_bytes(replacement)
            temporary.replace(target_path)
        return handle

    monkeypatch.setattr(Path, "open", replace_after_open)
    observation = observe_delivery(directory, tmp_path / "images/labels.csv")
    assert replaced and target_path.read_bytes() == replacement
    assert observation["quality"]["macro_f1"] == 1
    field = "predictions_sha256" if target == "predictions.csv" else "batch_sha256"
    assert observation[field] == bytes_digest(original)
