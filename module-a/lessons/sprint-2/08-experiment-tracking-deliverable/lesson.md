✂️
# Experiment tracking deliverable

Harbor Facilities wants to know which configuration it should promote and why. You will hand over a controlled comparison and a checked assistant recommendation. A separate training-error observation will test whether your report keeps different evaluation questions apart.

## Your route through this lesson

Give the client one connected comparison and an inspected assistant recommendation. Use your cumulative project and the supplied client inputs. Plan and perform the taught work independently. Keep the starting state and actual evidence; the reviewer uses separate validation material.

**Finish with:** Five-run/UI/autolog evidence plus an actual assistant record and validated recommendation.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=checkpoint-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## What you will work with

Use your cumulative helper project, its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Would a second engineer rank the same five runs from the raw table? Which assistant claims follow those records, and which go beyond them? What changes when the evaluation rows change?

## The client decision

Harbor's reviewer needs to decide which configuration is worth carrying into lifecycle validation. A favorable score or fluent assistant paragraph is insufficient: the reviewer must be able to reconstruct which runs were compared, why their conditions are comparable and how the recommendation follows the declared metric.

This checkpoint combines the matrix design, pipeline-integrated logging, UI comparison, autologging investigation and assistant claim review. Keep those components connected to your own selected executions. Do not combine a reference screenshot, an unrelated CSV and a fresh recommendation as though they came from one experiment population.

## Freeze the decision rule before execution

Use your five distinct planned configurations, the fixed snapshot and validation partition. Record the factor varied, anchor, controls, metric and direction before seeing results. Retain actual returned run IDs after execution. If the store contains earlier runs, define the selected population explicitly and keep excluded observations separately labeled.

Use an actual autologged training-error observation to test the boundary between fitting diagnostics and held-out selection. Keep its source run and metric name. The reserved final partition stays unopened until the selected configuration reaches the final handoff; this checkpoint does not spend it to manufacture an invalid comparison.

## What to hand to the reviewer

| Component | Observable completion |
|---|---|
| Plan and raw selected table | Five distinct configurations with fixed controls and actual IDs |
| Tracking/model records | Parameters, declared metrics and fitted artifacts trace to those runs |
| UI inspection | Actual five-run comparison, displayed metric and full selected IDs |
| Autologging | Configuration plus an observed autolog-specific field and interpretation |
| Assistant record | Exact prompt, input and actual response, kept unchanged |
| Claim review | Every recommendation checked, inaccuracies/unsupported claims flagged |
| Corrected recommendation | Actual run/config, primary metric and bounded justification |

The reviewer should be able to open a recommended run and inspect its original metric rather than trust the number copied into your prose. They should also be able to identify which claims still need serving or reproduction evidence.

## Keep incomplete work visible

If assistant access fails, preserve the failure and use the saved response for rehearsal, but mark the required new request incomplete. If the UI was not inspected, an API sort does not complete that part. If a run failed, preserve its status and explain why it is outside the finished comparison population.

You do not need to make the original response look perfect. A strong submission can identify a wrong winner or an overclaim, support the correction with raw fields and state a more defensible recommendation. Finish by checking that all evidence paths and IDs point to the same intended experiment group.

## Making improvements

### Task A — Track controlled configurations

Log at least five distinct declared configurations in MLflow with fixed data/split/evaluation conditions. Retain matrix and raw run IDs, parameters, primary/diagnostic metrics and model artifacts. Retain an actual autolog `training_root_mean_squared_error` observation with its source run, label its training-row basis, and explain why it cannot replace `rmse_kwh` in the validation ranking. Do not invent a copied score. Keep the final partition unopened until the selected configuration reaches the final handoff.

### Task B — Demonstrate autologging

Show the enabled setup and at least one actual autolog-specific field alongside the explicit validation metric. Explain convenience versus control. Compare five runs in the MLflow UI and keep a verifiable inspection record.

### Task C — Validate assistant advice

Direct an approved assistant using the raw table and metric rule. Preserve prompt, input and response. Validate every recommendation against raw MLflow fields, flag errors/unsupported claims, and produce a corrected configuration-to-promote recommendation with run ID.

## Final check

Submit an evidence index with actual file paths, run IDs and observed checks. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Acceptance packet

Submit the pre-run matrix; selected run-ID file; raw selected table; a separate excluded-observation record; actual five-run UI inspection; autolog field evidence; exact assistant prompt/input/response; and the claim validation/corrected recommendation. Your recommendation must identify a configuration/run, but it need not be the reference alpha if you declared a different controlled matrix. A saved response is useful rehearsal if access fails; it does not demonstrate that you directed an approved assistant in this assessment.

## Learning outcome

Deliverable: at least 5 experiment configurations logged and compared in MLflow, an autologging setup, and an AI-assisted summary recommending which configuration to promote - with the summary validated against raw data.

## Summary

Harbor receives a recommendation supported by controlled runs, actual logging evidence and a checked assistant response. The original response remains available beside its corrections.
