"""Export a small, unlabeled intake from the separate incoming-image pool."""
import argparse
import json
from pathlib import Path
from src.inference import export_samples

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--partition", default="current")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export_samples(args.data, args.partition, args.count, args.output), indent=2))
