"""Describe delivered images and distinguish drift signals from labeled quality."""

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from catalog_mlops.artifacts import bytes_digest, json_digest
from catalog_mlops.data import CLASS_NAMES
from catalog_mlops.evaluation import score_predictions

# Declared exercise investigation thresholds, not universal statistical cutoffs.
MONITOR_POLICY = {
    "name": "catalog-cohort-v1",
    "mean_brightness_bin_edges": np.linspace(0, 1, 11).tolist(),
    "brightness_total_variation_alert": 0.20,
    "macro_f1_drop_alert": 0.05,
}


def observe_delivery(directory: Path, labels_path: Path | None = None) -> dict:
    """Use the pixels and predictions consumed by a complete batch, not a later reread."""
    batch_content = (directory / "batch.json").read_bytes()
    batch = json.loads(batch_content)
    prediction_content = (directory / "predictions.csv").read_bytes()
    if bytes_digest(prediction_content) != batch["predictions_sha256"]:
        raise ValueError("Batch predictions changed after publication")
    with io.StringIO(prediction_content.decode("utf-8"), newline="") as stream:
        predictions = list(csv.DictReader(stream))
    ids = [row["image_id"] for row in predictions]
    if (
        not ids
        or len(set(ids)) != len(ids)
        or len(ids) != batch["count"]
        or ids != [row["image_id"] for row in batch["inputs"]]
        or ids != [row["image_id"] for row in batch["image_observations"]]
    ):
        raise ValueError("Batch observation and prediction identities differ")
    means = np.array([row["mean_brightness"] for row in batch["image_observations"]])
    if not np.isfinite(means).all() or (means < 0).any() or (means > 1).any():
        raise ValueError("Mean image brightness must be finite on the 0–1 scale")
    predicted = np.array([int(row["class_id"]) for row in predictions])
    if (predicted < 0).any() or (predicted >= 10).any():
        raise ValueError("Unknown predicted category")
    if any(
        row["class_name"] != CLASS_NAMES[int(row["class_id"])] for row in predictions
    ):
        raise ValueError("Prediction names differ from the declared category order")
    counts, _ = np.histogram(means, bins=MONITOR_POLICY["mean_brightness_bin_edges"])
    result = {
        "schema": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "count": len(ids),
        "model": batch["model"],
        "policy": MONITOR_POLICY,
        "batch_sha256": bytes_digest(batch_content),
        "predictions_sha256": batch["predictions_sha256"],
        "inputs": batch["inputs"],
        "mean_brightness_counts": counts.tolist(),
        "predicted_category_counts": np.bincount(predicted, minlength=10).tolist(),
        "quality_available": labels_path is not None,
    }
    if labels_path is not None:
        content = labels_path.read_bytes()
        with io.StringIO(content.decode("utf-8"), newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ["image_id", "label"]:
                raise ValueError("Labels must have exactly image_id,label columns")
            label_rows = list(reader)
        if any(None in row or None in row.values() for row in label_rows):
            raise ValueError("Incomplete label row")
        label_ids = [row["image_id"] for row in label_rows]
        if len(set(label_ids)) != len(label_ids) or set(label_ids) != set(ids):
            raise ValueError("Labels must cover exactly the delivered image identities")
        labels = {row["image_id"]: int(row["label"]) for row in label_rows}
        truth = np.array([labels[image_id] for image_id in ids])
        if (truth < 0).any() or (truth >= 10).any():
            raise ValueError("Unknown known category")
        result["quality"] = score_predictions(truth, predicted)
        result["labels_sha256"] = bytes_digest(content)
        result["label_identities"] = [[image_id, labels[image_id]] for image_id in ids]
    result["observation_sha256"] = json_digest(result)
    return result


def verify_observation(report: dict) -> None:
    payload = {
        key: value for key, value in report.items() if key != "observation_sha256"
    }
    if (
        report.get("observation_sha256") != json_digest(payload)
        or report["policy"] != MONITOR_POLICY
    ):
        raise ValueError("Observation changed or uses another monitoring policy")
    if not isinstance(report["count"], int) or report["count"] <= 0:
        raise ValueError("An observed cohort must contain at least one image")
    for field in ("mean_brightness_counts", "predicted_category_counts"):
        counts = np.asarray(report[field])
        if (
            counts.shape != (10,)
            or (counts < 0).any()
            or not np.equal(counts, counts.astype(int)).all()
            or counts.sum() != report["count"]
        ):
            raise ValueError("Observation counts do not cover the cohort")


def total_variation(first: list[int], second: list[int]) -> float:
    a, b = np.asarray(first, dtype=float), np.asarray(second, dtype=float)
    return float(np.abs(a / a.sum() - b / b.sum()).sum() / 2)


def compare_cohorts(reference: dict, current: dict) -> dict:
    for report in (reference, current):
        verify_observation(report)
    for key in ("model_sha256", "training_source_sha256", "inference_source_sha256"):
        if reference["model"][key] != current["model"][key]:
            raise ValueError(
                "Cohort drift comparison requires the same model and preparation code"
            )
    brightness_tv = total_variation(
        reference["mean_brightness_counts"], current["mean_brightness_counts"]
    )
    result = {
        "policy": MONITOR_POLICY,
        "reference_sha256": reference["observation_sha256"],
        "current_sha256": current["observation_sha256"],
        "brightness_total_variation": brightness_tv,
        "brightness_alert": brightness_tv
        >= MONITOR_POLICY["brightness_total_variation_alert"],
        "predicted_category_total_variation": total_variation(
            reference["predicted_category_counts"], current["predicted_category_counts"]
        ),
        "quality_comparison_available": reference["quality_available"]
        and current["quality_available"],
        "interpretation": "Distribution differences are investigation signals; unlabeled data does not measure correctness.",
    }
    if result["quality_comparison_available"]:
        drop = reference["quality"]["macro_f1"] - current["quality"]["macro_f1"]
        result.update(
            macro_f1_drop=drop,
            quality_alert=drop >= MONITOR_POLICY["macro_f1_drop_alert"],
        )
    return result


def compare_model_quality(first: dict, second: dict) -> dict:
    """Compare models on identical consumed images and known labels."""
    for report in (first, second):
        verify_observation(report)
        if not report["quality_available"]:
            raise ValueError("Comparing model quality requires known labels")
    if (
        first["inputs"] != second["inputs"]
        or first["label_identities"] != second["label_identities"]
    ):
        raise ValueError(
            "A model-quality comparison requires identical input bytes, order and labels"
        )
    if (
        first["model"]["inference_source_sha256"]
        != second["model"]["inference_source_sha256"]
    ):
        raise ValueError(
            "Keep preparation and inference code fixed when attributing a model change"
        )
    delta = second["quality"]["macro_f1"] - first["quality"]["macro_f1"]
    return {
        "policy": MONITOR_POLICY,
        "first_sha256": first["observation_sha256"],
        "second_sha256": second["observation_sha256"],
        "macro_f1_change": delta,
        "quality_regression_alert": delta <= -MONITOR_POLICY["macro_f1_drop_alert"],
        "first_model": first["model"],
        "second_model": second["model"],
        "interpretation": "Paired quality observations on the same supplied images and labels; no universal performance claim.",
    }
