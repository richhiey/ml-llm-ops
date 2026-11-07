"""Train one fresh CNN; inspect the weight-update loop in training.py."""
import argparse
import json
from pathlib import Path
from catalog_mlops.artifacts import read_json
from catalog_mlops.model import TrainingConfig
from catalog_mlops.training import train

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = TrainingConfig(**read_json(args.config))
    result = train(args.data, args.output, config)
    print(json.dumps(result, indent=2, allow_nan=False))
