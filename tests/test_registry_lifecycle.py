"""Native lifecycle behavior on tiny explicitly synthetic mechanics data."""

from dataclasses import replace
from pathlib import Path
import shutil

import mlflow
import numpy as np
import pytest
from fastapi.testclient import TestClient

from src import tracking, training
from src.artifacts import read_json, sha256, write_json
from src.evaluation import evaluate
from src.model import TrainingConfig
from src.registry import (
    RegistryPredictor,
    assign_alias,
    audit_status,
    register_version,
    registry_client,
    validate_version,
)
from src.reproduction import verify_reproduction
from src.service import create_prediction_app


@pytest.fixture(scope="module")
def lifecycle(tmp_path_factory):
    root = tmp_path_factory.mktemp("native-registry")
    rng = np.random.default_rng(24)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.tile(np.arange(10, dtype=np.uint8), 4)
    manifest = {
        "name": "synthetic-registry-fixture",
        "split_sha256": "mechanics-split",
        "partitions": {"train": list(range(20)), "validation": list(range(20, 40))},
    }
    patch = pytest.MonkeyPatch()
    for module in (training, tracking):
        patch.setattr(module, "verify_data", lambda _: manifest)
        patch.setattr(module, "load_arrays", lambda _: (images, labels))
    try:
        config = TrainingConfig(epochs=1, batch_size=10, cpu_threads=1)
        receipt = tracking.tracked_train(
            root, root / "original", config, root / "state", "original"
        )
        bad = tracking.tracked_train(
            root, root / "bad", replace(config, epochs=2), root / "state", "other"
        )
        training.train(root, root / "retrained", config)
        for directory, destination in [
            (root / "original", root / "saved-evaluation.json"),
            (root / "retrained", root / "retrained-evaluation.json"),
        ]:
            model, _ = training.load_model(directory / "model.pt")
            loader = training.make_loader(
                images, labels, manifest["partitions"]["validation"], config
            )
            metrics, _, _ = evaluate(model, loader)
            record = training.verify_run(directory)
            metrics["evaluation_evidence"] = {
                "model_sha256": record["model_sha256"],
                "split_sha256": manifest["split_sha256"],
                "evaluation_source_sha256": training.runtime_source_sha256(),
            }
            write_json(destination, metrics)
        inputs = dict(
            recipe=root / "original",
            retrained=root / "retrained",
            saved_evaluation=root / "saved-evaluation.json",
            retrained_evaluation=root / "retrained-evaluation.json",
        )
        report = verify_reproduction(root / "state", receipt["run_id"], **inputs)
        assert report["status"] == "passed"
        evidence = root / "replay.json"
        write_json(evidence, report)
        yield root, receipt, bad, evidence, inputs, images
    finally:
        patch.undo()


def test_pending_refusal_native_incident_rollback_and_pinned_consumers(lifecycle):
    root, original, bad, evidence, _, images = lifecycle
    state, name = root / "state", "catalog-mechanics"
    before_uris = mlflow.get_tracking_uri(), mlflow.get_registry_uri()
    first = register_version(
        state, name, original["run_id"], "catalog-engineer", "Retain evaluated model"
    )
    assert first["validation_status"] == "pending"
    assert (
        register_version(
            state,
            name,
            original["run_id"],
            "catalog-engineer",
            "Inspect existing version",
        )["version"]
        == first["version"]
    )
    with pytest.raises(ValueError, match="pending"):
        assign_alias(
            state,
            name,
            "active",
            first["version"],
            None,
            evidence,
            "catalog-engineer",
            "Premature selection",
        )
    validated = validate_version(
        state,
        name,
        first["version"],
        evidence,
        "catalog-engineer",
        "Check clean replay",
    )
    assert validated["validation_tags"]["validation_status"] == "passed"
    assign_alias(
        state,
        name,
        "active",
        first["version"],
        None,
        evidence,
        "catalog-engineer",
        "Select approved recipe",
    )
    pinned_good = RegistryPredictor(state, name)
    second = register_version(
        state, name, bad["run_id"], "catalog-engineer", "Retain other recipe for review"
    )
    client = registry_client(state)
    # Actual native assignment deliberately bypasses the reviewed path.
    client.set_registered_model_alias(name, "active", second["version"])
    assert not audit_status(state, name, "active")["state_matches_last_recorded_change"]
    pinned_bad = RegistryPredictor(state, name)
    assert pinned_bad.identity["validation_status_at_startup"] == "pending"
    with pytest.raises(ValueError, match="differs from the declared previous"):
        assign_alias(
            state,
            name,
            "active",
            first["version"],
            first["version"],
            evidence,
            "catalog-engineer",
            "Stale state",
            rollback=True,
        )
    changed = assign_alias(
        state,
        name,
        "active",
        first["version"],
        second["version"],
        evidence,
        "catalog-engineer",
        "Restore previously approved model",
        rollback=True,
    )
    fresh = RegistryPredictor(state, name)
    assert changed["previous_version"] == second["version"]
    assert (
        fresh.identity["source_run_id"]
        == original["run_id"]
        == pinned_good.identity["source_run_id"]
    )
    assert fresh.identity["model_sha256"] != pinned_bad.identity["model_sha256"]
    with (
        TestClient(create_prediction_app(pinned_bad)) as old_client,
        TestClient(create_prediction_app(fresh)) as fresh_client,
    ):
        assert (
            old_client.get("/health").json()["model"]["registered_version"]
            == second["version"]
        )
        assert (
            fresh_client.get("/health").json()["model"]["registered_version"]
            == first["version"]
        )
        response = fresh_client.post(
            "/predict", json={"image_id": "probe", "pixels": images[0].tolist()}
        )
        assert response.status_code == 200
    audit = audit_status(state, name, "active")
    assert (
        audit["state_matches_last_recorded_change"]
        and not audit["unresolved_operations"]
    )
    rollback = [
        e
        for e in audit["events"]
        if e["action"] == "rollback" and e["status"] == "completed"
    ][-1]
    assert (
        rollback["previous_version"] == second["version"]
        and rollback["observed_version"] == first["version"]
    )
    assert (
        rollback["actor"] == "catalog-engineer"
        and rollback["reason"] == "Restore previously approved model"
    )
    assert (mlflow.get_tracking_uri(), mlflow.get_registry_uri()) == before_uris


def test_replay_reports_environment_mismatch_and_rejects_changed_raw_result(
    lifecycle, tmp_path
):
    root, original, _, _, inputs, _ = lifecycle
    copied = tmp_path / "repeat"
    shutil.copytree(inputs["retrained"], copied)
    environment = read_json(copied / "environment.json")
    environment["platform"] = "different-platform"
    write_json(copied / "environment.json", environment)
    record = read_json(copied / "run.json")
    record["environment_sha256"] = sha256(copied / "environment.json")
    write_json(copied / "run.json", record)
    result = verify_reproduction(
        root / "state", original["run_id"], **{**inputs, "retrained": copied}
    )
    assert result["status"] == "failed" and not result["checks"]["environment"]
    altered = read_json(inputs["retrained_evaluation"])
    altered["macro_f1"] += 0.01
    write_json(tmp_path / "altered.json", altered)
    result = verify_reproduction(
        root / "state",
        original["run_id"],
        **{**inputs, "retrained_evaluation": tmp_path / "altered.json"},
    )
    assert (
        result["status"] == "failed" and not result["checks"]["retrained_raw_metrics"]
    )
    with pytest.raises(ValueError, match="checksum mismatch"):
        (copied / "source.zip").write_bytes(b"changed archive")
        verify_reproduction(
            root / "state", original["run_id"], **{**inputs, "retrained": copied}
        )


def test_copying_original_artifacts_is_not_an_independent_training_replay(
    lifecycle, tmp_path
):
    root, original, _, _, inputs, _ = lifecycle
    copied = tmp_path / "copied-original"
    shutil.copytree(inputs["recipe"], copied)
    report = verify_reproduction(
        root / "state",
        original["run_id"],
        **{
            **inputs,
            "retrained": copied,
            "retrained_evaluation": inputs["saved_evaluation"],
        },
    )
    assert report["status"] == "failed"
    assert not report["checks"]["distinct_training_record"]
    assert not report["checks"]["separate_evaluation_files"]
    # Exact learned weights are allowed when the run and evaluation were separate.
    actual = verify_reproduction(root / "state", original["run_id"], **inputs)
    assert actual["status"] == "passed" and actual["retrained_state_exact"]


def test_registration_retry_completes_tags_and_preserves_passed_validation(
    lifecycle, monkeypatch
):
    from mlflow import MlflowClient

    root, original, _, evidence, _, _ = lifecycle
    state, name = root / "state", "catalog-tag-recovery"
    set_tag = MlflowClient.set_model_version_tag
    interrupted = False

    def fail_one_tag(client, model_name, version, key, value):
        nonlocal interrupted
        if model_name == name and key == "source_sha256" and not interrupted:
            interrupted = True
            raise RuntimeError("simulated interrupted tag write")
        return set_tag(client, model_name, version, key, value)

    with monkeypatch.context() as patch:
        patch.setattr(MlflowClient, "set_model_version_tag", fail_one_tag)
        with pytest.raises(RuntimeError, match="interrupted tag"):
            register_version(
                state,
                name,
                original["run_id"],
                "catalog-engineer",
                "First registration",
            )
    client = registry_client(state)
    versions = client.search_model_versions(f"name = '{name}'")
    assert len(versions) == 1 and "validation_status" not in versions[0].tags
    result = register_version(
        state,
        name,
        original["run_id"],
        "catalog-engineer",
        "Finish interrupted registration",
    )
    assert (
        result["version"] == str(versions[0].version)
        and result["validation_status"] == "pending"
    )
    tags = client.get_model_version(name, result["version"]).tags
    assert all(
        key in tags
        for key in ["checkpoint_sha256", "source_sha256", "data_sha256", "split_sha256"]
    )
    validate_version(
        state, name, result["version"], evidence, "catalog-engineer", "Verify replay"
    )
    assert (
        register_version(
            state,
            name,
            original["run_id"],
            "catalog-engineer",
            "Inspect approved version",
        )["validation_status"]
        == "passed"
    )
    audit = audit_status(state, name, "active")
    failed = [
        e for e in audit["events"] if e["name"] == name and e["status"] == "failed"
    ][0]
    assert failed["version"] == result["version"]


def test_ui_registered_version_can_be_approved_and_loaded(lifecycle):
    root, original, other, evidence, _, _ = lifecycle
    state, name = root / "state", "catalog-ui-registration"
    client = registry_client(state)
    client.create_registered_model(name)
    source = client.get_logged_model(original["model_uri"].removeprefix("models:/"))
    other_source = client.get_logged_model(other["model_uri"].removeprefix("models:/"))
    # The Register model dialog submits an artifact location and a source run ID.
    good = client.create_model_version(
        name, source.artifact_location, original["run_id"]
    )
    wrong = client.create_model_version(
        name, other_source.artifact_location, original["run_id"]
    )
    with pytest.raises(ValueError, match="Registered source differs"):
        validate_version(state, name, wrong.version, evidence, "engineer", "Check replay")

    validate_version(state, name, good.version, evidence, "engineer", "Check replay")
    assign_alias(state, name, "active", good.version, None, evidence, "engineer", "Select fit")
    predictor = RegistryPredictor(state, name)
    assert predictor.identity["model_uri"] == original["model_uri"]
    assert predictor.identity["registered_version"] == str(good.version)
    reused = register_version(state, name, original["run_id"], "engineer", "Reuse fit")
    assert reused["version"] == str(good.version)


def test_alias_selection_checks_retrievable_validation_artifact(lifecycle, tmp_path):
    root, original, _, evidence, _, _ = lifecycle
    state, name = root / "state", "catalog-evidence-retention"
    version = register_version(
        state, name, original["run_id"], "catalog-engineer", "Retain model"
    )["version"]
    approved = validate_version(
        state, name, version, evidence, "catalog-engineer", "Retain replay evidence"
    )
    tags = approved["validation_tags"]
    client = registry_client(state)
    destination = tmp_path / "retained"
    destination.mkdir()
    artifact = f"registry-validation/{tags['validation_evidence_sha256']}.json"
    retained = Path(
        client.download_artifacts(original["run_id"], artifact, str(destination))
    )
    assert retained.read_bytes() == evidence.read_bytes()
    changed = tmp_path / retained.name
    changed.write_bytes(b"changed validation report")
    client.log_artifact(original["run_id"], str(changed), "registry-validation")
    try:
        with pytest.raises(ValueError, match="validation artifact changed"):
            assign_alias(
                state,
                name,
                "active",
                version,
                None,
                evidence,
                "catalog-engineer",
                "Reject overwritten evidence",
            )
    finally:
        changed.write_bytes(evidence.read_bytes())
        client.log_artifact(original["run_id"], str(changed), "registry-validation")


def test_final_holdout_stays_closed_for_a_pending_active_model(lifecycle, tmp_path):
    import subprocess
    import sys

    root, original, _, _, _, _ = lifecycle
    state, name = root / "state", "catalog-holdout-guard"
    version = register_version(
        state, name, original["run_id"], "catalog-engineer", "Pending review"
    )["version"]
    registry_client(state).set_registered_model_alias(name, "active", version)
    repo = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_holdout.py",
            "--state",
            str(state),
            "--name",
            name,
            "--data",
            str(tmp_path / "unavailable-data"),
            "--output",
            str(tmp_path / "holdout.json"),
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0
    assert "Select the approved model before opening the final holdout" in result.stderr
    assert "FileNotFoundError" not in result.stderr
    assert not (tmp_path / "holdout.json").exists()
