"""Fit and evaluate scikit-learn models on the fixed image study."""

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import time

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from threadpoolctl import threadpool_limits

from src.artifacts import bytes_digest, json_digest, sha256, write_json
from src.data import load_arrays, verify_data
from src.evaluation import score_predictions
from src.features import flatten_pixels


def build_model(config: dict):
    """Map a recipe to a fitted-pipeline specification with fixed CPU defaults."""
    kind = config["estimator"]
    factories = {
        "logistic_regression": (LogisticRegression, {"max_iter": 1500}),
        "random_forest": (RandomForestClassifier, {"n_estimators": 50, "n_jobs": 1}),
        "mlp": (MLPClassifier, {"hidden_layer_sizes": (64,), "max_iter": 200}),
    }
    if kind not in factories or set(config) != {"estimator", "params", "seed"}:
        raise ValueError("Use a supported estimator, its params and an explicit seed")
    estimator, defaults = factories[kind]
    settings = {**defaults, **config["params"], "random_state": config["seed"]}
    return make_pipeline(FunctionTransformer(flatten_pixels), estimator(**settings))


def fitted_state_sha256(model) -> str:
    """Hash semantic learned arrays, excluding unused padding in serialized tree buffers."""
    estimator = model[-1]
    arrays = [estimator.classes_]
    if isinstance(estimator, RandomForestClassifier):
        for tree in estimator.estimators_:
            state = tree.tree_
            arrays.extend((
                state.children_left, state.children_right, state.feature,
                state.threshold, state.value, state.missing_go_to_left,
            ))
    elif isinstance(estimator, MLPClassifier):
        arrays.extend(estimator.coefs_ + estimator.intercepts_)
    else:
        arrays.extend((estimator.coef_, estimator.intercept_))
    return json_digest([
        {"dtype": str(array.dtype), "shape": list(array.shape), "sha256": bytes_digest(array.tobytes())}
        for array in arrays
    ])


def classify(model, images: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with threadpool_limits(limits=2, user_api="blas"):
        probabilities = model.predict_proba(images)
    columns = probabilities.argmax(axis=1)
    return model.classes_[columns], probabilities[np.arange(len(images)), columns], probabilities


def evaluate_images(model, images: np.ndarray, labels: np.ndarray):
    predicted, scores, probabilities = classify(model, images)
    report = score_predictions(labels, predicted)
    report["loss"] = float(log_loss(labels, probabilities, labels=model.classes_))
    return report, predicted, scores


def train_sklearn(data_root: Path, output: Path, config: dict) -> dict:
    # The common artifact format also supports archived CNN runs.
    from src.training import environment_record, model_state_sha256, source_snapshot, write_predictions

    if output.exists():
        raise FileExistsError(f"Run directory already exists: {output}")
    model = build_model(config)
    manifest = verify_data(data_root)
    images, labels = load_arrays(data_root)
    train_ids = manifest["partitions"]["train"]
    validation_ids = manifest["partitions"]["validation"]
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=".training-") as private:
        run = Path(private) / "result"
        run.mkdir()
        started = time.perf_counter()
        source = source_snapshot(run / "source.zip")
        write_json(run / "config.json", config)
        write_json(run / "dataset.json", manifest)
        write_json(run / "environment.json", environment_record())
        initial = json_digest(config)
        fit_started = time.perf_counter()
        with threadpool_limits(limits=2, user_api="blas"):
            model.fit(images[train_ids], labels[train_ids])
        training_seconds = time.perf_counter() - fit_started
        joblib.dump(model, run / "model.joblib")
        restored = joblib.load(run / "model.joblib")
        probe = images[validation_ids[:10]]
        np.testing.assert_array_equal(classify(model, probe)[2], classify(restored, probe)[2])
        metrics, predictions, scores = evaluate_images(restored, images[validation_ids], labels[validation_ids])
        write_predictions(run / "validation-predictions.csv", validation_ids,
                          labels[validation_ids], predictions, scores)
        write_json(run / "metrics.json", metrics)
        record = {
            "schema": 1, "status": "complete", "backend": "sklearn",
            "architecture": config["estimator"], "initialization": "from-scratch",
            "created_at": datetime.now(timezone.utc).isoformat(), "source": source,
            "config_sha256": json_digest(config), "data_sha256": json_digest(manifest),
            "split_sha256": manifest["split_sha256"], "model_sha256": sha256(run / "model.joblib"),
            "environment_sha256": sha256(run / "environment.json"),
            "validation_predictions_sha256": sha256(run / "validation-predictions.csv"),
            "metrics_sha256": sha256(run / "metrics.json"),
            "validation_accuracy": metrics["accuracy"], "validation_macro_f1": metrics["macro_f1"],
            "train_count": len(train_ids), "validation_count": len(validation_ids),
            "initial_state_sha256": initial, "trained_state_sha256": model_state_sha256(restored),
            "training_seconds": training_seconds, "total_seconds": time.perf_counter() - started,
            "checkpoint_reload_exact": True,
        }
        write_json(run / "run.json", record)
        reservation = output.parent / f".{output.name}.lock"
        reservation.mkdir()
        try:
            if output.exists():
                raise FileExistsError(f"Another process already published {output}")
            run.rename(output)
        finally:
            reservation.rmdir()
        return record
