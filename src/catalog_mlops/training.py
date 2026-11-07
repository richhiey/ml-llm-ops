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

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from catalog_mlops.artifacts import bytes_digest, json_digest, read_json, sha256, write_json
from catalog_mlops.data import CLASS_NAMES, load_arrays, verify_data
from catalog_mlops.evaluation import evaluate
from catalog_mlops.model import CatalogCNN, TrainingConfig
from catalog_mlops.preprocessing import normalize_pixels


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
    root = Path(__file__).resolve().parents[2]
    files = sorted((root / "src").rglob("*.py"))
    files += [root / name for name in ("pyproject.toml", "uv.lock", ".python-version")]
    if not all(path.is_file() for path in files):
        raise ValueError("Source checkout and environment lock are required to record reproducible runs")
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in files}


def runtime_source_sha256() -> str:
    return json_digest({name: bytes_digest(content) for name, content in source_files().items()})


def source_snapshot(destination: Path) -> dict:
    root = Path(__file__).resolve().parents[2]
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
    for package in ("torch", "numpy", "scikit-learn", "mlflow", "fastapi", "tensorboard"):
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


def train(data_root: Path, output: Path, config: TrainingConfig, telemetry=None) -> dict:
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
                  "primary_metric": "validation_macro_f1", "validation_macro_f1": metrics["macro_f1"],
                  "validation_accuracy": metrics["accuracy"], "train_count": len(training.dataset),
                  "validation_count": len(validation_ids), "parameters": sum(p.numel() for p in model.parameters()),
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
        raise ValueError("Checkpoint class order differs from the catalog contract")
    if checkpoint.get("preprocessing") != "uint8-grayscale-28x28-div255-v1":
        raise ValueError("Checkpoint preprocessing contract differs")
    config = TrainingConfig(**checkpoint["config"])
    model = CatalogCNN(dropout=config.dropout)
    model.load_state_dict(checkpoint["state_dict"], strict=True)
    model.eval()
    return model, checkpoint


def verify_run(path: Path) -> dict:
    record = read_json(path / "run.json")
    if record.get("status") != "complete" or record.get("initialization") != "from-scratch":
        raise ValueError("Run is incomplete or has an unsupported training origin")
    checks = {"model.pt": "model_sha256", "metrics.json": "metrics_sha256",
              "history.json": "history_sha256",
              "environment.json": "environment_sha256",
              "validation-predictions.csv": "validation_predictions_sha256"}
    for filename, key in checks.items():
        if sha256(path / filename) != record[key]:
            raise ValueError(f"Run artifact checksum mismatch for {filename}")
    if json_digest(read_json(path / "config.json")) != record["config_sha256"]:
        raise ValueError("Run configuration checksum mismatch")
    if json_digest(read_json(path / "dataset.json")) != record["data_sha256"]:
        raise ValueError("Run dataset identity differs")
    if sha256(path / "source.zip") != record["source"]["archive_sha256"]:
        raise ValueError("Run source archive checksum mismatch")
    return record
