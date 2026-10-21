✂️
# Reproducible pipeline deliverable

Harbor Facilities is the receiving team for your completed cumulative pipeline. Its receiving engineer has your clean execution evidence, but a newly copied handoff package fails acceptance. Diagnose that unfamiliar failure, repair the copy and determine which earlier proof still applies.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Reproducible pipeline deliverable** using its Campus activity ID **A-S4-06**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Reuse your canonical selected-run export, actual clean receiving result, extension checks and handoff note. Prepare a deliberately altered client copy:

```sh
uv run python docs/course/exercises/prepare-evidence.py receiving --destination work/harbor-receiving
```

Read the generated receiving brief. The `candidate-bundle` inside that directory is a copy for this assessment; the selected source run, canonical export and original tracking store stay intact. The copy deliberately contains a fault to investigate. Attempt the taught acceptance procedure against the copy using a new destination and preserve the failure before repairing anything. Do not modify your canonical export, regenerate the checksum index, change tolerance, retune or bypass the acceptance checks.

After validation-based selection is fixed, observe the reserved final partition once using `uv run linden-mlops final` in the original cumulative project. Keep the result separate from promotion and recovery; do not retune. Reuse the cached observation if it already exists. No live session is needed for this checkpoint.

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

At which verification layer does the copied package fail? What is the smallest evidence-preserving repair? If the repaired package matches the already proven canonical export, which claims can reuse the earlier receiving evidence and which would need a fresh execution?

## Quick diagnosis

Before editing the copy, preserve the exact command, exit/failure text and the earliest failed acceptance layer. Identify the affected file from evidence and explain whether the result is a packaging, lineage/environment, numerical or serving failure. State what can already be ruled out and what has not yet been tested.

## Making improvements

### Task A — Trace the connected system

Use the existing cumulative records to trace train → track → register → select active → batch, including at least one non-trivial validated extension and its line-by-line explanation. The optional T4 estimator transfer stays inside the same interfaces and has separately established validation evidence. Identify which source run and export Harbor is supposed to receive.

### Task B — Diagnose and repair the client copy

Investigate `candidate-bundle` using the taught recovery checks. Keep its original failure record. Restore the affected copied artifact from the canonical export, explaining the source of truth and why the repair addresses the first failure. Preserve the original checksum index and intended selected configuration. Verify that the repaired package's indexed files and their hashes agree with the canonical export; fixing a filename or obtaining a successful prediction alone is insufficient.

### Task C — Scope the receiving proof

Connect your previous clean test to the exact canonical export, restored source, new environment and empty state used there. Check the existing lineage comparison, absolute validation RMSE delta `<=1e-6` kWh and batch evidence: intended active version, `24` finite aligned predictions and completion within `60` seconds. Decide, with evidence, whether another full clean run is needed after this repair. If bytes, source or environment differ, diagnose the difference and execute a fresh receiving test; never stretch the earlier proof to a different recipe.

In the receiving environment, probe a separate input copy with `occupancy=101` and preserve its rejection without modifying the bundled data. Include the responsible stage in your extension explanation. Keep the reserved final observation separate from both validation selection and the recovery comparison.

## Final check

Update the same handoff note with the failed command/output, diagnosis, repair source, before/after integrity evidence and the scope of reused or new receiving evidence. Keep the original failure visible. A passing numerical score cannot override a failed checksum or lineage check. Your note should let a second engineer distinguish an accepted package from a merely plausible result.

## Check your diagnosis after the attempt

<details>
<summary>Solution — failed package, repair and evidence reuse</summary>

**Result you should get:** the first failure is export integrity: `config.json` in `candidate-bundle` differs from the original recorded hash. The acceptance error is `Recovery file missing or changed: config.json`. This happens before recovery training and does not establish numerical, environment or serving divergence. Restoring that file from the canonical selected-run export makes the indexed package agree again without changing `bundle.json`, selection or tolerance.

A justified reuse decision requires identical indexed bytes to the exact canonical export already used in a successful clean-source/environment/state receiving test. When that identity and the earlier complete receiving evidence are verified, another identical training run adds no new proof. A checksum pass alone is insufficient if the prior test used another recipe, never started clean or lacks serving evidence. An extra/unindexed file is outside the checksum index; do not silently treat it as part of the accepted recipe.

**How:** retain the original failure, then compare the copied file and index with the canonical export before restoring the recorded artifact. In a local script, replace the path below with your actual canonical export. This integrity check does not train or consult the original tracking store:

```python
from pathlib import Path
import json
from linden_mlops.pipeline import sha256
from linden_mlops.recovery import verify_bundle

canonical = Path("work/handoff-export")  # your actual selected-run export
candidate = Path("work/harbor-receiving/candidate-bundle")
verify_bundle(canonical)
verify_bundle(candidate)
assert (candidate / "bundle.json").read_bytes() == (canonical / "bundle.json").read_bytes()
index = json.loads((canonical / "bundle.json").read_text())
for name, expected in index["files"].items():
    assert sha256(canonical / name) == expected
    assert sha256(candidate / name) == expected
print("All indexed files match the canonical export")
```

The first `verify_bundle(candidate)` fails before the repair and succeeds afterward. A valid repair copies the canonical `config.json`; generating a new index would hide the corruption. After preserving the original failed evidence, the repair itself is:

```python
from shutil import copyfile
copyfile(canonical / "config.json", candidate / "config.json")
```

Run the integrity comparison again after that copy. Link the passing comparison to the existing `recovery-check.json`, batch CSV/metadata and audit event. Check all invariant fields and the absolute RMSE delta, then the batch's source run/version, row order, finiteness and completion time. Preserve the `occupancy=101` rejection and explain that the range guard stops it before prediction.

If integrity still fails, inspect the named indexed file before retraining. If integrity passes but lineage fails, restore the recorded source/data/environment or label and test the portability change. A final-partition result answers a different evaluation question and cannot replace the validation recovery score.

</details>

## Learning outcome

Deliverable: the cumulative end-to-end pipeline (train -> track -> register -> select active version -> exercise the selected inference path) reproduced from the declared clean state, with traceable code/data/configuration/environment lineage, reproducible setup/run instructions, inference evidence, and at least one non-trivial extension documented and explained.

## Summary

Harbor’s altered copy has an evidence-based diagnosis and repair. Your handoff connects exact package identity to the clean lifecycle and serving proof, so a receiving engineer can tell which claims have actually been established.
