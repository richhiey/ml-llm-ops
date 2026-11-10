"""Run an explicit training recipe with an MLflow tracking adapter."""
import argparse
import json
from pathlib import Path
from src.training import read_training_config
from src.tracking import DEFAULT_EXPERIMENT, tracked_train

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--experiment", default=DEFAULT_EXPERIMENT)
    parser.add_argument("--autolog", action="store_true")
    args = parser.parse_args()
    result = tracked_train(args.data, args.output, read_training_config(args.config),
                           args.state, args.name, autolog=args.autolog, experiment=args.experiment)
    print(json.dumps(result, indent=2, allow_nan=False))
