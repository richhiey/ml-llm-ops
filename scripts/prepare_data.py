"""Load Fashion-MNIST with TorchVision and record the fixed CPU partitions."""
import argparse
import json
from pathlib import Path
from src.data import prepare_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    args = parser.parse_args()
    manifest = prepare_data(args.data)
    print(json.dumps({"name": manifest["name"], "split_sha256": manifest["split_sha256"],
                      "counts": {key: len(ids) for key, ids in manifest["partitions"].items()}}, indent=2))
