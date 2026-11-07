"""Select an approved model version and record alias readback in the local audit."""

import argparse
import json
from pathlib import Path
from catalog_mlops.registry import assign_alias

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--alias", default="active")
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--expected-current",
        required=True,
        help="Current version, or none for an unassigned alias",
    )
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    current = None if args.expected_current == "none" else args.expected_current
    result = assign_alias(
        args.state,
        args.name,
        args.alias,
        args.version,
        current,
        args.evidence,
        args.actor,
        args.reason,
        rollback=args.rollback,
    )
    print(json.dumps(result, indent=2))
