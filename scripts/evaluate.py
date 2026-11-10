"""Reload saved weights and evaluate on the run's fixed validation images."""
import argparse
import json
from pathlib import Path
from src.data import load_arrays, verify_data
from src.training import evaluate_run_model, load_run_model, runtime_source_sha256, verify_run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    record = verify_run(args.run)
    manifest = verify_data(args.data)
    if record["split_sha256"] != manifest["split_sha256"]:
        raise ValueError("Evaluation split differs from the training run")
    images, labels = load_arrays(args.data)
    model, checkpoint = load_run_model(args.run, record)
    metrics, _, _ = evaluate_run_model(
        model, checkpoint, images, labels, manifest["partitions"]["validation"]
    )
    metrics["evaluation_evidence"] = {
        "model_sha256": record["model_sha256"],
        "training_source_sha256": record["source"]["source_sha256"],
        "evaluation_source_sha256": runtime_source_sha256(),
        "split_sha256": manifest["split_sha256"],
    }
    print(json.dumps(metrics, indent=2, allow_nan=False))
