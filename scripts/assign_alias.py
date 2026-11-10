"""Approve and select a model version, or restore an earlier approved version."""

import argparse
import json
from pathlib import Path
from src.registry import assign_alias, validate_version

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
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument(
        "--approve",
        action="store_true",
        help="Verify and retain the replay report before selecting this version",
    )
    operation.add_argument(
        "--rollback",
        action="store_true",
        help="Restore a version with a prior recorded selection",
    )
    args = parser.parse_args()
    current = None if args.expected_current == "none" else args.expected_current
    if args.approve:
        validate_version(
            args.state, args.name, args.version, args.evidence, args.actor, args.reason
        )
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
