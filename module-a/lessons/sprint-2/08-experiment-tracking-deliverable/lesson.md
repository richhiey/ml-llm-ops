✂️
# Experiment tracking deliverable

Harbor Facilities wants to know which configuration it should promote and why. You will hand over a controlled comparison and a checked assistant recommendation. A separate training-error observation will test whether your report keeps different evaluation questions apart.

**Continue here:** [Sprint 2 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb#scrollTo=checkpoint-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Would a second engineer rank the same five runs from the raw table? Which assistant claims follow those records, and which go beyond them? What changes when the evaluation rows change?

## Making improvements

### Task A — Track controlled configurations

Log at least five distinct declared configurations in MLflow with fixed data/split/evaluation conditions. Retain matrix and raw run IDs, parameters, primary/diagnostic metrics and model artifacts. Retain an actual autolog `training_root_mean_squared_error` observation with its source run, label its training-row basis, and explain why it cannot replace `rmse_kwh` in the validation ranking. Do not invent a copied score. Keep the final partition unopened until the selected configuration reaches the final handoff.

### Task B — Demonstrate autologging

Show the enabled setup and at least one actual autolog-specific field alongside the explicit validation metric. Explain convenience versus control. Compare five runs in the MLflow UI and keep a verifiable inspection record.

### Task C — Validate assistant advice

Direct an approved assistant using the raw table and metric rule. Preserve prompt, input and response. Validate every recommendation against raw MLflow fields, flag errors/unsupported claims, and produce a corrected configuration-to-promote recommendation with run ID.

## Final check

Finish the checkpoint section in your sprint notebook with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Learning outcome

Deliverable: at least 5 experiment configurations logged and compared in MLflow, an autologging setup, and an AI-assisted summary recommending which configuration to promote - with the summary validated against raw data.

## Summary

Harbor receives a recommendation supported by controlled runs, actual logging evidence and a checked assistant response. The original response remains available beside its corrections.
