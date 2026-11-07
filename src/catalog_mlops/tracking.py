"""Record the existing CNN pipeline in MLflow without changing its learning recipe."""

from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
from pathlib import Path
import re
import threading
import time

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from mlflow.models import infer_signature
import mlflow.pytorch
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter

from catalog_mlops.artifacts import json_digest, read_json, write_json
from catalog_mlops.data import CLASS_NAMES, load_arrays, verify_data
from catalog_mlops.model import TrainingConfig
from catalog_mlops.training import load_model, model_state_sha256, runtime_source_sha256, train, verify_run


_TRACKING_LOCK = threading.Lock()


def tracking_uri(state: Path) -> str:
    state.mkdir(parents=True, exist_ok=True)
    return "sqlite:///" + (state.resolve() / "tracking.db").as_posix()



@contextmanager
def tracking_store(state: Path):
    """Use the same local tracking and registry store for native MLflow operations."""
    with _TRACKING_LOCK:
        previous_tracking, previous_registry = mlflow.get_tracking_uri(), mlflow.get_registry_uri()
        uri = tracking_uri(state)
        try:
            mlflow.set_tracking_uri(uri)
            mlflow.set_registry_uri(uri)
            yield MlflowClient(tracking_uri=uri, registry_uri=uri)
        finally:
            mlflow.set_tracking_uri(previous_tracking)
            mlflow.set_registry_uri(previous_registry)


def experiment_id(client: MlflowClient, state: Path, name: str) -> str:
    existing = client.get_experiment_by_name(name)
    if existing is not None:
        if existing.lifecycle_stage != "active":
            raise ValueError("The requested experiment is deleted. Restore it or choose another name.")
        return existing.experiment_id
    artifact_root = state.resolve() / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    try:
        return client.create_experiment(name, artifact_location=artifact_root.as_uri())
    except MlflowException as error:
        if error.error_code != "RESOURCE_ALREADY_EXISTS":
            raise
        return client.get_experiment_by_name(name).experiment_id



def verify_recipe_request(record: dict, request: dict) -> None:
    if (record["config_sha256"] != request["config_sha256"]
            or record["data_sha256"] != request["data_sha256"]
            or record["source"]["source_sha256"] != request["source_sha256"]):
        raise ValueError("Retained training result differs from the tracking request")


def verify_logged_model(client: MlflowClient, uri: str, run_id: str, record: dict):
    """Resolve the native MLflow model identity, then verify the actual learned weights."""
    if not re.fullmatch(r"models:/m-[0-9a-f]{32}", uri):
        raise ValueError("Expected the retained native MLflow logged-model URI")
    logged = client.get_logged_model(uri.removeprefix("models:/"))
    if logged.source_run_id != run_id:
        raise ValueError("Logged model belongs to a different source run")
    local_model = mlflow.artifacts.download_artifacts(artifact_uri=logged.artifact_location)
    metadata = mlflow.models.Model.load(local_model).metadata
    for field, expected in {"checkpoint_sha256": record["model_sha256"],
                            "state_sha256": record["trained_state_sha256"],
                            "split_sha256": record["split_sha256"],
                            "class_names": list(CLASS_NAMES)}.items():
        if metadata.get(field) != expected:
            raise ValueError(f"Logged model metadata differs for {field}")
    restored = mlflow.pytorch.load_model(local_model, map_location="cpu")
    restored.eval()
    if model_state_sha256(restored) != record["trained_state_sha256"]:
        raise ValueError("The logged model's weight identity differs from its source checkpoint")
    return restored


def verify_history(client, run_id, history, autolog):
    prefix = "auto" if autolog else "manual"
    keys = [key for key in history[0] if key != "epoch"]
    for key in keys:
        expected = {row["epoch"]: float(np.float32(row[key])) if autolog else row[key] for row in history}
        captured = client.get_metric_history(run_id, f"{prefix}/{key}")
        if {item.step for item in captured} != set(expected):
            raise ValueError(f"Tracking did not capture every epoch of {prefix}/{key}")
        if any(not np.isfinite(item.value) or abs(item.value - expected[item.step]) > 1e-12 for item in captured):
            raise ValueError(f"Tracking history differs from retained observations for {prefix}/{key}")
    return sorted(expected)


def tracked_train(data_root: Path, output: Path, config: TrainingConfig, state: Path,
                  name: str, autolog: bool = False, experiment: str = "threadline-cnn") -> dict:
    """Train once or resume logging a verified local result under its known MLflow ID.

    The process lock protects MLflow's global tracking URI and hook configuration.
    The directory lock reserves this local run across separate CLI processes.
    """
    with _TRACKING_LOCK:
        if mlflow.active_run() is not None:
            raise ValueError("Finish the current MLflow run before starting tracked pipeline training")
        output = output.resolve()
        state = state.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        reservation = output.parent / f".{output.name}.tracking.lock"
        reservation.mkdir()
        previous_uri = mlflow.get_tracking_uri()
        receipt_path = output.parent / f"{output.name}.tracking.json"
        client = None
        receipt = None
        attempt_started = False
        try:
            uri = tracking_uri(state)
            mlflow.set_tracking_uri(uri)
            client = MlflowClient(tracking_uri=uri)
            manifest = verify_data(data_root)
            request = {"tracking_uri": uri, "experiment": experiment,
                       "config_sha256": json_digest(config.to_dict()),
                       "data_sha256": json_digest(manifest),
                       "source_sha256": runtime_source_sha256(), "autolog_enabled": autolog}
            if receipt_path.exists():
                receipt = read_json(receipt_path)
                if any(receipt.get(key) != value for key, value in request.items()):
                    raise ValueError("This run's tracking receipt belongs to a different recipe, source or store")
                observed = client.get_run(receipt["run_id"])
                if observed.info.status == "FINISHED" and observed.data.tags.get("pipeline_status") == "complete":
                    record = verify_run(output)
                    verify_recipe_request(record, request)
                    if (observed.data.tags.get("model_uri") != receipt["model_uri"]
                            or observed.data.tags.get("checkpoint_sha256") != record["model_sha256"]):
                        raise ValueError("Completed local run differs from the logged model identity")
                    verify_logged_model(client, receipt["model_uri"], receipt["run_id"], record)
                    verify_history(client, receipt["run_id"], read_json(output / "history.json"), autolog)
                    receipt["status"] = "complete"
                    write_json(receipt_path, receipt)
                    return receipt
            else:
                if output.exists():
                    record = verify_run(output)
                    verify_recipe_request(record, request)
                created = client.create_run(experiment_id(client, state, experiment), run_name=name,
                                            tags={"pipeline_status": "pending", "task": "fashion-mnist"})
                attempt_started = True
                receipt = {**request, "run_id": created.info.run_id, "status": "pending",
                           "model_uri": None, "attempts": 0}
                write_json(receipt_path, receipt)

            attempt_started = True
            receipt["attempts"] += 1
            receipt["status"] = "logging"
            write_json(receipt_path, receipt)
            started = time.perf_counter()
            mlflow.pytorch.autolog(log_every_n_step=1, log_models=False, checkpoint=False,
                                  disable=not autolog)
            with mlflow.start_run(run_id=receipt["run_id"]):
                mlflow.log_params({**config.to_dict(), "autolog_enabled": autolog})
                mlflow.set_tags({"pipeline_status": "running", "source_sha256": request["source_sha256"],
                                 "split_sha256": manifest["split_sha256"],
                                 "data_sha256": request["data_sha256"], "initialization": "from-scratch",
                                 "primary_metric": "validation_macro_f1", "attempts": receipt["attempts"]})
                events = state / "tensorboard" / receipt["run_id"]
                writer_context = SummaryWriter(log_dir=str(events)) if autolog else nullcontext(None)
                with writer_context as writer:
                    def observe(observation):
                        step = observation["epoch"]
                        values = {key: value for key, value in observation.items() if key != "epoch"}
                        if autolog:
                            for key, value in values.items():
                                writer.add_scalar(f"auto/{key}", value, global_step=step)
                        else:
                            mlflow.log_metrics({f"manual/{key}": value for key, value in values.items()}, step=step)

                    try:
                        if output.exists():
                            record = verify_run(output)
                            verify_recipe_request(record, request)
                            history = read_json(output / "history.json")
                            prefix = "auto" if autolog else "manual"
                            present = {key: {item.step for item in client.get_metric_history(
                                receipt["run_id"], f"{prefix}/{key}")}
                                for key in history[0] if key != "epoch"}
                            for observation in history:
                                missing = {key: value for key, value in observation.items()
                                           if key != "epoch" and observation["epoch"] not in present[key]}
                                if missing:
                                    observe({"epoch": observation["epoch"], **missing})
                            mlflow.set_tag("telemetry_history_replayed", "true")
                        else:
                            record = train(data_root, output, config, telemetry=observe)
                            history = read_json(output / "history.json")
                            verify_recipe_request(record, request)
                    finally:
                        if autolog:
                            # This public TB operation flushes the pinned MLflow scalar queue, including after failure.
                            writer.add_hparams({"autolog_hook": "tensorboard"}, {})

                metrics = read_json(output / "metrics.json")
                mlflow.log_metrics({"validation_macro_f1": metrics["macro_f1"],
                                    "validation_accuracy": metrics["accuracy"],
                                    "validation_loss": metrics["loss"],
                                    "training_seconds": record["training_seconds"],
                                    "parameters": record["parameters"]})
                class_metrics = {}
                for label, class_name in enumerate(CLASS_NAMES):
                    for metric in ("precision", "recall", "f1", "support"):
                        class_metrics[f"class_{label}_{metric}"] = metrics["per_class"][class_name][metric]
                mlflow.log_metrics(class_metrics)
                mlflow.log_artifacts(str(output), artifact_path="recipe")
                model, checkpoint = load_model(output / "model.pt")
                images, _ = load_arrays(data_root)
                probe_ids = np.asarray(manifest["partitions"]["validation"]).reshape(10, -1)[:, 0]
                example = images[probe_ids, None, :, :].astype(np.float32) / 255.0
                with torch.inference_mode():
                    expected_logits = model(torch.from_numpy(example)).numpy()
                if receipt["model_uri"] is None:
                    info = mlflow.pytorch.log_model(
                        model, name="cnn", code_paths=[str(Path(__file__).parent)],
                        signature=infer_signature(example, expected_logits), input_example=example,
                        pip_requirements=["torch==2.8.0", "numpy==2.3.3", "mlflow==3.5.1", "sqlalchemy==2.0.44"],
                        metadata={"class_names": list(CLASS_NAMES),
                                  "preprocessing": checkpoint["preprocessing"],
                                  "checkpoint_sha256": record["model_sha256"],
                                  "state_sha256": record["trained_state_sha256"],
                                  "split_sha256": record["split_sha256"]})
                    receipt["model_uri"] = info.model_uri
                    write_json(receipt_path, receipt)
                restored = verify_logged_model(client, receipt["model_uri"], receipt["run_id"], record)
                with torch.inference_mode():
                    actual_logits = restored(torch.from_numpy(example)).numpy()
                np.testing.assert_allclose(actual_logits, expected_logits, rtol=0, atol=0)
                captured_steps = verify_history(client, receipt["run_id"], history, autolog)
                if autolog and client.get_run(receipt["run_id"]).data.params.get("autolog_hook") != "tensorboard":
                    raise ValueError("The TensorBoard hyperparameter hook did not capture its proof parameter")
                mlflow.set_tags({"pipeline_status": "complete", "model_uri": receipt["model_uri"],
                                 "checkpoint_sha256": record["model_sha256"], "logged_model_reload_exact": "true"})
                mlflow.log_metric("tracked_wall_seconds", time.perf_counter() - started)
                receipt.update(status="logged", captured_epoch_steps=captured_steps,
                               logged_model_reload_exact=True,
                               completed_at=datetime.now(timezone.utc).isoformat())
                write_json(receipt_path, receipt)
            receipt["status"] = "complete"
            write_json(receipt_path, receipt)
            return receipt
        except BaseException:
            if attempt_started and client is not None and receipt is not None:
                client.set_tag(receipt["run_id"], "pipeline_status", "incomplete")
                client.set_terminated(receipt["run_id"], status="FAILED")
            raise
        finally:
            mlflow.pytorch.autolog(disable=True)
            mlflow.set_tracking_uri(previous_uri)
            reservation.rmdir()


def download_recipe(client: MlflowClient, run_id: str, destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    return Path(client.download_artifacts(run_id, "recipe", str(destination)))
