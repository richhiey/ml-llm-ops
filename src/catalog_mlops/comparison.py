"""Compare raw held-out CNN evidence under declared one-factor controls."""

import csv
from datetime import datetime, timezone
from pathlib import Path
import re
import tempfile

from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
import numpy as np

from catalog_mlops.artifacts import json_digest, read_json
from catalog_mlops.evaluation import score_predictions
from catalog_mlops.tracking import download_recipe, tracking_uri, verify_logged_model, verify_history
from catalog_mlops.training import verify_run


def inspect_tracked_run(client: MlflowClient, run_id: str, destination: Path) -> dict:
    if not re.fullmatch(r"[0-9a-f]{32}", run_id):
        raise ValueError("Use a full 32-character MLflow run ID")
    observed = client.get_run(run_id)
    if observed.info.status != "FINISHED" or observed.data.tags.get("pipeline_status") != "complete":
        raise ValueError("Run has not completed both learning and verified model logging")
    directory = download_recipe(client, run_id, destination / run_id)
    record = verify_run(directory)
    config = read_json(directory / "config.json")
    dataset = read_json(directory / "dataset.json")
    metrics = read_json(directory / "metrics.json")
    environment = read_json(directory / "environment.json")
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
    for field, key in (("macro_f1", "validation_macro_f1"), ("accuracy", "validation_accuracy")):
        values = [metrics[field], record[key], observed.data.metrics.get(key, float("inf"))]
        if not np.isfinite(values).all() or not np.allclose(values, raw[field], rtol=0, atol=1e-12):
            raise ValueError(f"MLflow/recipe metric {key} differs from raw predictions")
    for key, value in config.items():
        if observed.data.params.get(key) != str(value):
            raise ValueError(f"MLflow parameter {key} differs from the retained configuration")
    controls = {"source_sha256": record["source"]["source_sha256"],
                "data_sha256": record["data_sha256"], "split_sha256": record["split_sha256"],
                "environment_sha256": record["environment_sha256"],
                "architecture": record["architecture"], "validation_count": metrics["count"],
                "initial_state_sha256": record["initial_state_sha256"],
                "primary_metric": record["primary_metric"]}
    for key in ("source_sha256", "data_sha256", "split_sha256", "primary_metric"):
        if observed.data.tags.get(key) != str(controls[key]):
            raise ValueError(f"MLflow tag {key} differs from the retained run")
    verify_logged_model(client, observed.data.tags["model_uri"], run_id, record)
    verify_history(client, run_id, read_json(directory / "history.json"),
                   observed.data.params.get("autolog_enabled") == "True")
    return {"run_id": run_id, "name": observed.data.tags.get("mlflow.runName", run_id),
            "config": config, "controls": controls, "config_sha256": record["config_sha256"],
            "validation_macro_f1": raw["macro_f1"], "validation_accuracy": raw["accuracy"],
            "training_seconds": record["training_seconds"], "per_class": raw["per_class"],
            "model_uri": observed.data.tags["model_uri"], "model_sha256": record["model_sha256"],
            "environment": environment, "autolog_enabled": observed.data.params.get("autolog_enabled") == "True"}


def compare_runs(state: Path, baseline_run_id: str, run_ids: list[str]) -> dict:
    """Retain excluded rows and rank eligible distinct configurations by raw macro F1."""
    client = MlflowClient(tracking_uri=tracking_uri(state))
    with tempfile.TemporaryDirectory(prefix="catalog-comparison-") as temporary:
        destination = Path(temporary)
        baseline = inspect_tracked_run(client, baseline_run_id, destination)
        baseline.update(kind="baseline", comparable=True, reasons=[], changed_field=None, delta_macro_f1=0.0)
        rows = [baseline]
        seen_ids = {baseline_run_id}
        seen_configs = {baseline["config_sha256"]}
        for run_id in run_ids:
            if run_id in seen_ids:
                rows.append({"run_id": run_id, "kind": "duplicate", "comparable": False,
                             "reasons": ["Repeated run ID does not add another configuration"]})
                continue
            seen_ids.add(run_id)
            try:
                row = inspect_tracked_run(client, run_id, destination)
            except (ValueError, KeyError, OSError, MlflowException) as error:
                rows.append({"run_id": run_id, "kind": "excluded", "comparable": False, "reasons": [str(error)]})
                continue
            reasons = []
            for key, value in baseline["controls"].items():
                if row["controls"].get(key) != value:
                    reasons.append(f"Changed comparison control {key}")
            changed = [key for key, value in baseline["config"].items() if row["config"].get(key) != value]
            if row["config_sha256"] in seen_configs:
                kind = "repeat"
            else:
                kind = "candidate"
                if len(changed) != 1:
                    reasons.append("An improvement candidate must change exactly one declared training factor")
                if set(changed) & {"seed", "cpu_threads"}:
                    reasons.append("Seed and CPU thread count are fixed comparison controls")
            row.update(kind=kind, comparable=not reasons, reasons=reasons,
                       changed_field=changed[0] if len(changed) == 1 else None,
                       delta_macro_f1=row["validation_macro_f1"] - baseline["validation_macro_f1"])
            rows.append(row)
            if not reasons:
                seen_configs.add(row["config_sha256"])
        eligible = [row for row in rows if row["comparable"] and row["kind"] in {"baseline", "candidate"}]
        selected = max(eligible, key=lambda row: row["validation_macro_f1"])
        result = {"schema": 1, "created_at": datetime.now(timezone.utc).isoformat(),
                  "tracking_uri": tracking_uri(state), "baseline_run_id": baseline_run_id,
                  "primary_metric": "validation_macro_f1", "direction": "maximize",
                  "tie_rule": "Keep the earliest declared eligible row, with baseline first",
                  "rows": rows, "selected_run_id": selected["run_id"], "selected_model_uri": selected["model_uri"],
                  "distinct_candidates": sum(row["kind"] == "candidate" and row["comparable"] for row in rows),
                  "interpretation": "Best observed eligible configuration under these fixed conditions"}
        result["comparison_sha256"] = json_digest(result)
        return result
