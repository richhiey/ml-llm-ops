✂️
# Registry lifecycle deliverable

Harbor Facilities hands over three model versions and a revised validation-error limit. A trial is active, and a newer artifact is still pending. Identify and restore a suitable prior approved version from the evidence, rather than assuming that “latest” means safe.

## Your route through this lesson

Resolve the client incident from actual tags and metrics, then prove recovery and lineage. Use your cumulative project and the supplied client inputs. Plan and perform the taught work independently. Keep the starting state and actual evidence; the reviewer uses separate validation material.

**Finish with:** Qualifying prior selection, retained decoy/incident records, batch and reproduction packet.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=checkpoint-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## What you will work with

Use your cumulative helper project, its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Which version meets the revised client requirement and has approval evidence? What will the next batch actually load? Can you recover the run behind that version?

## The incident brief

Harbor has inherited a trial selection made under an earlier acceptance rule. The client now requires validation RMSE at most `1.45` kWh. Three versions are present, but the newest is still pending. The receiving engineer needs a suitable prior approved artifact restored, with enough explanation to understand the decision and enough lineage to rebuild its result.

This is a transfer task, not a replay of the worked rollback. Inspect the prepared client's actual tags, source runs and metrics. Do not choose a version by counter, display name or an assumption that the last registered artifact was tested. Keep all artifacts and historical evidence available.

## Establish the before-condition

Prepare the supplied client state or inspect the equivalent real starting state. Record current `active`, its source run and the revised client rule before any change. Inventory all candidate versions with their validation status and source metric. Distinguish the old helper gate from the new client acceptance decision; both belong in the explanation.

Separately retain your cumulative project's registered → validated → active sequence. The client incident then tests whether you can use the same lifecycle concepts under changed conditions. Reusing the solved notebook's after-rollback state would remove the decision this checkpoint is intended to assess.

## Evidence Harbor needs

| Decision | Evidence the reviewer will inspect |
|---|---|
| Which artifact was registered? | Version identity, model source and source run |
| Why was selection allowed? | Validation status, actual test/metric rationale |
| Why must the trial be replaced? | Revised condition and trial's raw result |
| Which prior version qualifies? | Its approval evidence and result under the client rule |
| Did rollback affect the next job? | Before/after selection, helper event, newly resolved batch |
| Can its result be rebuilt? | Recoverable source/data/config/environment and reproduction comparison |

Your incident note should tell the story through these records, not simply state that `activate` returned successfully. A pending version may remain useful investigation material even when it is not eligible for selection.

## Submit a bounded incident conclusion

Preserve the current/previous selection evidence, the reasoned alias reassignment, incident metadata, new batch and original/new reproduction IDs. Explain which fields the event captured and which changes the helper log would miss. Do not claim that an already-running consumer necessarily reloaded its model or that the local log is immutable.

The final packet should allow another engineer to identify the chosen approved artifact, reproduce the recorded evaluation within `1e-6` kWh under matching lineage and inspect why it replaced the trial. If any of those links is missing, state and resolve the gap before treating the incident as complete.

## Making improvements

### Task A — Inspect the client handover

Prepare the client intake with `uv run python exercises/prepare-practice.py registry-assessment --state state-harbor-registry` from your project/helper root. This produces three registered artifacts, validation tags and a currently active trial; no rollback is done for you. The revised client limit is validation RMSE <= `1.45` kWh. Inspect all three versions and their source runs. Determine which previously approved version qualifies; the highest version number is not necessarily approved or active.

### Task B — Complete and reverse a lifecycle decision

Document a registered/tagged/active selection from your cumulative project. For the client state, record the current alias and validation evidence, reassign `active` to the qualifying prior version with a reason, retain all artifacts, and tag the trial incident. Capture old/new versions and source run in audit evidence. A new batch must prove the restored selection is actually used.

### Task C — Reproduce the approved result

Recover the selected version's source/data/config/environment/model lineage. Rebuild its evaluation in a new state and compare absolute RMSE within `1e-6` kWh. Name which clean-state layers you proved and what would remain to demonstrate a new environment. Explain the audit's helper-only, mutable and non-atomic limits.

## Final check

Submit an evidence index with actual file paths, run IDs and observed checks. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Submission boundaries

Return the three-version inspection table, before/after alias record, reasoned audit event, incident tag, new batch output/version evidence and approved-run reproduction report. The new numerical limit changes the client decision, not the taught registry operations. Keep the source snapshot and cumulative pipeline contracts unchanged.

## Learning outcome

Deliverable: a model registered, tagged with validation evidence, assigned the active-model alias, then rolled back by alias reassignment - with a documented audit trail and the lineage needed to reproduce the approved run within the tolerance declared in the clean-state verification specification.

## Summary

Harbor’s revised acceptance rule is connected to a preserved trial, a documented rollback and a reproducible approved result. Current selection and history have distinct evidence.
