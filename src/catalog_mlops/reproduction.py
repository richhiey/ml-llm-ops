"""Verify native saved-model evaluation and clean from-scratch replay separately."""

from datetime import datetime, timezone
from pathlib import Path
import csv

from mlflow import MlflowClient
import numpy as np

from catalog_mlops.artifacts import json_digest, read_json, sha256
from catalog_mlops.evaluation import score_predictions
from catalog_mlops.tracking import tracking_uri, verify_logged_model
from catalog_mlops.training import load_model, model_state_sha256, verify_run


# This policy is declared before the replay, not fitted to its result.
REPLAY_POLICY = {
    "schema": 1,
    "name": "clean-cpu-replay-v1",
    "saved_metric_atol": 1e-12,
    "retrained_macro_f1_atol": 0.002,
    "retrained_accuracy_atol": 0.002,
    "require_same_source_data_config_environment": True,
}


def verify_reproduction(
    state: Path,
    run_id: str,
    recipe: Path,
    retrained: Path,
    saved_evaluation: Path,
    retrained_evaluation: Path,
) -> dict:
    original, repeated = verify_run(recipe), verify_run(retrained)
    client = MlflowClient(tracking_uri=tracking_uri(state))
    observed = client.get_run(run_id)
    if (
        observed.info.status != "FINISHED"
        or observed.data.tags.get("pipeline_status") != "complete"
    ):
        raise ValueError("The original tracked experiment is incomplete")
    for field, expected in {
        "source_sha256": original["source"]["source_sha256"],
        "data_sha256": original["data_sha256"],
        "split_sha256": original["split_sha256"],
        "checkpoint_sha256": original["model_sha256"],
    }.items():
        if observed.data.tags.get(field) != expected:
            raise ValueError(
                f"Retrieved recipe differs from tracked experiment: {field}"
            )
    verify_logged_model(client, observed.data.tags["model_uri"], run_id, original)
    saved, fitted = read_json(saved_evaluation), read_json(retrained_evaluation)
    checks = {
        "distinct_training_record": recipe.resolve() != retrained.resolve()
        and sha256(recipe / "run.json") != sha256(retrained / "run.json")
        and original["created_at"] != repeated["created_at"],
        "separate_evaluation_files": saved_evaluation.resolve()
        != retrained_evaluation.resolve(),
        "source": original["source"]["source_sha256"]
        == repeated["source"]["source_sha256"],
        "data": original["data_sha256"] == repeated["data_sha256"],
        "split": original["split_sha256"] == repeated["split_sha256"],
        "configuration": original["config_sha256"] == repeated["config_sha256"],
        "environment": original["environment_sha256"] == repeated["environment_sha256"],
        "initial_weights": original["initial_state_sha256"]
        == repeated["initial_state_sha256"],
    }
    for label, evaluation, record in [
        ("saved", saved, original),
        ("retrained", fitted, repeated),
    ]:
        identity = evaluation["evaluation_evidence"]
        checks[f"{label}_evaluation_identity"] = (
            identity["model_sha256"] == record["model_sha256"]
            and identity["split_sha256"] == original["split_sha256"]
            and identity["evaluation_source_sha256"]
            == original["source"]["source_sha256"]
            and evaluation["count"] == record["validation_count"]
        )
        for metric, recorded in [
            ("macro_f1", "validation_macro_f1"),
            ("accuracy", "validation_accuracy"),
        ]:
            values = [evaluation[metric], record[recorded]]
            checks[f"{label}_{metric}_record_consistent"] = bool(
                np.isfinite(values).all()
                and abs(values[0] - values[1]) <= REPLAY_POLICY["saved_metric_atol"]
            )
    for metric in ("macro_f1", "accuracy"):
        checks[f"saved_{metric}_matches_tracked"] = (
            abs(saved[metric] - observed.data.metrics[f"validation_{metric}"])
            <= REPLAY_POLICY["saved_metric_atol"]
        )
        checks[f"retrained_{metric}_within_tolerance"] = (
            abs(fitted[metric] - saved[metric])
            <= REPLAY_POLICY[f"retrained_{metric}_atol"]
        )
    with (
        (recipe / "validation-predictions.csv").open() as first,
        (retrained / "validation-predictions.csv").open() as second,
    ):
        original_rows, repeated_rows = (
            list(csv.DictReader(first)),
            list(csv.DictReader(second)),
        )
    checks["evaluation_ids_and_labels"] = [
        (r["image_id"], r["label"]) for r in original_rows
    ] == [(r["image_id"], r["label"]) for r in repeated_rows]
    for label, directory, rows, evaluation, record in (
        ("saved", recipe, original_rows, saved, original),
        ("retrained", retrained, repeated_rows, fitted, repeated),
    ):
        raw = score_predictions(
            np.array([int(row["label"]) for row in rows]),
            np.array([int(row["prediction"]) for row in rows]),
        )
        expected_ids = [
            f"train:{image_id}"
            for image_id in read_json(directory / "dataset.json")["partitions"][
                "validation"
            ]
        ]
        checks[f"{label}_prediction_ids"] = [
            row["image_id"] for row in rows
        ] == expected_ids
        checks[f"{label}_raw_metrics"] = raw["confusion_matrix"] == evaluation[
            "confusion_matrix"
        ] and all(
            abs(raw[key] - evaluation[key]) <= REPLAY_POLICY["saved_metric_atol"]
            for key in ("accuracy", "macro_f1")
        )
        model, _ = load_model(directory / "model.pt")
        checks[f"{label}_weight_identity"] = (
            model_state_sha256(model) == record["trained_state_sha256"]
        )
    result = {
        "schema": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "execution_scope": "Checks retained artifacts; retain fresh-environment command and interpreter evidence separately.",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "policy": REPLAY_POLICY,
        "original_run_id": run_id,
        "original_model_sha256": original["model_sha256"],
        "original_source_sha256": original["source"]["source_sha256"],
        "original_trained_state_sha256": original["trained_state_sha256"],
        "retrained_state_exact": original["trained_state_sha256"]
        == repeated["trained_state_sha256"],
        "saved_metrics": {key: saved[key] for key in ("accuracy", "macro_f1")},
        "retrained_metrics": {key: fitted[key] for key in ("accuracy", "macro_f1")},
        "inputs": {
            "recipe": str(recipe.resolve()),
            "retrained": str(retrained.resolve()),
            "saved_evaluation": str(saved_evaluation.resolve()),
            "retrained_evaluation": str(retrained_evaluation.resolve()),
        },
        "input_sha256": {
            "recipe_run": sha256(recipe / "run.json"),
            "retrained_run": sha256(retrained / "run.json"),
            "saved_evaluation": sha256(saved_evaluation),
            "retrained_evaluation": sha256(retrained_evaluation),
        },
    }
    result["verification_sha256"] = json_digest(result)
    return result
