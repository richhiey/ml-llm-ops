✂️
# Rolling back a bad model version

Linden Facilities trialed a version that met the original RMSE gate of `5` kWh. A revised acceptance review now requires validation RMSE <= `1.6` kWh. The alpha `10` trial fails that requirement, while the previously approved alpha `1` version satisfies it. Preserve both artifacts while restoring the approved selection.

## Your route through this lesson

Inspect a changed acceptance condition and restore a suitable prior selection. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Before/after alias, reasoned audit event and a new batch using the restored version.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=registry-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use your own two originally approved versions with the trial currently active, or create the intended starting state with `uv run python exercises/prepare-practice.py rollback --state state-rollback` from the helper/project root. Read `state-rollback/case.json`, then inspect the actual version tags and source runs using the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md). The preparation stops before rollback; the learner must perform that operation. An **audit event** records a change; the current alias lookup records only the present selection.

| Before learner work | Required observation after work |
|---|---|
| Trial is active | Alias points to a suitable prior approved version |
| Original gate still recorded | Client incident and changed requirement explained |
| Prior batch may exist | New job records the restored version |

## Inspect before changing selection

This practice begins with a trial active. Do not run the complete worked registry notebook to prepare it: that reference ends after its own rollback. Use the supplied preparation command or an equivalent real state whose before-condition you can demonstrate. Read the current alias, both versions' validation tags and their source runs before selecting a target.

The incident is a changed client requirement. Both versions passed the original 5-kWh teaching gate. The client's revised 1.6-kWh limit now makes the trial unacceptable. An old `approved` tag describes the earlier decision; it does not override the new requirement. You must connect each version's raw validation score to the correct source run and decide which version meets the revised condition.

## Plan the smallest corrective action

A rollback reassigns the alias to a suitable existing version. It does not undo the trial's training, reset the version counter or erase the incident. Write the intended transition before executing it: current version → chosen prior version, with the failed client condition as the reason.

Use the actual returned identities from your store. If the counters differ from an example, that is not automatically wrong. The important checks are source-run linkage, prior approval evidence and suitability under the revised brief. Preserve the trial artifact so another engineer can inspect why the decision changed.

## Make the after-condition observable

After reassignment, a current alias lookup should show the intended prior version. That proves selection state. A new batch should record that same resolved version and source run. That proves a subsequent job used the restored artifact. Keep these as two distinct observations; a previously written CSV says nothing about the new selection.

| Evidence | Before | After |
|---|---|---|
| Current alias | Trial version/source run | Restored approved version/source run |
| Client requirement | Revised 1.6-kWh limit | Same limit, applied to chosen record |
| Helper event | Earlier events retained | New old/new/time/reason entry |
| New batch | Not yet run | Output and resolved restored identity |

## Explain what the audit cannot tell you

Read the actual event and compare it with current registry state. Its previous/new versions should match your intended transition. The event covers helper-mediated changes; it does not prove that nobody edited the registry directly. The local log is mutable, and alias reassignment plus event persistence is not one atomic transaction. A job that resolved its model before rollback can continue with that model.

Your incident note should state what you observed, what action you took and what the next batch demonstrated. Avoid claiming that rollback repaired every possible consumer. If an event or source-run link is missing, record the gap and investigate rather than rewriting history to make the incident look complete.

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

## Separate the helper gate from the client incident

The original helper gate remains `5` kWh. The revised client requirement is a separate acceptance decision, so the helper will not automatically select the suitable version. Cite both raw scores against `1.6`, tag the trial's incident and explain why it is being replaced. Approval tags left from the original gate are historical context, not proof that the trial satisfies the revised brief.

## Learning outcome

Reassign the active-model alias from a bad version to the previous approved version, and document what the registry audit evidence captured during the rollback.

## Summary

The restored alias is backed by a reasoned event and a new batch using the previous approved version. Both artifacts remain available to explain the incident.
