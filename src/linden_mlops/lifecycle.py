"""Local single-user lifecycle: explicit evidence, modern aliases and replay."""
from dataclasses import asdict
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import math
import platform
import re
import importlib.metadata
import json
import subprocess
import sys
import tarfile
import time
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from mlflow.models import infer_signature
from .pipeline import Config, DATA, FEATURES, TARGET, sha256, preprocess, run_pipeline, ingest, evaluate

MODEL_NAME = "dev.linden-demand"
TOLERANCE = 1e-6
ROOT = Path(__file__).resolve().parents[2]


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_files():
    return sorted([ROOT / "pyproject.toml", ROOT / "uv.lock", *ROOT.glob("src/linden_mlops/**/*.py"), *ROOT.glob("src/linden_mlops/data/*")])


def code_revision():
    digest = hashlib.sha256()
    for file in source_files():
        digest.update(str(file.relative_to(ROOT)).encode())
        digest.update(file.read_bytes())
    return "sha256:" + digest.hexdigest()


def environment():
    return {"python": ".".join(map(str, sys.version_info[:3])),
            "system": platform.system(), "machine": platform.machine(),
            "packages": dict(sorted((re.sub(r"[-_.]+", "-", d.metadata["Name"]).lower(), d.version)
                                    for d in importlib.metadata.distributions())),
            "lock_sha256": sha256(ROOT / "uv.lock")}


class Workspace:
    """New path = clean SQLite store and local artifacts. Existing paths are never deleted."""
    def __init__(self, path="state"):
        self.path = Path(path).resolve()
        self.path.mkdir(parents=True, exist_ok=True)
        self.uri = "sqlite:///" + str(self.path / "mlflow.db")
        mlflow.set_tracking_uri(self.uri)
        mlflow.set_registry_uri(self.uri)
        self.client = MlflowClient(tracking_uri=self.uri, registry_uri=self.uri)
        experiment = self.client.get_experiment_by_name("linden-demand")
        self.experiment_id = experiment.experiment_id if experiment else self.client.create_experiment(
            "linden-demand", artifact_location=(self.path / "artifacts").as_uri())

    def connect(self):
        mlflow.set_tracking_uri(self.uri)
        mlflow.set_registry_uri(self.uri)

    def run(self, config=Config(), name="baseline", partition="validation"):
        self.connect()
        mlflow.sklearn.autolog(disable=not config.autolog, log_models=False, silent=True)
        try:
            with mlflow.start_run(experiment_id=self.experiment_id, run_name=name) as run:
                model, metrics, frame = run_pipeline(config, partition=partition)
                mlflow.log_params({**asdict(config), "evaluation_partition": partition,
                                   "data_sha256": sha256(DATA / "demand-v1.csv"), "code_revision": code_revision()})
                mlflow.log_metrics(metrics)
                sample = frame.loc[frame.partition == partition, FEATURES].iloc[:2]
                info = mlflow.sklearn.log_model(model, name="model", signature=infer_signature(sample, model.predict(sample)),
                                               input_example=sample, pip_requirements=["scikit-learn==1.7.2", "numpy==2.3.3", "pandas==2.3.3"])
                evidence_dir = self.path / "evidence" / run.info.run_id
                evidence_dir.mkdir(parents=True)
                manifest = {"run_id": run.info.run_id, "config": asdict(config), "metrics": metrics,
                            "evaluation_partition": partition, "code_revision": code_revision(),
                            "data_sha256": sha256(DATA / "demand-v1.csv"), "environment": environment(),
                            "model_uri": info.model_uri, "tolerance_rmse_kwh": TOLERANCE,
                            "command": f"uv run linden-mlops train --state fresh-state --alpha {config.alpha}" +
                                       (" --range-guard" if config.range_guard else "") +
                                       (" --autolog" if config.autolog else "") + f" --partition {partition}"}
                write_json(evidence_dir / "manifest.json", manifest)
                write_json(evidence_dir / "config.json", asdict(config))
                (evidence_dir / "environment.txt").write_text("\n".join(sorted(f"{d.metadata['Name']}=={d.version}" for d in importlib.metadata.distributions())) + "\n")
                with tarfile.open(evidence_dir / "source.tar.gz", "w:gz") as bundle:
                    for file in sorted(set(source_files() + [ROOT / "README.md", ROOT / ".gitignore", ROOT / ".gitattributes"] + list(ROOT.glob("configs/*.json")) + list(ROOT.glob("tests/*.py")) + list(ROOT.glob("docs/*.md")) + list(ROOT.glob("examples/*.py")))):
                        bundle.add(file, arcname=str(file.relative_to(ROOT)))
                mlflow.log_artifacts(str(evidence_dir), artifact_path="reproduction")
                mlflow.set_tags({"primary_metric": "rmse_kwh", "model_uri": info.model_uri,
                                 "comparison_group": "demand-v1-validation" if partition == "validation" else "final-holdout"})
        finally:
            mlflow.sklearn.autolog(disable=True)
        return manifest


def run_matrix(workspace, range_guard=True, autolog=False):
    return [workspace.run(Config(alpha=a, range_guard=range_guard, autolog=autolog), name=f"alpha-{a}")
            for a in [0.01, 0.1, 1.0, 10.0, 100.0]]


def export_runs(workspace):
    rows = []
    for run in workspace.client.search_runs([workspace.experiment_id], max_results=1000):
        if run.info.status == "FINISHED":
            rows.append({"run_id": run.info.run_id, **run.data.params, **run.data.metrics,
                         "comparison_group": run.data.tags.get("comparison_group")})
    return pd.DataFrame(rows)


def register(workspace, run_id):
    workspace.connect()
    run = workspace.client.get_run(run_id)
    version = mlflow.register_model(run.data.tags["model_uri"], MODEL_NAME)
    workspace.client.set_model_version_tag(MODEL_NAME, version.version, "validation_status", "pending")
    return str(version.version)


def approve(workspace, version, evidence):
    """Policy checks metric/lineage; caller supplies human-readable validation rationale."""
    mv = workspace.client.get_model_version(MODEL_NAME, str(version))
    run = workspace.client.get_run(mv.run_id)
    score = run.data.metrics.get("rmse_kwh", float("nan"))
    if (not evidence.strip() or not math.isfinite(score) or score > 5
            or run.data.params.get("range_guard") != "True"
            or run.data.params.get("evaluation_partition") != "validation"):
        raise ValueError("Approval needs rationale, range_guard=True and finite validation RMSE <= 5 kWh")
    workspace.client.set_model_version_tag(MODEL_NAME, str(version), "validation_evidence", evidence)
    workspace.client.set_model_version_tag(MODEL_NAME, str(version), "validation_status", "approved")


def activate(workspace, version, reason):
    if not reason.strip():
        raise ValueError("Alias change needs a reason")
    version = str(version)
    mv = workspace.client.get_model_version(MODEL_NAME, version)
    if mv.tags.get("validation_status") != "approved":
        raise ValueError("Only approved versions may be active")
    previous = workspace.client.get_registered_model(MODEL_NAME).aliases.get("active")
    previous = str(previous) if previous is not None else None
    event = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "model": MODEL_NAME,
             "alias": "active", "previous_version": previous, "new_version": version,
             "run_id": mv.run_id, "reason": reason}
    workspace.client.set_registered_model_alias(MODEL_NAME, "active", version)
    # Single-user application event log; no claim of atomicity/tamper-proof audit.
    with (workspace.path / "audit.jsonl").open("a") as file:
        file.write(json.dumps(event) + "\n")
    workspace.client.log_dict(mv.run_id, event, f"audit/{time.time_ns()}.json")
    return event


def batch_predict(workspace, input_path=None, output_name="batch"):
    """Resolve alias once and pin its version for this job; measure end-to-end completion."""
    workspace.connect()
    start = time.perf_counter()
    mv = workspace.client.get_model_version_by_alias(MODEL_NAME, "active")
    run = workspace.client.get_run(mv.run_id)
    config = Config(alpha=float(run.data.params["alpha"]), range_guard=run.data.params["range_guard"] == "True")
    inputs = pd.read_csv(input_path or DATA / "batch-v1.csv")
    if "row_id" not in inputs or inputs.row_id.duplicated().any() or inputs.row_id.isna().any():
        raise ValueError("Batch needs unique complete row_id values")
    features = preprocess(inputs, config)
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/{mv.version}")
    output = inputs[["row_id"]].copy()
    output["prediction_kwh"] = model.predict(features)
    output.to_csv(workspace.path / f"{output_name}.csv", index=False)
    seconds = time.perf_counter() - start
    evidence = {"resolved_version": str(mv.version), "run_id": mv.run_id, "model": MODEL_NAME,
                "rows": len(output), "elapsed_seconds": seconds, "rows_per_second": len(output) / seconds,
                "complete_within_60s": seconds <= 60, "input_sha256": sha256(input_path or DATA / "batch-v1.csv")}
    write_json(workspace.path / f"{output_name}.json", evidence)
    return output, evidence


def reproduce(workspace, run_id, destination):
    """Fail before rerun if loaded source/data/lock/runtime differ; compare like metrics."""
    local = Path(workspace.client.download_artifacts(run_id, "reproduction/manifest.json"))
    old = json.loads(local.read_text())
    if old["code_revision"] != code_revision() or old["data_sha256"] != sha256(DATA / "demand-v1.csv"):
        raise ValueError("Restore recorded source and data before reproduction")
    if old["environment"] != environment():
        raise ValueError("Restore recorded Python/package/lock environment before reproduction")
    if Path(destination).exists():
        raise ValueError("Reproduction destination must not exist")
    fresh = Workspace(destination)
    result = fresh.run(Config(**old["config"]), name="reproduced", partition=old["evaluation_partition"])
    delta = abs(result["metrics"]["rmse_kwh"] - old["metrics"]["rmse_kwh"])
    report = {"original_run_id": run_id, "reproduced_run_id": result["run_id"], "rmse_delta": delta,
              "tolerance": TOLERANCE, "passed": delta <= TOLERANCE, "lineage_matched": True}
    write_json(fresh.path / "reproduction-check.json", report)
    return report


def verify_summary(rows, recommended_run_id):
    """Numeric recommendation gate; semantic caveats still require human evidence review."""
    required = ["run_id", "alpha", "rmse_kwh", "comparison_group", "data_sha256",
                "code_revision", "range_guard", "evaluation_partition"]
    if not set(required).issubset(rows.columns) or rows[required].isna().any().any():
        raise ValueError("Selected run evidence is missing required fields")
    group = rows.copy()
    if (len(group) < 5 or group.run_id.duplicated().any()
            or group.alpha.astype(float).nunique() < 5):
        raise ValueError("Select 5+ unique runs with 5+ distinct alpha configurations")
    if (not group.comparison_group.eq("demand-v1-validation").all()
            or not group.evaluation_partition.eq("validation").all()
            or not group.range_guard.astype(str).eq("True").all()):
        raise ValueError("Select only guarded validation runs; label excluded runs separately")
    controls = ["data_sha256", "code_revision"]
    if any(group[c].nunique() != 1 for c in controls):
        raise ValueError("Selected runs must share data and code controls")
    if not all(math.isfinite(float(value)) and float(value) >= 0 for value in group.rmse_kwh):
        raise ValueError("RMSE evidence must be finite and nonnegative")
    best = group.sort_values(["rmse_kwh", "run_id"]).iloc[0]
    return {"recommended_run_id": recommended_run_id, "best_run_id": best.run_id,
            "best_rmse_kwh": float(best.rmse_kwh), "recommendation_matches_metric": recommended_run_id == best.run_id}
