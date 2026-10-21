✂️
# Proving the pipeline reproduces

Linden Facilities receives your handoff, but its reproducibility claim remains unproven until someone runs it from the declared starting state. This task tests the handoff rather than your ability to remember how you built it.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Proving the pipeline reproduces** using its Campus activity ID **A-S4-05**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Follow your runbook using [portable recovery](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md): restore to a new folder, run `uv sync --locked --python 3.12`, run tests and execute `reproduce-export` with the absolute export path and a new destination. Make the original store unavailable while testing portability, preserving it intact elsewhere. Inspect the receiving report, batch and alias event. Add only actual mismatches/corrections to your existing runbook. A new kernel alone is insufficient.


## Starting point

Use your packaged source, data snapshot, lock, recorded config, original raw run and `HANDOFF.md`. The [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md) distinguishes a new environment from merely restarting a notebook kernel.

| Expected to change | Must agree |
|---|---|
| Run ID, timestamp, path, version counter | Source/data/config/evaluation/environment |
| Observed timing | Completion within declared budget |
| New model execution identity | RMSE within declared absolute tolerance |

## Your task

Restore the package to a new source folder, create a fresh environment with the lock, and use a new state directory. Follow your handoff commands verbatim. Capture the complete end-to-end result: training/evaluation, tracking, registered version, validated active alias and batch evidence.

Compare original and new source revision, data hash, config, evaluation partition and environment. Compute the absolute RMSE difference and compare with `1e-6` kWh. Verify active-version inference meets the `24`-row/`60`-second brief. Keep changed identifiers separate from invariant lineage fields.

Add a clean-run section to your existing handoff index with commands, observed evidence, comparisons, pass/fail and any diagnosis. If a field differs or a command needed undocumented knowledge, fix the package and rerun from another fresh directory. Preserve the failed attempt as diagnosis evidence. In your diagnosis, distinguish a run that succeeds numerically but uses the wrong snapshot from one that has new IDs and matching lineage. State which is acceptable before opening the self-check; no additional execution is needed for this comparison.

## Working with documentation

Use the [reproduction contract](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md) to identify what must agree. Do not relax tolerance after seeing a disagreement.

## Hints

1. Snapshot bytes matter more than a familiar filename.
2. Verify interpreter and lock before blaming numerical variation.
3. A cached model predicting correctly cannot prove retraining was reproduced.

## Checkpoints

Both the old and new records remain inspectable. The result passes lineage and tolerance together. Your report distinguishes a fresh-source/environment test from a new-store replay. An unexplained divergence is an incomplete handoff, even if inference succeeds.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** one receiving execution from restored source, a fresh locked environment and a new store that does not depend on the original store. It has matching recorded source/data/config/partition/environment, absolute validation RMSE delta <= `0.000001` kWh, and a connected validated active version producing the accepted batch. New IDs are acceptable; a wrong snapshot fails even with the same score.

**How to check:** inspect the receiving report and raw lineage, then the registry/audit and batch output. A green numeric comparison alone does not prove the original store was unavailable or the environment was new; retain the commands and directories that show those conditions. Diagnose checksum/source/data/config/environment before numerical variation. If you repair a package or undocumented command, retry only the failed receiving proof from another fresh destination and preserve the earlier attempt. Do not widen tolerance or relabel a same-environment replay as a clean installation.

</details>

## Read the notebook figure

![Fresh receiving evidence: recipe invariants, delivered rows and validation RMSE tolerance](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/sprint-4/05-proving-the-pipeline-reproduces/assets/recovery-checks__01__en.png)

This verified receiving run restored the source into a fresh locked environment and used a new store while the original store was unavailable. Its source, data, environment, config and partition invariants pass. Independently checked output contains 24 aligned, finite predictions; batch execution took about 0.007443 seconds on the author machine, within 60 seconds. The absolute validation RMSE difference is 0 kWh against the declared 0.000001 kWh tolerance. Setup and retraining time are separate. New IDs are expected; matching lineage and tolerance are required.

Regenerate this figure from your actual records in the sprint notebook. The [editable SVG](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/05-proving-the-pipeline-reproduces/assets/recovery-checks__01__en.svg) and [reference observations](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/figures/reference-observations.json) make this author example inspectable.

## Learning outcome

Re-run the completed pipeline from the declared clean state, verify its lineage and result against the tolerance declared in the clean-state verification specification, and document and diagnose any divergence.

## Summary

The clean run turns a setup claim into observed evidence. Your comparison separates changed identifiers from the lineage and results that must agree.
