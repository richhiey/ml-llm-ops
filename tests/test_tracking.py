"""Exercise real MLflow/TensorBoard behavior with explicitly synthetic mechanics data."""

from dataclasses import replace
from pathlib import Path

import mlflow
from mlflow import MlflowClient
import numpy as np
import pytest

from catalog_mlops import tracking, training
from catalog_mlops.artifacts import read_json, write_json
from catalog_mlops.comparison import compare_runs
from catalog_mlops.model import TrainingConfig


@pytest.fixture
def mechanics(tmp_path, monkeypatch):
    rng = np.random.default_rng(22)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.tile(np.arange(10, dtype=np.uint8), 4)
    manifest = {"name": "synthetic-tracking-fixture", "split_sha256": "mechanics-split",
                "partitions": {"train": list(range(20)), "validation": list(range(20, 40))}}
    for module in (training, tracking):
        monkeypatch.setattr(module, "verify_data", lambda _: manifest)
        monkeypatch.setattr(module, "load_arrays", lambda _: (images, labels))
    return tmp_path, TrainingConfig(epochs=1, batch_size=10, cpu_threads=1)


def test_autolog_captures_real_events_and_completion_is_reusable(mechanics, monkeypatch):
    root, config = mechanics
    state = root / "state"
    manual = tracking.tracked_train(root, root / "manual", config, state, "manual")
    automatic = tracking.tracked_train(root, root / "automatic", config, state, "automatic", autolog=True)
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    before = client.get_run(manual["run_id"])
    after = client.get_run(automatic["run_id"])
    assert "autolog_hook" not in before.data.params
    assert after.data.params["autolog_hook"] == "tensorboard"
    assert "auto/train_loss" not in before.data.metrics
    assert [item.step for item in client.get_metric_history(automatic["run_id"], "auto/train_loss")] == [1]
    assert before.data.metrics["validation_macro_f1"] == after.data.metrics["validation_macro_f1"]
    assert automatic["model_uri"].startswith("models:/m-")
    assert automatic["logged_model_reload_exact"]

    def unexpected_training(*args, **kwargs):
        raise AssertionError("A completed logging receipt must not refit the model")

    monkeypatch.setattr(tracking, "train", unexpected_training)
    repeated = tracking.tracked_train(root, root / "automatic", config, state, "automatic", autolog=True)
    assert repeated["run_id"] == automatic["run_id"]
    assert len(client.search_runs([after.info.experiment_id])) == 2
    assert mlflow.active_run() is None


def test_model_logging_failure_resumes_same_run_without_retraining(mechanics, monkeypatch):
    root, config = mechanics
    state = root / "state"
    original_log_model = mlflow.pytorch.log_model

    def failed_log(*args, **kwargs):
        raise RuntimeError("simulated model-store interruption")

    monkeypatch.setattr(mlflow.pytorch, "log_model", failed_log)
    with pytest.raises(RuntimeError, match="model-store"):
        tracking.tracked_train(root, root / "candidate", config, state, "candidate", autolog=True)
    pending = read_json(root / "candidate.tracking.json")
    assert (root / "candidate/model.pt").is_file()
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    assert client.get_run(pending["run_id"]).info.status == "FAILED"
    monkeypatch.setattr(mlflow.pytorch, "log_model", original_log_model)

    def unexpected_training(*args, **kwargs):
        raise AssertionError("Completed local training must be retained on a logging retry")

    monkeypatch.setattr(tracking, "train", unexpected_training)
    resumed = tracking.tracked_train(root, root / "candidate", config, state, "candidate", autolog=True)
    assert resumed["run_id"] == pending["run_id"]
    assert resumed["attempts"] == 2
    assert client.get_run(resumed["run_id"]).info.status == "FINISHED"
    with pytest.raises(ValueError, match="different recipe"):
        tracking.tracked_train(root, root / "candidate", replace(config, epochs=2), state, "candidate", autolog=True)
    assert client.get_run(resumed["run_id"]).info.status == "FINISHED"


def test_comparison_checks_controls_raw_metrics_and_distinct_configurations(mechanics):
    root, config = mechanics
    state = root / "state"
    baseline = tracking.tracked_train(root, root / "baseline", config, state, "baseline")
    longer = tracking.tracked_train(root, root / "longer", replace(config, epochs=2), state, "longer")
    confounded = tracking.tracked_train(root, root / "confounded", replace(config, epochs=2, weight_decay=0.001), state, "confounded")
    report = compare_runs(state, baseline["run_id"], [longer["run_id"], confounded["run_id"], longer["run_id"]])
    assert report["distinct_candidates"] == 1
    assert report["rows"][1]["comparable"]
    assert not report["rows"][2]["comparable"]
    assert report["rows"][3]["kind"] == "duplicate"
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    client.log_metric(longer["run_id"], "validation_macro_f1", 1.0)
    mismatched = compare_runs(state, baseline["run_id"], [longer["run_id"]])
    assert not mismatched["rows"][1]["comparable"]
    assert mismatched["selected_run_id"] == baseline["run_id"]


def test_training_failure_flushes_auto_events_and_does_not_leak_hooks(mechanics, monkeypatch):
    root, config = mechanics
    state = root / "state"
    original_train = tracking.train

    def interrupted_train(data_root, output, config, telemetry):
        telemetry({"epoch": 1, "train_loss": 0.5, "validation_loss": 0.6,
                   "validation_accuracy": 0.2, "validation_macro_f1": 0.1})
        raise RuntimeError("simulated training interruption")

    monkeypatch.setattr(tracking, "train", interrupted_train)
    with pytest.raises(RuntimeError, match="training interruption"):
        tracking.tracked_train(root, root / "failed", config, state, "failed", autolog=True)
    failed = read_json(root / "failed.tracking.json")
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    assert client.get_run(failed["run_id"]).info.status == "FAILED"
    assert len(client.get_metric_history(failed["run_id"], "auto/train_loss")) == 1
    assert mlflow.active_run() is None
    monkeypatch.setattr(tracking, "train", original_train)
    manual = tracking.tracked_train(root, root / "manual", config, state, "manual")
    assert "auto/train_loss" not in client.get_run(manual["run_id"]).data.metrics


def test_comparison_publication_never_overwrites_an_existing_decision(tmp_path):
    path = tmp_path / "decision.json"
    write_json(path, {"selected": "original"}, overwrite=False)
    with pytest.raises(FileExistsError):
        write_json(path, {"selected": "changed"}, overwrite=False)
    assert read_json(path) == {"selected": "original"}


def test_completed_receipt_rejects_another_valid_local_dataset_run(mechanics, monkeypatch):
    import shutil
    root, config = mechanics
    state = root / "state"
    receipt = tracking.tracked_train(root, root / "original", config, state, "original")
    original_manifest = training.verify_data(root)
    with monkeypatch.context() as patch:
        patch.setattr(training, "verify_data", lambda _: {**original_manifest, "name": "another-snapshot"})
        training.train(root, root / "replacement", config)
    shutil.rmtree(root / "original")
    (root / "replacement").rename(root / "original")
    with pytest.raises(ValueError, match="differs from the tracking request"):
        tracking.tracked_train(root, root / "original", config, state, "original")
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    assert client.get_run(receipt["run_id"]).info.status == "FINISHED"


def test_partial_epoch_is_repaired_without_duplicate_scalars_or_retraining(mechanics, monkeypatch):
    root, config = mechanics
    config = replace(config, epochs=2)
    state = root / "state"
    training.train(root, root / "retained", config)
    original_log = mlflow.log_metrics

    def interrupted_log(values, *args, **kwargs):
        if "manual/train_loss" in values:
            original_log({"manual/train_loss": values["manual/train_loss"]}, *args, **kwargs)
            raise RuntimeError("interrupted after first scalar")
        return original_log(values, *args, **kwargs)

    monkeypatch.setattr(mlflow, "log_metrics", interrupted_log)
    with pytest.raises(RuntimeError, match="first scalar"):
        tracking.tracked_train(root, root / "retained", config, state, "retained")
    pending = read_json(root / "retained.tracking.json")
    monkeypatch.setattr(mlflow, "log_metrics", original_log)
    monkeypatch.setattr(tracking, "train", lambda *a, **k: pytest.fail("Retry must not retrain"))
    resumed = tracking.tracked_train(root, root / "retained", config, state, "retained")
    assert resumed["run_id"] == pending["run_id"]
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    history = read_json(root / "retained/history.json")
    for key in ("train_loss", "validation_loss", "validation_accuracy", "validation_macro_f1"):
        captured = client.get_metric_history(resumed["run_id"], f"manual/{key}")
        assert sorted((item.step, item.value) for item in captured) == [(row["epoch"], row[key]) for row in history]


def test_model_uri_must_identify_the_model_from_the_evaluated_run(mechanics):
    root, config = mechanics
    state = root / "state"
    baseline = tracking.tracked_train(root, root / "baseline", config, state, "baseline")
    candidate = tracking.tracked_train(root, root / "candidate", replace(config, epochs=2), state, "candidate")
    client = MlflowClient(tracking_uri=tracking.tracking_uri(state))
    for replacement in (baseline["model_uri"], "models:/invalid"):
        client.set_tag(candidate["run_id"], "model_uri", replacement)
        comparison = compare_runs(state, baseline["run_id"], [candidate["run_id"]])
        assert not comparison["rows"][1]["comparable"]
        assert comparison["selected_run_id"] == baseline["run_id"]


def test_source_change_between_request_and_training_cannot_complete(mechanics, monkeypatch):
    root, config = mechanics
    original_train = tracking.train
    source_files = training.source_files

    def changed_source_train(*args, **kwargs):
        with monkeypatch.context() as patch:
            patch.setattr(training, "source_files", lambda: {**source_files(), "changed-source.txt": b"changed"})
            return original_train(*args, **kwargs)

    monkeypatch.setattr(tracking, "train", changed_source_train)
    with pytest.raises(ValueError, match="differs from the tracking request"):
        tracking.tracked_train(root, root / "candidate", config, root / "state", "candidate")
    receipt = read_json(root / "candidate.tracking.json")
    client = MlflowClient(tracking_uri=tracking.tracking_uri(root / "state"))
    assert client.get_run(receipt["run_id"]).info.status == "FAILED"
