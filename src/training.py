"""Train a fresh CNN and retain the recipe needed to inspect and reproduce it."""

import csv
from datetime import datetime, timezone
import importlib.metadata
from pathlib import Path
import platform
import random
import shutil
import subprocess
import tempfile
import time
import zipfile

import joblib
import numpy as np
from sklearn.base import BaseEstimator
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.artifacts import bytes_digest, json_digest, read_json, sha256, write_json
from src.data import CLASS_NAMES, load_arrays, verify_data
from src.evaluation import evaluate
from src.model import CatalogCNN, TrainingConfig
from src.preprocessing import normalize_pixels


def make_loader(images: np.ndarray, labels: np.ndarray, ids: list[int], config: TrainingConfig,
                shuffle: bool = False) -> DataLoader:
    dataset = TensorDataset(torch.from_numpy(images[ids].copy()).unsqueeze(1),
                            torch.from_numpy(labels[ids].astype(np.int64)))
    return DataLoader(dataset, batch_size=config.batch_size, shuffle=shuffle, num_workers=0,
                      generator=torch.Generator().manual_seed(config.seed))


def configure_cpu(config: TrainingConfig) -> None:
    random.seed(config.seed)
    np.random.seed(config.seed)
    torch.manual_seed(config.seed)
    torch.set_num_threads(config.cpu_threads)
    torch.use_deterministic_algorithms(True)


def model_state_sha256(model: nn.Module | BaseEstimator) -> str:
    """Identify named weight values independently of a serialization container."""
    if isinstance(model, BaseEstimator):
        from src.sklearn_model import fitted_state_sha256

        return fitted_state_sha256(model)
    parameters = []
    for name, tensor in sorted(model.state_dict().items()):
        values = tensor.detach().cpu().contiguous().numpy()
        parameters.append({"name": name, "shape": list(values.shape), "dtype": str(values.dtype),
                           "values_sha256": bytes_digest(values.tobytes())})
    return json_digest(parameters)


def translate_batch(inputs: torch.Tensor, pixels: int, generator: torch.Generator) -> torch.Tensor:
    if pixels == 0:
        return inputs
    padded = nn.functional.pad(inputs, (pixels, pixels, pixels, pixels))
    offsets = torch.randint(0, 2 * pixels + 1, (len(inputs), 2), generator=generator)
    shifted = torch.empty_like(inputs)
    for index, (top, left) in enumerate(offsets.tolist()):
        shifted[index] = padded[index, :, top:top + 28, left:left + 28]
    return shifted


def source_files() -> dict[str, bytes]:
    root = Path(__file__).resolve().parents[1]
    files = sorted((root / "src").rglob("*.py"))
    files += sorted((root / "scripts").rglob("*.py"))
    files += [root / name for name in ("pyproject.toml", "uv.lock", ".python-version")]
    if not all(path.is_file() for path in files):
        raise ValueError("Source checkout and environment lock are required to record reproducible runs")
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in files}


def runtime_source_sha256() -> str:
    return json_digest({name: bytes_digest(content) for name, content in source_files().items()})


def source_snapshot(destination: Path) -> dict:
    root = Path(__file__).resolve().parents[1]
    contents = source_files()
    hashes = {name: bytes_digest(content) for name, content in contents.items()}
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in contents.items():
            archive.writestr(name, content)
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True,
                                         stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True))
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit, dirty = None, None
    return {"git_commit": commit, "git_dirty": dirty, "file_sha256": hashes,
            "source_sha256": json_digest(hashes), "archive_sha256": sha256(destination)}


def environment_record() -> dict:
    packages = {}
    for package in ("torch", "torchvision", "numpy", "scikit-learn", "mlflow", "sqlalchemy", "fastapi", "tensorboard"):
        packages[package] = importlib.metadata.version(package)
    return {"python": platform.python_version(), "platform": platform.platform(),
            "machine": platform.machine(), "packages": packages, "device": "cpu"}


def write_predictions(path: Path, ids: list[int], truth: np.ndarray,
                      predicted: np.ndarray, scores: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["image_id", "label", "prediction", "top_score"])
        for image_id, label, prediction, score in zip(ids, truth, predicted, scores, strict=True):
            writer.writerow([f"train:{image_id}", int(label), int(prediction), float(score)])


def read_training_config(path: Path) -> TrainingConfig | dict:
    values = read_json(path)
    return values if "estimator" in values else TrainingConfig(**values)


def train(data_root: Path, output: Path, config: TrainingConfig | dict, telemetry=None) -> dict:
    if isinstance(config, dict):
        from src.sklearn_model import train_sklearn

        return train_sklearn(data_root, output, config)
    """Create a new result directory only after successful training and checkpoint reload."""
    if output.exists():
        raise FileExistsError(f"Run directory already exists. Inspect its retained results or choose a new path: {output}")
    manifest = verify_data(data_root)
    images, labels = load_arrays(data_root)
    configure_cpu(config)
    training = make_loader(images, labels, manifest["partitions"]["train"], config, shuffle=True)
    validation_ids = manifest["partitions"]["validation"]
    validation = make_loader(images, labels, validation_ids, config)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    started = time.perf_counter()
    try:
        source = source_snapshot(temporary / "source.zip")
        write_json(temporary / "config.json", config.to_dict())
        write_json(temporary / "dataset.json", manifest)
        write_json(temporary / "environment.json", environment_record())
        model = CatalogCNN(dropout=config.dropout)
        initial_state_sha256 = model_state_sha256(model)
        optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
        augmentation_rng = torch.Generator().manual_seed(config.seed + 1)
        history = []
        training_started = time.perf_counter()
        for epoch in range(1, config.epochs + 1):
            model.train()
            loss_total = 0.0
            examples = 0
            for raw, target in training:
                inputs = normalize_pixels(raw)
                inputs = translate_batch(inputs, config.translation_pixels, augmentation_rng)
                optimizer.zero_grad(set_to_none=True)
                loss = nn.functional.cross_entropy(model(inputs), target)
                loss.backward()
                optimizer.step()
                loss_total += loss.item() * len(target)
                examples += len(target)
            validation_report, _, _ = evaluate(model, validation)
            observation = {"epoch": epoch, "train_loss": loss_total / examples,
                           "validation_loss": validation_report["loss"],
                           "validation_accuracy": validation_report["accuracy"],
                           "validation_macro_f1": validation_report["macro_f1"]}
            history.append(observation)
            if telemetry is not None:
                telemetry(observation)
            print(f"Epoch {epoch}/{config.epochs}  loss={observation['train_loss']:.4f}  "
                  f"val_accuracy={observation['validation_accuracy']:.4f}  "
                  f"val_macro_f1={observation['validation_macro_f1']:.4f}", flush=True)
        training_seconds = time.perf_counter() - training_started
        checkpoint = {"schema": 1, "architecture": "catalog-cnn-v1", "class_names": list(CLASS_NAMES),
                      "preprocessing": "uint8-grayscale-28x28-div255-v1", "config": config.to_dict(),
                      "state_sha256": model_state_sha256(model),
                      "state_dict": model.state_dict()}
        torch.save(checkpoint, temporary / "model.pt")
        restored, _ = load_model(temporary / "model.pt")
        metrics, predicted, scores = evaluate(restored, validation)
        first_raw, _ = next(iter(validation))
        first_inputs = normalize_pixels(first_raw)
        with torch.inference_mode():
            torch.testing.assert_close(model.eval()(first_inputs), restored(first_inputs), rtol=0, atol=0)
        write_predictions(temporary / "validation-predictions.csv", validation_ids,
                          labels[validation_ids], predicted, scores)
        write_json(temporary / "history.json", history)
        write_json(temporary / "metrics.json", metrics)
        record = {"schema": 1, "status": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
                  "initialization": "from-scratch", "architecture": "catalog-cnn-v1", "source": source,
                  "config_sha256": json_digest(config.to_dict()), "data_sha256": json_digest(manifest),
                  "split_sha256": manifest["split_sha256"], "model_sha256": sha256(temporary / "model.pt"),
                  "environment_sha256": sha256(temporary / "environment.json"),
                  "validation_predictions_sha256": sha256(temporary / "validation-predictions.csv"),
                  "history_sha256": sha256(temporary / "history.json"),
                  "metrics_sha256": sha256(temporary / "metrics.json"),
                  "validation_macro_f1": metrics["macro_f1"],
                  "validation_accuracy": metrics["accuracy"], "train_count": len(training.dataset),
                  "validation_count": len(validation_ids), "parameters": sum(p.numel() for p in model.parameters()),
                  "initial_state_sha256": initial_state_sha256,
                  "trained_state_sha256": checkpoint["state_sha256"],
                  "training_seconds": training_seconds, "total_seconds": time.perf_counter() - started,
                  "checkpoint_reload_exact": True}
        write_json(temporary / "run.json", record)
        # An empty lock directory reserves the requested name across concurrent writers.
        reservation = output.parent / f".{output.name}.lock"
        reservation.mkdir()
        try:
            if output.exists():
                raise FileExistsError(f"Another process already published {output}")
            temporary.rename(output)
        finally:
            reservation.rmdir()
        return record
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def load_model(path: Path) -> tuple[CatalogCNN, dict]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if checkpoint.get("schema") != 1 or checkpoint.get("architecture") != "catalog-cnn-v1":
        raise ValueError("Unsupported model checkpoint")
    if checkpoint.get("class_names") != list(CLASS_NAMES):
        raise ValueError("Checkpoint class order differs from the expected class order")
    if checkpoint.get("preprocessing") != "uint8-grayscale-28x28-div255-v1":
        raise ValueError("Checkpoint preprocessing contract differs")
    config = TrainingConfig(**checkpoint["config"])
    model = CatalogCNN(dropout=config.dropout)
    model.load_state_dict(checkpoint["state_dict"], strict=True)
    if checkpoint.get("state_sha256") is not None and model_state_sha256(model) != checkpoint["state_sha256"]:
        raise ValueError("Checkpoint weight values differ from the declared model state")
    model.eval()
    return model, checkpoint


def load_run_model(directory: Path, record: dict):
    if record.get("backend") == "sklearn":
        model = joblib.load(directory / "model.joblib")
        if model_state_sha256(model) != record["trained_state_sha256"]:
            raise ValueError("The fitted model differs from the recorded state")
        return model, {"config": read_json(directory / "config.json")}
    return load_model(directory / "model.pt")


def evaluate_run_model(model, checkpoint: dict, images, labels, ids):
    if isinstance(model, BaseEstimator):
        from src.sklearn_model import evaluate_images

        return evaluate_images(model, images[ids], labels[ids])
    config = TrainingConfig(**checkpoint["config"])
    configure_cpu(config)
    return evaluate(model, make_loader(images, labels, ids, config))


def verify_run(path: Path) -> dict:
    record = read_json(path / "run.json")
    if record.get("status") != "complete" or record.get("initialization") != "from-scratch":
        raise ValueError("Run is incomplete or has an unsupported training origin")
    model_file = "model.joblib" if record.get("backend") == "sklearn" else "model.pt"
    checks = {model_file: "model_sha256", "metrics.json": "metrics_sha256",
              "environment.json": "environment_sha256",
              "validation-predictions.csv": "validation_predictions_sha256"}
    if model_file == "model.pt":
        checks["history.json"] = "history_sha256"
    for filename, key in checks.items():
        if sha256(path / filename) != record[key]:
            raise ValueError(f"Run artifact checksum mismatch for {filename}")
    if json_digest(read_json(path / "config.json")) != record["config_sha256"]:
        raise ValueError("Run configuration checksum mismatch")
    if json_digest(read_json(path / "dataset.json")) != record["data_sha256"]:
        raise ValueError("Run dataset identity differs")
    if sha256(path / "source.zip") != record["source"]["archive_sha256"]:
        raise ValueError("Run source archive checksum mismatch")
    file_hashes = record["source"]["file_sha256"]
    if json_digest(file_hashes) != record["source"]["source_sha256"]:
        raise ValueError("Source identity differs from its declared file hashes")
    with zipfile.ZipFile(path / "source.zip") as archive:
        if len(archive.namelist()) != len(file_hashes) or set(archive.namelist()) != set(file_hashes):
            raise ValueError("Source archive files differ from the recorded snapshot")
        for filename, digest in file_hashes.items():
            if bytes_digest(archive.read(filename)) != digest:
                raise ValueError(f"Archived source bytes differ for {filename}")
    return record
