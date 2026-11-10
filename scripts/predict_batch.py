"""Score an image manifest with a saved run or a registered model."""

import argparse
import json
from pathlib import Path
import time

from src.inference import deliver_batch, predict_batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    model = parser.add_mutually_exclusive_group(required=True)
    model.add_argument("--run", type=Path, help="Saved run directory")
    model.add_argument("--name", help="Registered model name")
    parser.add_argument("--state", type=Path, help="MLflow state directory (default: work/mlflow)")
    parser.add_argument("--alias", help="Registered model alias (default: active)")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--report-errors", action="store_true",
        help="Write results.csv with a prediction or input error for every manifest row.",
    )
    args = parser.parse_args()
    if args.run is not None:
        if args.state is not None or args.alias is not None:
            parser.error("--state and --alias require --name")
        report = predict_batch(
            args.run, args.manifest, args.output, report_errors=args.report_errors
        )
    else:
        from src.registry import RegistryPredictor

        if args.output.exists():
            raise FileExistsError(args.output)
        started = time.perf_counter()
        predictor = RegistryPredictor(
            args.state or Path("work/mlflow"), args.name, args.alias or "active"
        )
        receipt = deliver_batch(
            predictor, args.manifest, args.output, started, report_errors=args.report_errors
        )
        result_fields = ("predictions_sha256",)
        if args.report_errors:
            result_fields = ("results_sha256", "prediction_count", "error_count")
        report = {
            key: receipt[key] for key in ("count", "model", *result_fields, "elapsed_seconds")
        }
        report["output"] = str(args.output)
    print(json.dumps(report, indent=2, allow_nan=False))
