"""Compare selected MLflow runs against raw retained validation predictions."""
import argparse
import json
from pathlib import Path
from catalog_mlops.artifacts import write_json
from catalog_mlops.comparison import compare_runs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare_runs(args.state, args.baseline, args.runs)
    write_json(args.output, result, overwrite=False)
    print(json.dumps(result, indent=2, allow_nan=False))
