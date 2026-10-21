✂️
# Registry lifecycle deliverable

Harbor Facilities hands over three model versions and a revised validation-error limit. A trial is active, and a newer artifact is still pending. Identify and restore a suitable prior approved version from the evidence, rather than assuming that “latest” means safe.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb) in your local project environment. Find the section for **Registry lifecycle deliverable** using its Campus activity ID **A-S3-06**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Prepare Harbor's separate intake once:

```sh
uv run linden-mlops prepare --case registry-assessment --state work/harbor-registry
uv run linden-mlops inspect --state work/harbor-registry
```

Use the known CLI/API operations to investigate and resolve the revised `1.45` kWh limit. Supply explicit `--state work/harbor-registry` for its alias, batch and reproduction operations; use the actual version/run IDs. Retain the main cumulative selection. Preparation performs no recovery decision. There is nothing to submit.


## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Which version meets the revised client requirement and has approval evidence? What will the next batch actually load? Can you recover the run behind that version?

## Quick diagnosis

Before changing the alias, make a three-row inventory with each actual version ID, source run ID, validation RMSE, approval status and current alias. State which version Harbor should serve under the revised requirement and why the other two do not qualify. Commit to that prediction before executing the rollback.

## Making improvements

### Task A — Inspect the client handover

Prepare the separate Harbor intake using the command above. This produces three registered artifacts, validation tags and a currently active trial; no rollback is done for you. The revised client limit is validation RMSE <= `1.45` kWh. Inspect all three versions and their source runs. Determine which previously approved version qualifies; the highest version number is not necessarily approved or active.

### Task B — Complete and reverse a lifecycle decision

Document a registered/tagged/active selection from your cumulative project. For the client state, record the current alias and validation evidence, reassign `active` to the qualifying prior version with a reason, retain all artifacts, and tag the trial incident. Capture old/new versions and source run in audit evidence. A new batch must prove the restored selection is actually used.

### Task C — Reproduce the approved result

Recover the selected version's source/data/config/environment/model lineage. Rebuild its evaluation in a new state and compare absolute RMSE within `1e-6` kWh. Name which clean-state layers you proved and what would remain to demonstrate a new environment. Explain the audit's helper-only, mutable and non-atomic limits.

## Final check

Check your existing working notes with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before relying on them. Use only previously practiced interfaces; no new platform is required.

## Check your recovery after the attempt

<details>
<summary>Solution — approved rollback and its proof</summary>

**Result you should get:** the source run configured with `alpha=0.1` is the previously approved version that meets validation RMSE `<=1.45` kWh. The active `alpha=10` trial fails the revised threshold even though it passed the earlier approval policy. The newer `alpha=100` artifact is pending; “newest” provides neither approval nor suitability. Use the actual version/run IDs returned in your state rather than assuming version counters.

After recovery, `active` resolves to the qualifying prior version, all three artifacts remain and the trial has an incident tag. The audit names the observed old and new versions, reason and time. A new batch names the restored version and source run, produces `24` aligned finite outputs and meets the completion budget. Reproduction matches the chosen version's invariant lineage and absolute validation RMSE delta `<=1e-6` kWh. A new-store replay alone does not prove a fresh source/environment test.

**How:** join each registry version to its source run and approval tags, then apply the revised client threshold to the validation metric. Compare the pre-action alias with the rollback event and post-action alias. Inspect the new batch metadata instead of treating an alias command's success as inference evidence. Compare the reproduced run's recorded recipe and evaluation with the same approved source run; timestamps and run IDs may change.

If the batch names the trial, check whether it was created before the reassignment or against the wrong `--state`. If the newest pending artifact was chosen, restore the approval requirement before moving the alias again. Preserve the failed evidence and reason for correction. The helper's mutable, non-atomic local audit records its own operations; it cannot prove that all possible out-of-band changes were captured.

</details>

## Learning outcome

Deliverable: a model registered, tagged with validation evidence, assigned the active-model alias, then rolled back by alias reassignment - with a documented audit trail and the lineage needed to reproduce the approved run within the tolerance declared in the clean-state verification specification.

## Summary

Harbor’s revised acceptance rule is connected to a preserved trial, a documented rollback and a reproducible approved result. Current selection and history have distinct evidence.
