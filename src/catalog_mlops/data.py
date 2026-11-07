"""Verified Fashion-MNIST downloads and stable, disjoint training partitions."""

import gzip
from pathlib import Path
import struct
import tempfile
from urllib.request import urlopen

import numpy as np

from catalog_mlops.artifacts import json_digest, read_json, sha256, write_json


CLASS_NAMES = ("T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal",
               "Shirt", "Sneaker", "Bag", "Ankle boot")
SOURCE = "https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/"
FILES = {
    "train-images-idx3-ubyte.gz": "3aede38d61863908ad78613f6a32ed271626dd12800ba2636569512369268a84",
    "train-labels-idx1-ubyte.gz": "a04f17134ac03560a47e3764e11b92fc97de4d1bfaf8ba1a3aa29af54cc90845",
    "t10k-images-idx3-ubyte.gz": "346e55b948d973a97e58d2351dde16a484bd415d4595297633bb08f03db6a073",
    "t10k-labels-idx1-ubyte.gz": "67da17c76eaffca5446c3361aaab5c3cd6d1c2608764d35dfb1850b086bf8dd5",
}
PARTITIONS = {"train": 1200, "validation": 300, "reference": 100,
              "current": 100, "adaptation": 200, "shift_validation": 200}


def download_file(root: Path, filename: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    target = root / filename
    if target.exists():
        if sha256(target) != FILES[filename]:
            raise ValueError(f"Checksum mismatch for {target}. Remove the damaged file and download again.")
        return target
    with tempfile.NamedTemporaryFile(dir=root, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            with urlopen(SOURCE + filename, timeout=60) as response:
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    stream.write(chunk)
            stream.close()
            if sha256(temporary) != FILES[filename]:
                raise ValueError(f"Downloaded bytes failed checksum for {filename}")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return target


def load_arrays(root: Path, official_test: bool = False) -> tuple[np.ndarray, np.ndarray]:
    prefix = "t10k" if official_test else "train"
    image_raw = gzip.decompress((root / f"{prefix}-images-idx3-ubyte.gz").read_bytes())
    label_raw = gzip.decompress((root / f"{prefix}-labels-idx1-ubyte.gz").read_bytes())
    magic, count, height, width = struct.unpack(">IIII", image_raw[:16])
    label_magic, label_count = struct.unpack(">II", label_raw[:8])
    expected = 10000 if official_test else 60000
    if (magic, count, height, width) != (2051, expected, 28, 28):
        raise ValueError("Unexpected Fashion-MNIST image header")
    if label_magic != 2049 or label_count != count or len(label_raw) != count + 8:
        raise ValueError("Unexpected Fashion-MNIST label header")
    if len(image_raw) != count * 28 * 28 + 16:
        raise ValueError("Unexpected Fashion-MNIST image payload")
    images = np.frombuffer(image_raw, dtype=np.uint8, offset=16).reshape(count, 28, 28)
    labels = np.frombuffer(label_raw, dtype=np.uint8, offset=8)
    if labels.max() > 9:
        raise ValueError("Unknown class identifier")
    return images, labels


def prepare_data(root: Path) -> dict:
    for filename in FILES:
        download_file(root, filename)
    _, labels = load_arrays(root)
    rng = np.random.default_rng(426)
    groups = [rng.permutation(np.flatnonzero(labels == label)) for label in range(10)]
    partitions = {}
    start = 0
    for name, per_class in PARTITIONS.items():
        partitions[name] = np.concatenate([group[start:start + per_class] for group in groups]).tolist()
        start += per_class
    payload = {"name": "fashion-mnist-cpu-v1", "seed": 426, "raw_sha256": FILES,
               "source": SOURCE, "class_names": list(CLASS_NAMES), "partitions": partitions,
               "official_test_policy": "Reserved until candidate selection is recorded"}
    payload["split_sha256"] = json_digest(partitions)
    manifest_path = root / "manifest.json"
    if manifest_path.exists() and read_json(manifest_path) != payload:
        raise ValueError("Existing manifest differs from the declared dataset version")
    write_json(manifest_path, payload)
    return payload


def verify_data(root: Path) -> dict:
    manifest = read_json(root / "manifest.json")
    if manifest["raw_sha256"] != FILES or list(manifest["class_names"]) != list(CLASS_NAMES):
        raise ValueError("Dataset identity or class order differs from the supported snapshot")
    for filename, digest in FILES.items():
        if sha256(root / filename) != digest:
            raise ValueError(f"Checksum mismatch for {filename}")
    partitions = manifest["partitions"]
    if set(partitions) != set(PARTITIONS) or json_digest(partitions) != manifest["split_sha256"]:
        raise ValueError("Split manifest checksum or partition names differ")
    flat = np.concatenate([np.asarray(ids) for ids in partitions.values()])
    if len(np.unique(flat)) != len(flat) or flat.min() < 0 or flat.max() >= 60000:
        raise ValueError("Partitions must contain disjoint official training indices")
    _, labels = load_arrays(root)
    for name, ids in partitions.items():
        if np.asarray(ids).dtype.kind not in "iu":
            raise ValueError("Split indices must be integers")
        if not np.array_equal(np.bincount(labels[ids], minlength=10), np.full(10, PARTITIONS[name])):
            raise ValueError(f"Unexpected class counts for {name}")
    return manifest
