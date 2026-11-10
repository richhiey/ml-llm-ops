"""Starter for registering one evaluated image classifier.

Copy this file to scripts/release_model.py and complete release().
"""

import argparse
import json
from pathlib import Path

from src.artifacts import json_digest, read_json, write_json
from src.registry import register_version
from src.tracking import tracked_train
from src.training import read_training_config


def release(settings: dict, work: Path, actor: str) -> dict:
    state = work / "mlflow"
    output = work / "trained"
    training_config = read_training_config(Path(settings["training_config"]))

    # Use tracked_train to train, evaluate and log this configuration.
    # Use the returned run ID to register its native logged model.
    # Return run_id, model_uri, registered_name and registered_version.
    raise NotImplementedError("Connect tracking and registration")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    args = parser.parse_args()
    settings = read_json(args.config)
    if settings["inference_mode"] not in {"batch", "real-time"}:
        raise ValueError("Choose batch or real-time for inference_mode")
    path = args.work / "release.json"
    if path.exists():
        raise FileExistsError(f"Choose a new work directory: {args.work}")
    result = {
        **release(settings, args.work, args.actor),
        "inference_mode": settings["inference_mode"],
        "project_config_sha256": json_digest(settings),
    }
    write_json(path, result, overwrite=False)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
