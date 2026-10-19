✂️
# Rolling back a bad model version

Linden Facilities trialed a version that met the original RMSE gate of `5` kWh. A revised acceptance review now requires validation RMSE <= `1.6` kWh. The alpha `10` trial fails that requirement, while the previously approved alpha `1` version satisfies it. Preserve both artifacts while restoring the approved selection.

**Continue here:** [Sprint 3 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=registry-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use your own two originally approved versions with the trial currently active, or create the intended starting state with `uv run python exercises/prepare-practice.py rollback --state state-rollback` from the helper/project root. Read `state-rollback/case.json`, then inspect the actual version tags and source runs using the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md). The preparation stops before rollback; the learner must perform that operation. An **audit event** records a change; the current alias lookup records only the present selection.

| Before learner work | Required observation after work |
|---|---|
| Trial is active | Alias points to a suitable prior approved version |
| Original gate still recorded | Client incident and changed requirement explained |
| Prior batch may exist | New job records the restored version |

## Your task

Record the active version and source run before the rollback. Find the previous approved version by its actual validation evidence. Confirm the revised RMSE requirement against both raw runs. Reassign `active` to that previous version using the helper, with a reason that names the acceptance failure.

Run a new representative batch and prove its resolved version/source run match the restored version. Save the before/after alias evidence, application audit event and batch output. Mark the trial's incident using a version tag; do not delete it to make the history look cleaner.

Explain what the audit captured: time, old/new versions, source run and reason. Also explain its limits: helper-mediated changes only, mutable local evidence, no guarantee that an already-running job reloaded a model, and no atomic transaction across alias change and event persistence.

## Working with documentation

Use the [MLflow alias API example](https://mlflow.org/docs/3.5.1/ml/model-registry/workflow/) to distinguish reassignment from registering another artifact.

## Hints

1. A rollback changes the selection pointer; it does not undo training.
2. Read the old/new fields before interpreting the event as a reversal.
3. Batch inference must be invoked again after reassignment to prove the next job follows it.

## Checkpoints

Both versions remain inspectable. The event's previous version is the trial and new version is the approved version. A new batch records the restored version. If registry and log disagree, report the inconsistency and reconcile it rather than claiming a complete audit.

## Learning outcome

Reassign the active-model alias from a bad version to the previous approved version, and document what the registry audit evidence captured during the rollback.

## Summary

The restored alias is backed by a reasoned event and a new batch using the previous approved version. Both artifacts remain available to explain the incident.
