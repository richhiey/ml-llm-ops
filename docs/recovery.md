# Export the selected recipe and test a clean receiver

Use the intended active model's explicit source **validation** run as the operational handoff recipe. The original five-run selection remains its historical experiment decision. Keep one `work/HANDOFF.md` with actual locations, configuration, extension explanation and checks. The portable export and that document have different jobs: the export supplies recoverable content; the runbook tells a receiver how to use and judge it.

## Know which location a command uses

| Location | Contains / purpose |
|---|---|
| Original project | Your current source/environment, `work/project.json` and `work/tracking` |
| Canonical export | `manifest.json`, `config.json`, `environment.txt`, `source.tar.gz`, fitted `model/`, indexed `training-data.csv` for data-aware runs, and `bundle.json` |
| Receiving source | A newly restored folder containing code/data/lock and a newly installed `.venv` |
| Receiving state | A previously absent directory for the new run, registry, audit and batch |

The archive includes recorded application source, meaningful regression tests, bundled reference data and lock. It excludes course assets, examples and fixture preparation tools. A learner-created source module and its test are included as ordinary application files. Data-aware runs also export their exact selected `training-data.csv` separately under the checksum index; receiving uses those bytes, including feedback when applicable. The automatic export does **not** collect `work/HANDOFF.md` or arbitrary learner notes. Transfer the runbook beside the export, with the changed-stage explanation/diff and relevant probe evidence copied or quoted from your existing work. Refer to those supplementary files by package-relative names. Keep them distinct from indexed runtime inputs; do not rewrite an existing export index to add a report.

## Inspect and export in the original project

```sh
uv run linden-mlops status
uv run linden-mlops export --release work/release.json --destination work/handoff-export
```

Create and verify the real release descriptor described in the [API reference](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md), naming the intended active version, source run and actual batch. Export consumes that checked selection, including its current/approved model, actual job and training/serving-source agreement.

The separate `--run-id ACTUAL_RUN_ID` route exports an explicitly named run's archived recipe, with `--state` when needed for an isolated store. It does not verify a release descriptor, current active selection or actual serving job. A valid archived recipe alone is therefore insufficient evidence for the operational handoff required here. There is no historical-selection default. Do not use the reserved final-evaluation run. Destinations must be new. If an export already exists, inspect its manifest and reuse it only when it is the intended recipe; do not overwrite it.

A **checksum index** records expected file-content fingerprints. It detects a changed/missing copy relative to that retained index. It does not establish the origin of an arbitrary package by itself: use the canonical export you retained from the selected run. `verify_bundle` is a read-only inspection, not training:

```python
from pathlib import Path
from linden_mlops.recovery import verify_bundle

bundle = Path("work/handoff-export").resolve()
manifest = verify_bundle(bundle)
print("Selected source run:", manifest["run_id"])
print("Recorded config:", manifest["config"])
print("Exact Python patch:", manifest["environment"]["python"])
print("Portable export:", bundle)
```

Put this in your inspection script and retain the actual values in the runbook. `bundle.json` covers its indexed files; unindexed additions are not silently part of that integrity claim. A checksum failure stops before training. Diagnose the named file against authoritative retained content before considering later layers.

## Restore source and install its own environment

From the original project:

```sh
uv run linden-mlops restore-source --bundle work/handoff-export --destination ../linden-received
```

`restore-source` checks integrity and unpacks code/data/lock. The source destination must not exist; it does not copy the original `.venv` or tracking store. Record the actual absolute export path before changing folders.

In a new terminal starting at the **original-project directory**, replace `RECORDED_PATCH` below with `manifest.environment.python` (for example, `3.12.13` only when that is your recorded value). Do not pass the literal placeholder or assume that `3.12` selects the same patch.

```sh
cd ../linden-received
uv sync --locked --python RECORDED_PATCH
uv run python --version
uv run python -c "import sys,linden_mlops; print(sys.prefix); print(linden_mlops.__file__)"
uv run pytest tests/test_batch_input.py tests/test_spine.py::test_contract_extension_and_unchanged_pipeline -q
```

The completed branch includes your new `src/linden_mlops/batch_input.py` stage, its call in `batch_predict` and your `tests/test_batch_input.py` regression file. Those files must be present in the restored selected-source archive; the untouched baseline intentionally lacks this learner-added stage. Do not substitute the existing range-guard test for the new complete-plan checks.

Check that no `.venv` existed before installation, `sys.prefix` is the receiving `.venv`, and the package path belongs to its restored `src/linden_mlops`. Select that interpreter in VS Code if editing there. The exact environment check also compares installed distributions, lock hash, operating system and architecture. A different platform is a deliberate portability investigation, not identical-environment reproduction. [uv synchronization](https://docs.astral.sh/uv/concepts/projects/sync/) and [Python version requests](https://docs.astral.sh/uv/concepts/python-versions/) explain the installation options.

## Execute without the original store, then restore it

Use this reversible reference pattern in the **original-project terminal** after installing the receiving environment. Stop its MLflow UI and other producer processes first. Adapt the three locations to your runbook; keep the export available. Save this as `work/receive-isolated.py` and run `uv run python work/receive-isolated.py`:

```python
from pathlib import Path
import os
import subprocess

original = Path("work/tracking").resolve()
offline = original.with_name("tracking.offline")
bundle = Path("work/handoff-export").resolve()
receiver = Path("../linden-received").resolve()
if not original.is_dir() or offline.exists():
    raise RuntimeError("Inspect original/offline paths before isolating; preserve both")
if not (receiver / ".venv").is_dir() or (receiver / "work/received").exists():
    raise RuntimeError("Use the installed receiving environment and a new receiving state")
env = os.environ.copy()
for key in ["VIRTUAL_ENV", "PYTHONPATH", "LINDEN_WORK_DIR"]:
    env.pop(key, None)
original.rename(offline)
try:
    assert not original.exists()
    print("Original store unavailable:", original, flush=True)
    subprocess.run([
        "uv", "run", "--locked", "python", "-c",
        "import sys,linden_mlops; from pathlib import Path; "
        "print('Receiving interpreter:', sys.prefix); "
        "print('Receiving source:', linden_mlops.__file__); "
        "assert Path(sys.prefix).resolve() == Path('.venv').resolve(); "
        "assert Path(linden_mlops.__file__).resolve().parents[2] == Path.cwd().resolve()",
    ], cwd=receiver, env=env, check=True)
    subprocess.run([
        "uv", "run", "--locked", "linden-mlops", "reproduce-export",
        "--bundle", str(bundle), "--destination", "work/received",
    ], cwd=receiver, env=env, check=True)
    assert not original.exists(), "Another process recreated the original store"
finally:
    if original.exists():
        raise RuntimeError("A new store appeared at the original path; preserve it and the offline store, then reconcile before restoring")
    offline.rename(original)
    print("Original store restored:", original, flush=True)
```

The `finally` block restores the store on normal completion or command failure. If another process recreates the old path, it refuses to overwrite either copy; reconcile them before continuing. A forced process termination can prevent cleanup: retain both paths and restore the preserved store to its exact original location before returning to producer work. Its artifact addresses depend on that location. Never delete the store to demonstrate independence.

The receiving command reads the export, checks loaded source/data/environment, retrains the recorded validation configuration, logs a new model, registers/approves it under the local metric policy, assigns `active` and creates a new batch. It does not consult the original store. Its approval reason does not execute contract tests; those were a separate command above. The exported original model address remains lineage evidence, while the receiver logs its own model.

## Inspect the receiving result in the receiving source

Read `work/received/recovery-check.json`, `batch.csv`, `batch.json` and `audit.jsonl`. Compare the original manifest with the receiving raw records:

| Layer | What to verify |
|---|---|
| Clean execution | New source/environment/state and recorded original-store isolation |
| Recipe | All source/data/config/partition/environment invariants agree |
| Evaluation | Absolute validation RMSE difference `<=0.000001` kWh |
| Lifecycle | Newly trained run → version/approval → active alias → job version/source |
| Output | Independently check `24` unique aligned IDs, finite predictions, input hash and completion `<=60` seconds |

`passed=True` in the helper report checks useful conditions, but it does not independently establish output order/finiteness or the history of your installation. Inspect those facts. New run IDs, paths, timestamps and version counters can differ. Whole-job timing covers model loading through file writing, excluding setup/training; calculate throughput as delivered rows divided by seconds.

For further input probes from the receiving source, use an explicit received store, for example `uv run linden-mlops batch --state work/received --input work/PROBE.csv --output-name NEW_PROBE_NAME`. Prepare a separate input copy, predict the result and use a fresh output name. The receiver does not automatically have the producer’s `work/project.json` selection.

If a command fails, retain its command/output and diagnose the first failed layer: integrity, source/data/config/environment, numerical agreement, then delivery. Repair the prerequisite or instructions and retry only the affected receiving proof in a new destination. Do not widen tolerance, retune or rewrite the original checksum index. A prior clean proof applies only to the same proven package and conditions; an integrity pass alone cannot replace it.

## Smaller past-run replay

`uv run linden-mlops reproduce --run-id ACTUAL_SELECTED_ID --destination work/past-replay` uses the original store and a new state. It checks the recipe and score while reusing the installed source/environment. It cannot establish the broader receiving proof above.

## Final observation

Only after freezing the validation selection and restoring the original store, run `uv run linden-mlops final` in the original cumulative project. It evaluates the selected configuration on reserved final rows and caches that observation. Reopening reuses it. Do not retune from it or promote that final-evaluation run; registration and recovery continue to use the selected validation source run.

## Operational evidence

Keep a short incident record and the policy/monitor/comparison observations beside the indexed export. The [operational runbook](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md) distinguishes reference/current monitoring, independent feedback labels and candidate evaluation. The historical final observation does not establish current-condition quality for a feedback-trained candidate.

## Source identity at release

An intermediate batch can investigate a new serving validation change with an existing fitted model. A final release must use one matching current training and serving source revision: the exported source is the training-time archive. If source changes afterward, revalidate/retrain the intended recipe from the completed source in a deliberate new experiment, then produce a fresh named batch before exporting. The release verifier rejects a source mismatch before creating an export directory.
