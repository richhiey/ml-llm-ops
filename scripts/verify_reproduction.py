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
    parser.add_argument(
        "--replay", type=Path, help="Folder containing the replay artifacts"
    )
    parser.add_argument("--recipe", type=Path)
    parser.add_argument("--retrained", type=Path)
    parser.add_argument("--saved-evaluation", type=Path)
    parser.add_argument("--retrained-evaluation", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    paths = {
        "recipe": "recipe",
        "retrained": "retrained",
        "saved_evaluation": "saved-evaluation.json",
        "retrained_evaluation": "retrained-evaluation.json",
        "output": "verification.json",
    }
    for argument, filename in paths.items():
        if getattr(args, argument) is None:
            if args.replay is None:
                flag = argument.replace("_", "-")
                parser.error(f"--{flag} is required without --replay")
            setattr(args, argument, args.replay / filename)
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
