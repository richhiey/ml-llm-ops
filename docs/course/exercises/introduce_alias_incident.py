"""Construct a real mistaken native alias assignment for the rollback exercise.

This course fixture intentionally bypasses the reviewed application selection
path. It is not an application feature or an actual retailer incident.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import mlflow
from mlflow import MlflowClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--bad-run-id", required=True)
    parser.add_argument("--expected-approved", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    uri = "sqlite:///" + (args.state.resolve() / "tracking.db").as_posix()
    mlflow.set_tracking_uri(uri)
    mlflow.set_registry_uri(uri)
    client = MlflowClient()
    before = client.get_model_version_by_alias(args.name, "active")
    if (
        str(before.version) != args.expected_approved
        or before.tags.get("validation_status") != "passed"
    ):
        raise ValueError("Start with the expected approved version selected")
    run = client.get_run(args.bad_run_id)
    if (
        run.info.status != "FINISHED"
        or run.data.tags.get("pipeline_status") != "complete"
    ):
        raise ValueError("Use a real completed candidate experiment")
    if run.info.run_id == before.run_id:
        raise ValueError("The incident candidate must differ from the approved model")
    audit = args.state / "registry-audit.jsonl"
    audit_before = hashlib.sha256(audit.read_bytes()).hexdigest()
    version = mlflow.register_model(run.data.tags["model_uri"], args.name)
    client.set_model_version_tag(
        args.name, version.version, "validation_status", "pending"
    )
    client.set_model_version_tag(
        args.name,
        version.version,
        "exercise_incident",
        "bypassed-reviewed-alias-selection",
    )
    client.set_registered_model_alias(args.name, "active", version.version)
    after = client.get_model_version_by_alias(args.name, "active")
    audit_after = hashlib.sha256(audit.read_bytes()).hexdigest()
    assert str(after.version) == str(version.version) and audit_before == audit_after
    report = {
        "kind": "constructed native alias incident",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "name": args.name,
        "alias": "active",
        "previous_approved_version": str(before.version),
        "previous_run_id": before.run_id,
        "active_bad_version": str(after.version),
        "bad_run_id": after.run_id,
        "bad_model_sha256": run.data.tags["checkpoint_sha256"],
        "validation_status": after.tags["validation_status"],
        "local_audit_sha256_before": audit_before,
        "local_audit_sha256_after": audit_after,
        "scope": "This separate fixture records the native change. The application local audit did not capture it.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps(report, indent=2))
