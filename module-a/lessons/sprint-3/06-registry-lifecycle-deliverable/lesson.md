✂️
# Registry lifecycle deliverable

Harbor Facilities hands over three model versions and a revised validation-error limit. A trial is active, and a newer artifact is still pending. Identify and restore a suitable prior approved version from the evidence, rather than assuming that “latest” means safe.

**Continue here:** [Sprint 3 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=checkpoint-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Which version meets the revised client requirement and has approval evidence? What will the next batch actually load? Can you recover the run behind that version?

## Making improvements

### Task A — Inspect the client handover

Prepare the client intake with `uv run python exercises/prepare-practice.py registry-assessment --state state-harbor-registry` from your project/helper root. This produces three registered artifacts, validation tags and a currently active trial; no rollback is done for you. The revised client limit is validation RMSE <= `1.45` kWh. Inspect all three versions and their source runs. Determine which previously approved version qualifies; the highest version number is not necessarily approved or active.

### Task B — Complete and reverse a lifecycle decision

Document a registered/tagged/active selection from your cumulative project. For the client state, record the current alias and validation evidence, reassign `active` to the qualifying prior version with a reason, retain all artifacts, and tag the trial incident. Capture old/new versions and source run in audit evidence. A new batch must prove the restored selection is actually used.

### Task C — Reproduce the approved result

Recover the selected version's source/data/config/environment/model lineage. Rebuild its evaluation in a new state and compare absolute RMSE within `1e-6` kWh. Name which clean-state layers you proved and what would remain to demonstrate a new environment. Explain the audit's helper-only, mutable and non-atomic limits.

## Final check

Finish the checkpoint section in your sprint notebook with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Learning outcome

Deliverable: a model registered, tagged with validation evidence, assigned the active-model alias, then rolled back by alias reassignment - with a documented audit trail and the lineage needed to reproduce the approved run within the tolerance declared in the clean-state verification specification.

## Summary

Harbor’s revised acceptance rule is connected to a preserved trial, a documented rollback and a reproducible approved result. Current selection and history have distinct evidence.
