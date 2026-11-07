"""Load the active native registry version once and predict an identified image batch."""

import argparse
import json
from pathlib import Path
import time
from catalog_mlops.inference import deliver_batch
from catalog_mlops.registry import RegistryPredictor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--alias", default="active")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    started = time.perf_counter()
    predictor = RegistryPredictor(args.state, args.name, args.alias)
    report = deliver_batch(predictor, args.manifest, args.output, started)
    summary = {
        key: report[key]
        for key in ("count", "model", "predictions_sha256", "elapsed_seconds")
    }
    summary["output"] = str(args.output)
    print(json.dumps(summary, indent=2, allow_nan=False))
