"""Check saved-model evaluation and archived-source retraining against the declared policy."""

import argparse
import json
from pathlib import Path
from src.artifacts import write_json
from src.reproduction import verify_reproduction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--retrained", type=Path, required=True)
    parser.add_argument("--saved-evaluation", type=Path, required=True)
    parser.add_argument("--retrained-evaluation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = verify_reproduction(
        args.state,
        args.run_id,
        args.recipe,
        args.retrained,
        args.saved_evaluation,
        args.retrained_evaluation,
    )
    write_json(args.output, report, overwrite=False)
    print(json.dumps(report, indent=2, allow_nan=False))
    raise SystemExit(0 if report["status"] == "passed" else 2)
