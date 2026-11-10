"""Shared model loading and prediction for image batches and HTTP requests."""

import csv
from datetime import datetime, timezone
import io
from pathlib import Path
import shutil
import tempfile
import threading
import time

import numpy as np
from PIL import Image
import torch

from src.artifacts import bytes_digest, sha256, write_json
from src.data import CLASS_NAMES, load_arrays, verify_data
from src.preprocessing import preprocess, validate_intake
from src.sklearn_model import classify
from src.training import load_run_model, runtime_source_sha256, verify_run


def decode_thumbnail(content: bytes, name: str) -> np.ndarray:
    with Image.open(io.BytesIO(content)) as image:
        if image.mode != "L" or image.size != (28, 28):
            raise ValueError(f"Expected a 28x28 grayscale image in mode L: {name}")
        return np.asarray(image).copy()


class Predictor:
    """Pin one verified saved model for the lifetime of a consumer."""

    def __init__(self, run_directory: Path):
        self.run_directory = run_directory.resolve()
        self.record = verify_run(self.run_directory)
        self.model, self.checkpoint = load_run_model(self.run_directory, self.record)
        self.identity = {"local_run": self.run_directory.name,
                         "model_sha256": self.record["model_sha256"],
                         "training_source_sha256": self.record["source"]["source_sha256"],
                         "inference_source_sha256": runtime_source_sha256()}
        self.model_lock = threading.Lock()
        if self.record.get("backend") != "sklearn":
            torch.set_num_threads(self.checkpoint["config"]["cpu_threads"])

    def predict(self, images: np.ndarray, image_ids: list[str]) -> list[dict]:
        if len(image_ids) != len(images) or len(set(image_ids)) != len(image_ids):
            raise ValueError("Every image must have one distinct identifier")
        if any(not isinstance(image_id, str) or not image_id.strip() for image_id in image_ids):
            raise ValueError("Image identifiers must be nonempty strings")
        with self.model_lock:
            if self.record.get("backend") == "sklearn":
                predicted, maximum, _ = classify(self.model, validate_intake(images))
            else:
                inputs = preprocess(images)
                with torch.inference_mode():
                    maximum, predicted = self.model(inputs).softmax(dim=1).max(dim=1)
        return [{"image_id": image_id, "class_id": int(class_id),
                 "class_name": CLASS_NAMES[int(class_id)], "top_score": float(score)}
                for image_id, class_id, score in zip(image_ids, predicted.tolist(), maximum.tolist(), strict=True)]


def read_batch_manifest(path: Path, content: bytes) -> list[dict]:
    with io.StringIO(content.decode("utf-8"), newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["image_id", "path"]:
            raise ValueError("Batch manifest must have exactly the columns image_id,path")
        rows = list(reader)
    if not rows or any(None in row or None in row.values() for row in rows):
        raise ValueError("Batch manifest is empty or contains incomplete rows")
    ids = [row["image_id"] for row in rows]
    if len(set(ids)) != len(ids) or any(not image_id.strip() for image_id in ids):
        raise ValueError("Batch image identifiers must be nonempty and unique")
    for row in rows:
        image_path = Path(row["path"])
        if not image_path.is_absolute():
            image_path = path.parent / image_path
        row["path"] = image_path
    return rows


def predict_batch(run_directory: Path, manifest_path: Path, output: Path) -> dict:
    started = time.perf_counter()
    if output.exists():
        raise FileExistsError(f"Batch output already exists: {output}")
    return deliver_batch(Predictor(run_directory), manifest_path, output, started)


def deliver_batch(predictor, manifest_path: Path, output: Path, started: float | None = None) -> dict:
    """Publish one complete delivery using the model pinned by its consumer."""
    if output.exists():
        raise FileExistsError(f"Batch output already exists: {output}")
    if started is None:
        started = time.perf_counter()
    manifest_bytes = manifest_path.read_bytes()
    rows = read_batch_manifest(manifest_path, manifest_bytes)
    predictions = []
    input_hashes = []
    image_observations = []
    for start in range(0, len(rows), 64):
        chunk = rows[start:start + 64]
        arrays = []
        for row in chunk:
            content = row["path"].read_bytes()
            pixels = decode_thumbnail(content, row["path"].name)
            arrays.append(pixels)
            input_hashes.append({"image_id": row["image_id"], "sha256": bytes_digest(content)})
            image_observations.append({"image_id": row["image_id"],
                                       "mean_brightness": float(pixels.mean() / 255.0)})
        predictions.extend(predictor.predict(np.stack(arrays), [row["image_id"] for row in chunk]))
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        with (temporary / "predictions.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["image_id", "class_id", "class_name", "top_score"])
            writer.writeheader()
            writer.writerows(predictions)
        report = {"created_at": datetime.now(timezone.utc).isoformat(), "count": len(predictions),
                  "model": predictor.identity, "manifest_sha256": bytes_digest(manifest_bytes),
                  "inputs": input_hashes, "predictions_sha256": sha256(temporary / "predictions.csv"),
                  "image_observations": image_observations,
                  "elapsed_seconds": time.perf_counter() - started}
        write_json(temporary / "batch.json", report)
        reservation = output.parent / f".{output.name}.lock"
        reservation.mkdir()
        try:
            if output.exists():
                raise FileExistsError(f"Another process already published {output}")
            temporary.rename(output)
        finally:
            reservation.rmdir()
        return report
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def export_samples(data_root: Path, partition: str, count: int, output: Path) -> dict:
    manifest = verify_data(data_root)
    if partition not in manifest["partitions"] or not 0 < count <= len(manifest["partitions"][partition]):
        raise ValueError("Choose a supported partition and a count within its size")
    images, _ = load_arrays(data_root)
    # Interleave classes so small exports are useful for visual inspection.
    per_class = len(manifest["partitions"][partition]) // 10
    ids = np.asarray(manifest["partitions"][partition]).reshape(10, per_class).T.flatten()[:count]
    if output.exists():
        raise FileExistsError(f"Intake directory already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        with (temporary / "manifest.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["image_id", "path"])
            for image_id in ids:
                filename = f"{int(image_id)}.png"
                Image.fromarray(images[image_id]).save(temporary / filename)
                writer.writerow([f"train:{int(image_id)}", filename])
        reservation = output.parent / f".{output.name}.lock"
        reservation.mkdir()
        try:
            if output.exists():
                raise FileExistsError(f"Another process already published {output}")
            temporary.rename(output)
        finally:
            reservation.rmdir()
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {"partition": partition, "count": count, "manifest": str(output / "manifest.csv")}
