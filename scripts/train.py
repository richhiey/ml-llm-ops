"""Fit one model from its configuration and retain the run artifacts."""
import argparse
import json
from pathlib import Path
from src.training import read_training_config
from src.training import train

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = read_training_config(args.config)
    result = train(args.data, args.output, config)
    print(json.dumps(result, indent=2, allow_nan=False))
