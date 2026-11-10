"""Verify a tracked run against its saved evaluation and logged model."""

import csv
from pathlib import Path
import re

from mlflow import MlflowClient
import numpy as np

from src.artifacts import read_json
from src.evaluation import score_predictions
from src.tracking import download_recipe, verify_history, verify_logged_model
from src.training import verify_run


def inspect_tracked_run(client: MlflowClient, run_id: str, destination: Path) -> dict:
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        raise ValueError("Use a full 32-character MLflow run ID")
    observed = client.get_run(run_id)
    tags = observed.data.tags
    if observed.info.status != "FINISHED" or tags.get("pipeline_status") != "complete":
        raise ValueError("Run has not completed both learning and verified model logging")

    directory = download_recipe(client, run_id, destination / run_id)
    record = verify_run(directory)
    dataset = read_json(directory / "dataset.json")
    metrics = read_json(directory / "metrics.json")
    with (directory / "validation-predictions.csv").open(newline="", encoding="utf-8") as stream:
        predictions = list(csv.DictReader(stream))
    expected_ids = [f"train:{image_id}" for image_id in dataset["partitions"]["validation"]]
    if [row["image_id"] for row in predictions] != expected_ids:
        raise ValueError("Prediction identities do not match the declared validation order")
    if len(predictions) != record["validation_count"] or dataset["split_sha256"] != record["split_sha256"]:
        raise ValueError("Validation count or split identity differs within the retained recipe")

    raw = score_predictions(np.array([int(row["label"]) for row in predictions]),
                            np.array([int(row["prediction"]) for row in predictions]))
    if raw["confusion_matrix"] != metrics["confusion_matrix"]:
        raise ValueError("Retained metrics do not match the raw validation predictions")
    for field in ("macro_f1", "accuracy"):
        key = f"validation_{field}"
        values = [metrics[field], record[key], observed.data.metrics.get(key, float("inf"))]
        if not np.isfinite(values).all() or not np.allclose(values, raw[field], rtol=0, atol=1e-12):
            raise ValueError(f"MLflow/recipe metric {key} differs from raw predictions")
    for key, value in read_json(directory / "config.json").items():
        if observed.data.params.get(key) != str(value):
            raise ValueError(f"MLflow parameter {key} differs from the retained configuration")

    identity = {"source_sha256": record["source"]["source_sha256"],
                "data_sha256": record["data_sha256"],
                "split_sha256": record["split_sha256"]}
    for key, value in identity.items():
        if tags.get(key) != value:
            raise ValueError(f"MLflow tag {key} differs from the retained run")
    model_uri = tags["model_uri"]
    verify_logged_model(client, model_uri, run_id, record)
    if record.get("backend") != "sklearn":
        verify_history(client, run_id, read_json(directory / "history.json"),
                       observed.data.params.get("autolog_enabled") == "True")
    return {**identity, "model_uri": model_uri, "model_sha256": record["model_sha256"]}
