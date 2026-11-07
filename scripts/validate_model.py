"""Verify retained clean-replay evidence and tag its registered model version."""

import argparse
import json
from pathlib import Path
from catalog_mlops.registry import validate_version

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            validate_version(
                args.state,
                args.name,
                args.version,
                args.evidence,
                args.actor,
                args.reason,
            ),
            indent=2,
        )
    )
