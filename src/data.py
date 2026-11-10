"""Load Fashion-MNIST with TorchVision and verify the fixed course split."""

from hashlib import sha256
from pathlib import Path

import numpy as np
from torchvision.datasets import FashionMNIST

from src.artifacts import json_digest, read_json, write_json


CLASS_NAMES = ("T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal",
               "Shirt", "Sneaker", "Bag", "Ankle boot")
SOURCE = "https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/"
FILES = {
    "train-images-idx3-ubyte.gz": "3aede38d61863908ad78613f6a32ed271626dd12800ba2636569512369268a84",
    "train-labels-idx1-ubyte.gz": "a04f17134ac03560a47e3764e11b92fc97de4d1bfaf8ba1a3aa29af54cc90845",
    "t10k-images-idx3-ubyte.gz": "346e55b948d973a97e58d2351dde16a484bd415d4595297633bb08f03db6a073",
    "t10k-labels-idx1-ubyte.gz": "67da17c76eaffca5446c3361aaab5c3cd6d1c2608764d35dfb1850b086bf8dd5",
}
# Verify the decoded pixels and labels that TorchVision actually serves, in row order.
ARRAY_SHA256 = {
    "train": (
        "2e487a6c89124f78f2d7521542223cafe96f7123c3ca13d447772ac6ecbb3012",
        "657fbd221bfc9f4198cc14b5619cc33ec57c58dd0e47af4d99d6650759e869a7",
    ),
    "test": (
        "c867c93ff95360594e8ec3287995350b824dd110b11595c0e13d5423f621867a",
        "3d0e6c6ea990b53b6f8f500a41cac93881d981b315f84578b7d915342ade01e9",
    ),
}
PARTITIONS = {"train": 1200, "validation": 300, "reference": 100,
              "current": 100, "adaptation": 200, "shift_validation": 200}


def load_arrays(root: Path, official_test: bool = False) -> tuple[np.ndarray, np.ndarray]:
    dataset = FashionMNIST(root=root, train=not official_test, download=True)
    images = dataset.data.numpy()
    labels = dataset.targets.numpy().astype(np.uint8)
    expected = 10000 if official_test else 60000
    if images.shape != (expected, 28, 28) or images.dtype != np.uint8 or labels.shape != (expected,):
        raise ValueError("Unexpected Fashion-MNIST image or label format")
    split = "test" if official_test else "train"
    if (sha256(images).hexdigest(), sha256(labels).hexdigest()) != ARRAY_SHA256[split]:
        raise ValueError(f"Fashion-MNIST {split} data differs from the verified snapshot")
    return images, labels


def prepare_data(root: Path) -> dict:
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
