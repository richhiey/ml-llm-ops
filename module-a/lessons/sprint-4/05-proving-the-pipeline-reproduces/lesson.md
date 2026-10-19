✂️
# Proving the pipeline reproduces

Linden Facilities receives your handoff, but its reproducibility claim remains unproven until someone runs it from the declared starting state. This task tests the handoff rather than your ability to remember how you built it.

## Your route through this lesson

Execute the written handoff in a new source/environment/store and diagnose divergence. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Clean-run transcript, invariant comparison, numeric delta and new active-version batch.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=handoff-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use your packaged source, data snapshot, lock, recorded config, original raw run and `HANDOFF.md`. The [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) distinguishes a new environment from merely restarting a notebook kernel.

| Expected to change | Must agree |
|---|---|
| Run ID, timestamp, path, version counter | Source/data/config/evaluation/environment |
| Observed timing | Completion within declared budget |
| New model execution identity | RMSE within declared absolute tolerance |

## Establish what “clean” means for this run

Use a new source folder, a newly created locked Python environment and a new state directory. A restarted notebook with an existing fitted model is not this starting state. Download caches may be reused, but the result must not depend on an already loaded model, original registry or variables from the authoring session.

If earlier investigation happened in Colab, create the comparison run in the supported locked local environment first. The hosted package set and Linux platform are not the same environment as a local macOS setup. Do not report an expected strict-environment rejection as random numerical drift, and do not remove the environment check to make the report pass.

## Run the instructions without silently repairing them

Capture the exact commands, interpreter, working directory and output path. Execute the declared connected lifecycle. If the document omits a needed step, preserve that attempt and revise the package/instructions; do not describe the attempt as a clean success because you knew how to fix it interactively.

Your new run should produce its own execution ID, registered version and output paths. Those changes are expected. Compare invariant lineage fields before comparing the metric. If a hash or config differs, you are not yet testing the same recipe.

## Separate identity, numeric agreement and serving

| Decision | Required comparison |
|---|---|
| Same recipe? | Code/data/config/partition/environment match |
| Same evaluation within contract? | Absolute difference of like RMSE values <= `1e-6` |
| Usable connected handoff? | New active-version batch, row integrity and completion requirement |

All three matter. Matching RMSE does not fix different source. Matching source does not prove the new artifact was registered and served. A successful batch from an old cached object does not prove retraining.

## Diagnose one field at a time

When a comparison fails, name the first differing field and inspect its source. A changed data hash may indicate modified bytes despite an unchanged filename. A package mismatch may come from selecting the wrong interpreter or installing extra distributions. An RMSE mismatch after matching recorded inputs needs closer numerical/execution investigation. Keep cause hypotheses distinct from confirmed causes.

Write the next check that would distinguish your hypotheses, then record the observed result. Correct the source/package/instructions and rerun into a different fresh destination. The final report should connect the failed attempt, diagnosis and successful correction rather than editing the failed result out of existence.

Finish by stating the strongest claim you actually established: new-store replay, fresh-environment training recovery, or the full connected handoff. This activity aims for the last of these, with lineage and tolerance evidence the receiver can inspect.

## Your task

Restore the package to a new source folder, create a fresh environment with the lock, and use a new state directory. Follow your handoff commands verbatim. Capture the complete end-to-end result: training/evaluation, tracking, registered version, validated active alias and batch evidence.

Compare original and new source revision, data hash, config, evaluation partition and environment. Compute the absolute RMSE difference and compare with `1e-6` kWh. Verify active-version inference meets the `24`-row/`60`-second brief. Keep changed identifiers separate from invariant lineage fields.

Write `clean-run-report.md` with commands, observed evidence, comparisons, pass/fail and any diagnosis. If a field differs or a command needed undocumented knowledge, fix the package and rerun from another fresh directory. Preserve the failed attempt as diagnosis evidence.

## Working with documentation

Use the [reproduction contract](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) to identify what must agree. Do not relax tolerance after seeing a disagreement.

## Hints

1. Snapshot bytes matter more than a familiar filename.
2. Verify interpreter and lock before blaming numerical variation.
3. A cached model predicting correctly cannot prove retraining was reproduced.

## Checkpoints

Both the old and new records remain inspectable. The result passes lineage and tolerance together. Your report distinguishes a fresh-source/environment test from a new-store replay. An unexplained divergence is an incomplete handoff, even if inference succeeds.

## Use a divergence decision table

For each mismatch record `observed field`, `expected value`, `likely cause`, `next check` and `resolved evidence`. A changed run ID is expected; a changed snapshot hash is not. A score outside tolerance with matching recorded inputs calls for environment/numerical investigation; a matching score with a different source still fails lineage. Preserve the failed attempt and a corrected rerun rather than editing its report to pass.

## Learning outcome

Re-run the completed pipeline from the declared clean state, verify its lineage and result against the tolerance declared in the clean-state verification specification, and document and diagnose any divergence.

## Summary

The clean run turns a setup claim into observed evidence. Your comparison separates changed identifiers from the lineage and results that must agree.
