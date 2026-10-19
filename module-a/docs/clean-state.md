# Clean-state verification specification

A clean state means a new source folder restored from the pinned helper source archive, Python 3.12 with a newly created `.venv` installed by `uv sync --locked`, and a new nonexistent state directory. No inherited database, model cache relied upon, notebook variables, registry or prior batch output is required. OS package/download caches may exist; results may not depend on cached model objects. Authoring was checked on macOS ARM64 with Python 3.12.13; other platforms must be reverified.

## End-to-end handoff

```sh
uv sync --locked
uv run pytest -q
uv run campus-mlops handoff --state state-fresh --alpha 1 --range-guard --autolog
```

Inspect returned `training.run_id`, `code_revision`, `data_sha256`, `config`, `environment` (Python, all installed distribution versions, OS family/architecture and lock hash), `model_uri`, metrics, registered `version`, audit event and `inference`. Each run stores those fields in `reproduction/manifest.json` and stores the corresponding `source.tar.gz`, `environment.txt` and `config.json`. Confirm data/config/source/lock against the original, not only the displayed score. Match registered version to its run and batch `resolved_version` to `active` at job start.

## Reproduce a past run

Save the original run ID. While the original store is available:

```sh
uv run campus-mlops reproduce --state state --run-id ACTUAL_RUN_ID --destination state-reproduced
```

Replace `ACTUAL_RUN_ID` with the recorded ID. Destination must not exist. This reruns the recorded config and evaluation partition, checks source/data/environment identity, and writes `reproduction-check.json`. Acceptance: absolute RMSE difference <= **0.000001 kWh** and matching lineage. Timing, run IDs, timestamps, artifact locations and model version numbers are expected to differ. Never widen tolerance to hide changed data or an environment mismatch.

If the source differs, download `reproduction/source.tar.gz` from the original run and extract into a **new** folder; inspect archive paths first. Run `uv sync --locked` there. Preserve the original store and use its absolute path for `--state`; use another new destination. The manifest's `command` is an exact recorded-config training command. For the complete lifecycle, run `handoff` with the chosen validation-run alpha/guard/autolog settings in a new state. Final-partition observations are evaluation-only and cannot pass validation-based promotion.

Diagnose in order: source revision, data hash, partition/config, Python and package/lock versions, model source run, then numerical difference. An RMSE match with different lineage is not a pass. Use the final partition only after selecting alpha; final and validation numbers cannot be compared as if they measured the same rows.


## Recover artifacts without assuming old absolute paths relocate

MLflow's original local artifact URIs are absolute. Retain the original store for comparison, or export its files before moving the package. From the original helper environment, use the MLflow client `download_artifacts(run_id, 'reproduction', dst_path=...)` to copy recovery files and `mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path=...)` to copy the logged model directory. Record their locations in the handoff. Inspect and extract `source.tar.gz` into a new source folder, use Python 3.12 and `uv sync --locked`, and run the manifest's exact training flags into a new state. The new run creates its own artifact paths; comparing original lineage does not require pretending the old SQLite file's absolute paths relocated. For the complete handoff, register and activate a validation run, then exercise batch inference. Use `train --partition final` only for the reserved final evaluation; the validation-based approval policy rejects final-partition promotion.
