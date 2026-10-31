✂️
# Proving the selected serving path uses the active version

Linden Facilities has a selected operational model and evidence of why it was chosen. The next planner batch must actually load that version. An old output file cannot establish what a job after the response will serve.

## Inspect the observed response first

Continue the same cumulative source and workspace. Reuse your observed drift-trigger-response cycle when its source, policy, inputs and selected model still match. There is no requirement to retrain again merely to create a new report. If an element is missing, complete that bounded part using the already taught [operational interfaces](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md).

Before acting, write the signal, threshold and action supported by the retained evidence. Distinguish the unlabeled shift from the later independent labeled observation. Identify the candidate's training rows and the validation IDs used for both model errors. Explain why the decision was to promote, retain or recover, and what evidence would have justified a different response. Keep the original and feedback final rows outside this decision.

If your event concerns an already active unsuitable version, use the taught rollback route and a suitable approved replacement. Rejecting a candidate that was never active is not rollback. Retain failed comparisons instead of deleting an inconvenient result.

## Your task

1. Inventory the before/after model versions, actual source run, policy/report/data hashes and comparison decision. Separate observed facts from a proposed next action.
2. Predict the version that a new inference job should load. Invoke `batch_predict` with an explicit workspace and a distinct output name for the response, using the [API reference](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md).
3. Inspect the raw CSV and job metadata independently: `24` unique IDs in input order, finite predictions, matching input hash, matching intended run/version, and complete job time within `60` seconds. Calculate throughput as rows divided by elapsed seconds. This measures delivery, not training/setup time or business cost.
4. Prepare a separate invalid-input copy, predict the result, invoke the same application route with the intended workspace explicitly, and retain the rejection. Valid input must still succeed; rejection alone is not evidence of a useful pipeline.
5. Start the incident note in the existing `HANDOFF.md`: observation/action times, affected version, chosen response, resulting state, verification and one follow-up owner.

Your useful output is the complete planner CSV and its job record. Save the small independent CSV/metadata inspection in your own operational check script so another engineer can repeat it on a new job. Give it the input/output paths; do not hard-code a lesson ID or accept a report's `passed` field as its result.

A supplied synthetic intake stays labeled as such. Use your own observed run/version IDs; a reference picture or passing helper flag cannot replace the raw evidence.

## Hints

<details><summary>Look for the job after the decision</summary>

The alias describes selection. A fresh job's `resolved_version` and source `run_id` show which model that job loaded. Old output values can look plausible even when they came from a different version.

</details>

## Checkpoints

One observed operational cycle is connected to a newly verified batch from its resulting intended version. Contract rejection evidence is retained separately. Your explanation distinguishes distribution change, measured error, response acceptance and delivery correctness.

<details><summary>Check after recording the action and inspecting the output</summary>

**Result you should get:** the new job and current alias identify the intended artifact, with ordered finite output inside the delivery budget. The separate invalid-input probe rejects before a successful output is claimed.

**How:** compare raw registry/run/job records, inspect every output row against input IDs, and independently check values and elapsed time. If the job is stale or resolves another version, retain the mismatch, repair selection or invocation and execute a new job. Correct any incident claim of rollback when the candidate was never active.

</details>

## Learning outcome

Exercise a bounded drift-trigger-response cycle in the cumulative system, justify the response using the declared policy, and verify that a fresh inference job uses the resulting intended active model version and meets the inference brief.

## Summary

The handoff now includes proof that the intended version served after the operational decision, alongside the evidence explaining that response.
