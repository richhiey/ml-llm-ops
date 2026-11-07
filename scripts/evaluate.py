"""Reload saved weights and evaluate on the run's fixed validation images."""
import argparse
import json
from pathlib import Path
from catalog_mlops.data import load_arrays, verify_data
from catalog_mlops.evaluation import evaluate
from catalog_mlops.model import TrainingConfig
from catalog_mlops.training import configure_cpu, load_model, make_loader, runtime_source_sha256, verify_run

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
    model, checkpoint = load_model(args.run / "model.pt")
    config = TrainingConfig(**checkpoint["config"])
    configure_cpu(config)
    validation = make_loader(images, labels, manifest["partitions"]["validation"], config)
    metrics, _, _ = evaluate(model, validation)
    metrics["evaluation_evidence"] = {
        "model_sha256": record["model_sha256"],
        "training_source_sha256": record["source"]["source_sha256"],
        "evaluation_source_sha256": runtime_source_sha256(),
        "split_sha256": manifest["split_sha256"],
    }
    print(json.dumps(metrics, indent=2, allow_nan=False))
