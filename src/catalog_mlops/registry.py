"""Register verified CNN artifacts, record validation and audit alias selection."""

from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import uuid

import mlflow
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException

from catalog_mlops.artifacts import bytes_digest, json_digest
from catalog_mlops.comparison import inspect_tracked_run
from catalog_mlops.inference import Predictor
from catalog_mlops.reproduction import REPLAY_POLICY, verify_reproduction
from catalog_mlops.tracking import tracking_store, tracking_uri
from catalog_mlops.training import model_state_sha256


def registry_client(state: Path) -> MlflowClient:
    uri = tracking_uri(state)
    return MlflowClient(tracking_uri=uri, registry_uri=uri)


def model_name(name: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_-]{1,63}", name):
        raise ValueError(
            "Use a 2–64 character lowercase model name with letters, digits, underscore or hyphen"
        )
    return name


def alias_version(client, name, alias):
    try:
        version = client.get_registered_model(name).aliases.get(alias)
        return str(version) if version is not None else None
    except MlflowException as error:
        if error.error_code != "RESOURCE_DOES_NOT_EXIST":
            raise
        return None


def _append(state: Path, event: dict):
    state.mkdir(parents=True, exist_ok=True)
    event = {"at": datetime.now(timezone.utc).isoformat(), **event}
    descriptor = os.open(
        state / "registry-audit.jsonl", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600
    )
    try:
        content = (json.dumps(event, sort_keys=True, allow_nan=False) + "\n").encode()
        if os.write(descriptor, content) != len(content):
            raise OSError("Incomplete registry audit write")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def mutation(state: Path, action: str, actor: str, reason: str, **details):
    if not actor.strip() or not reason.strip():
        raise ValueError("Record an actor role and reason for every registry mutation")
    state.mkdir(parents=True, exist_ok=True)
    lock = state / ".registry-mutation.lock"
    lock.mkdir()
    operation = {
        "operation_id": uuid.uuid4().hex,
        "action": action,
        "actor": actor,
        "reason": reason,
        **details,
    }
    completed = {}
    try:
        _append(state, {**operation, "status": "requested"})
        yield completed
        _append(state, {**operation, **completed, "status": "completed"})
    except BaseException as error:
        _append(
            state, {**operation, **completed, "status": "failed", "error": str(error)}
        )
        raise
    finally:
        lock.rmdir()


def register_version(
    state: Path, name: str, run_id: str, actor: str, reason: str
) -> dict:
    name = model_name(name)
    with mutation(state, "register", actor, reason, name=name, run_id=run_id) as event:
        with (
            tracking_store(state) as client,
            tempfile.TemporaryDirectory(prefix="registry-recipe-") as temporary,
        ):
            row = inspect_tracked_run(client, run_id, Path(temporary))
            try:
                existing = client.search_model_versions(f"name = '{name}'")
            except MlflowException as error:
                if error.error_code != "RESOURCE_DOES_NOT_EXIST":
                    raise
                existing = []
            matches = [
                v
                for v in existing
                if v.run_id == run_id and v.source == row["model_uri"]
            ]
            if matches:
                version = matches[0]
            else:
                version = mlflow.register_model(row["model_uri"], name)
            event.update(
                version=str(version.version),
                source=version.source,
                reused=bool(matches),
            )
            # A native version can survive an interrupted tag write. Complete its
            # provenance on retry without resetting an existing approval.
            current_tags = client.get_model_version(name, version.version).tags
            initial_tags = {
                "checkpoint_sha256": row["model_sha256"],
                "source_sha256": row["controls"]["source_sha256"],
                "data_sha256": row["controls"]["data_sha256"],
                "split_sha256": row["controls"]["split_sha256"],
            }
            if "validation_status" not in current_tags:
                initial_tags["validation_status"] = "pending"
            for key, value in initial_tags.items():
                if current_tags.get(key) != value:
                    client.set_model_version_tag(name, version.version, key, value)
            return {
                "name": name,
                "version": str(version.version),
                "run_id": run_id,
                "source": version.source,
                "validation_status": client.get_model_version(
                    name, version.version
                ).tags.get("validation_status"),
            }


def validate_version(
    state: Path, name: str, version: str, evidence: Path, actor: str, reason: str
) -> dict:
    name = model_name(name)
    content = evidence.read_bytes()
    report = json.loads(content)
    if report.get("verification_sha256") != json_digest(
        {key: value for key, value in report.items() if key != "verification_sha256"}
    ):
        raise ValueError(
            "Validation report content differs from its verification identity"
        )
    with mutation(
        state,
        "validate",
        actor,
        reason,
        name=name,
        version=str(version),
        evidence_sha256=bytes_digest(content),
    ) as event:
        client = registry_client(state)
        registered = client.get_model_version(name, version)
        if (
            report["original_run_id"] != registered.run_id
            or report.get("policy") != REPLAY_POLICY
        ):
            raise ValueError(
                "Validation report belongs to another run or replay policy"
            )
        inputs = {key: Path(value) for key, value in report["inputs"].items()}
        actual = verify_reproduction(state, registered.run_id, **inputs)
        if actual["status"] != "passed" or report["status"] != "passed":
            raise ValueError("The declared clean replay checks have not passed")
        stable = lambda value: {
            key: item
            for key, item in value.items()
            if key not in {"created_at", "verification_sha256"}
        }
        if stable(actual) != stable(report):
            raise ValueError("Validation evidence changed since the recorded replay")
        if (
            client.get_run(registered.run_id).data.tags["model_uri"]
            != registered.source
        ):
            raise ValueError(
                "Registered source differs from the evaluated native model"
            )
        digest = bytes_digest(content)
        artifact_path = f"registry-validation/{digest}.json"
        with tempfile.TemporaryDirectory(prefix="registry-validation-") as temporary:
            path = Path(temporary) / f"{digest}.json"
            path.write_bytes(content)
            client.log_artifact(registered.run_id, str(path), "registry-validation")
            _verify_retained_evidence(
                client, registered.run_id, digest, Path(temporary) / "readback"
            )
        tags = {
            "validation_scope": REPLAY_POLICY["name"],
            "validation_evidence_sha256": digest,
            "validation_evidence_uri": f"runs:/{registered.run_id}/{artifact_path}",
            "validated_model_sha256": report["original_model_sha256"],
            "validation_status": "passed",
        }
        for key, value in tags.items():
            client.set_model_version_tag(name, version, key, value)
        event.update(
            validation_status="passed", model_sha256=report["original_model_sha256"]
        )
        return {"name": name, "version": str(version), "validation_tags": tags}


def _verify_retained_evidence(client, run_id: str, digest: str, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    retained = Path(
        client.download_artifacts(
            run_id, f"registry-validation/{digest}.json", str(destination)
        )
    )
    if bytes_digest(retained.read_bytes()) != digest:
        raise ValueError("Retained registry validation artifact changed")


def assign_alias(
    state: Path,
    name: str,
    alias: str,
    version: str,
    expected_current: str | None,
    evidence: Path,
    actor: str,
    reason: str,
    rollback: bool = False,
) -> dict:
    name = model_name(name)
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,31}", alias):
        raise ValueError("Use a bounded lowercase alias")
    with mutation(
        state,
        "rollback" if rollback else "assign_alias",
        actor,
        reason,
        name=name,
        alias=alias,
        target_version=str(version),
        expected_current=expected_current,
    ) as event:
        client = registry_client(state)
        before = alias_version(client, name, alias)
        event["previous_version"] = before
        if before != expected_current:
            raise ValueError(
                "Active alias differs from the declared previous version; inspect before changing it"
            )
        target = client.get_model_version(name, version)
        if target.tags.get("validation_status") != "passed":
            raise ValueError(
                "A pending or failed version cannot be selected through this reviewed path"
            )
        if target.tags.get("validation_evidence_sha256") != bytes_digest(
            evidence.read_bytes()
        ):
            raise ValueError(
                "Alias selection needs the target version's retained validation evidence"
            )
        # Recheck the actual model/recipe attribution immediately before selection.
        with tempfile.TemporaryDirectory(prefix="alias-check-") as temporary:
            row = inspect_tracked_run(client, target.run_id, Path(temporary))
            digest = target.tags["validation_evidence_sha256"]
            if (
                target.tags.get("validation_evidence_uri")
                != f"runs:/{target.run_id}/registry-validation/{digest}.json"
            ):
                raise ValueError(
                    "Validation evidence is not connected to this run's retained artifact"
                )
            _verify_retained_evidence(
                client, target.run_id, digest, Path(temporary) / "validation"
            )
        if (
            target.source != row["model_uri"]
            or target.tags.get("validated_model_sha256") != row["model_sha256"]
        ):
            raise ValueError(
                "Validated model identity differs from the registered target"
            )
        if rollback:
            history = read_audit(state)
            if not any(
                r.get("status") == "completed"
                and r.get("action") in {"assign_alias", "rollback"}
                and r.get("name") == name
                and r.get("alias") == alias
                and r.get("target_version") == str(version)
                for r in history
            ):
                raise ValueError(
                    "Rollback target has no retained previous selection evidence"
                )
        client.set_registered_model_alias(name, alias, version)
        after = alias_version(client, name, alias)
        if after != str(version):
            raise ValueError("Alias read-back differs from requested target")
        event.update(
            observed_version=after,
            run_id=target.run_id,
            model_sha256=row["model_sha256"],
        )
        return {
            "name": name,
            "alias": alias,
            "previous_version": before,
            "active_version": after,
            "run_id": target.run_id,
            "model_sha256": row["model_sha256"],
        }


def read_audit(state: Path) -> list[dict]:
    path = state / "registry-audit.jsonl"
    return (
        [json.loads(line) for line in path.read_text().splitlines()]
        if path.exists()
        else []
    )


def audit_status(state: Path, name: str, alias: str) -> dict:
    events = read_audit(state)
    requests = {e["operation_id"] for e in events if e["status"] == "requested"}
    terminal = {
        e["operation_id"] for e in events if e["status"] in {"completed", "failed"}
    }
    changes = [
        e
        for e in events
        if e.get("name") == name
        and e.get("alias") == alias
        and e["status"] == "completed"
        and e["action"] in {"assign_alias", "rollback"}
    ]
    observed = alias_version(registry_client(state), name, alias)
    recorded = changes[-1]["target_version"] if changes else None
    return {
        "name": name,
        "alias": alias,
        "observed_version": observed,
        "last_recorded_version": recorded,
        "state_matches_last_recorded_change": observed == recorded,
        "unresolved_operations": sorted(requests - terminal),
        "events": events,
        "scope": "Local recorded operations; external alias changes and file rewriting require separate evidence",
    }


class RegistryPredictor:
    """Resolve an alias once at startup and retain the model actually loaded."""

    def __init__(self, state: Path, name: str, alias: str = "active"):
        with (
            tracking_store(state) as client,
            tempfile.TemporaryDirectory(prefix="registry-consumer-") as temporary,
        ):
            version = client.get_model_version_by_alias(model_name(name), alias)
            row = inspect_tracked_run(client, version.run_id, Path(temporary))
            if version.source != row["model_uri"]:
                raise ValueError("Registry version and evaluated model URI differ")
            recipe = Path(temporary) / version.run_id / "recipe"
            self.predictor = Predictor(recipe)
            # Resolve the alias once, then load that exact native registry version.
            loaded = mlflow.pytorch.load_model(
                f"models:/{name}/{version.version}", map_location="cpu"
            )
            loaded.eval()
            if (
                model_state_sha256(loaded)
                != self.predictor.record["trained_state_sha256"]
            ):
                raise ValueError(
                    "Registry-loaded weights differ from the evaluated checkpoint"
                )
            self.predictor.model = loaded
        self.identity = {
            **self.predictor.identity,
            "registered_name": name,
            "registered_version": str(version.version),
            "alias_at_startup": alias,
            "source_run_id": version.run_id,
            "model_uri": version.source,
            "validation_status_at_startup": version.tags.get(
                "validation_status", "unknown"
            ),
            "loaded_at": datetime.now(timezone.utc).isoformat(),
        }

    def predict(self, images, image_ids):
        return self.predictor.predict(images, image_ids)
