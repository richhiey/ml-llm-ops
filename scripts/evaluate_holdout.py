"""Report official-test quality after the configuration and approved model are fixed."""

import argparse
import json
from pathlib import Path

from src.artifacts import write_json
from src.data import load_arrays, verify_data
from src.registry import RegistryPredictor
from src.training import evaluate_run_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--alias", default="active")
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    consumer = RegistryPredictor(args.state, args.name, args.alias)
    if consumer.identity["validation_status_at_startup"] != "passed":
        raise ValueError("Select the approved model before opening the final holdout")
    manifest = verify_data(args.data)
    images, labels = load_arrays(args.data, official_test=True)
    metrics, _, _ = evaluate_run_model(
        consumer.predictor.model, consumer.predictor.checkpoint, images, labels, list(range(len(images)))
    )
    metrics["evaluation_evidence"] = {
        "model": consumer.identity,
        "cohort": "official-test; report only, configuration already fixed",
        "image_archive_sha256": manifest["raw_sha256"]["t10k-images-idx3-ubyte.gz"],
        "label_archive_sha256": manifest["raw_sha256"]["t10k-labels-idx1-ubyte.gz"],
    }
    write_json(args.output, metrics, overwrite=False)
    print(json.dumps(metrics, indent=2, allow_nan=False))
