"""Register one verified MLflow model as a numbered catalog model version."""

import argparse
import json
from pathlib import Path
from src.registry import register_version

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            register_version(
                args.state, args.name, args.run_id, args.actor, args.reason
            ),
            indent=2,
        )
    )
