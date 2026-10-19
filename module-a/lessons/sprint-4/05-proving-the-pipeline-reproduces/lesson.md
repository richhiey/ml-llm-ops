✂️
# Proving the pipeline reproduces

Linden Facilities receives your handoff, but its reproducibility claim remains unproven until someone runs it from the declared starting state. This task tests the handoff rather than your ability to remember how you built it.

**Continue here:** [Sprint 4 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb#scrollTo=handoff-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use your packaged source, data snapshot, lock, recorded config, original raw run and `HANDOFF.md`. The [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) distinguishes a new environment from merely restarting a notebook kernel.

| Expected to change | Must agree |
|---|---|
| Run ID, timestamp, path, version counter | Source/data/config/evaluation/environment |
| Observed timing | Completion within declared budget |
| New model execution identity | RMSE within declared absolute tolerance |

## Your task

Restore the package to a new source folder, create a fresh environment with the lock, and use a new state directory. Follow your handoff commands verbatim. Capture the complete end-to-end result: training/evaluation, tracking, registered version, validated active alias and batch evidence.

Compare original and new source revision, data hash, config, evaluation partition and environment. Compute the absolute RMSE difference and compare with `1e-6` kWh. Verify active-version inference meets the `24`-row/`60`-second brief. Keep changed identifiers separate from invariant lineage fields.

Add a clean-run section to your existing handoff index with commands, observed evidence, comparisons, pass/fail and any diagnosis. If a field differs or a command needed undocumented knowledge, fix the package and rerun from another fresh directory. Preserve the failed attempt as diagnosis evidence.

## Working with documentation

Use the [reproduction contract](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) to identify what must agree. Do not relax tolerance after seeing a disagreement.

## Hints

1. Snapshot bytes matter more than a familiar filename.
2. Verify interpreter and lock before blaming numerical variation.
3. A cached model predicting correctly cannot prove retraining was reproduced.

## Checkpoints

Both the old and new records remain inspectable. The result passes lineage and tolerance together. Your report distinguishes a fresh-source/environment test from a new-store replay. An unexplained divergence is an incomplete handoff, even if inference succeeds.

## Learning outcome

Re-run the completed pipeline from the declared clean state, verify its lineage and result against the tolerance declared in the clean-state verification specification, and document and diagnose any divergence.

## Summary

The clean run turns a setup claim into observed evidence. Your comparison separates changed identifiers from the lineage and results that must agree.
