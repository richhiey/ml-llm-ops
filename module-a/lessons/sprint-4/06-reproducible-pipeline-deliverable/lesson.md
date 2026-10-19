✂️
# Reproducible pipeline deliverable

Harbor Facilities is the receiving team for your completed cumulative pipeline. Its acceptance reviewer will use an independent environment and an input with occupancy=101 to check whether your handoff is trustworthy.

**Continue here:** [Sprint 4 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb#scrollTo=checkpoint-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Can the receiving engineer run your written commands without your help? Does the active version produce the submitted CSV? Does your extension reject a new invalid input while preserving valid behavior?

## Making improvements

### Task A — Submit the connected system

Deliver the existing cumulative train → track → register → select active → batch pipeline, with at least one non-trivial validated extension and a line-by-line explanation. The optional T4 estimator transfer stays inside the same interfaces and has separately established validation evidence.

### Task B — Hand over a recoverable package

Include source revision/archive, fixed data/hash, exact config, Python/package/lock environment, model artifact/source run, setup/run commands and accepted evidence. Give the reviewer the declared clean starting state, not your running notebook.

### Task C — Prove clean execution and serving

Execute the handoff in a new source folder, environment and state. Compare lineage and RMSE within 1e-6 kWh. Prove 24 aligned finite predictions within 60 seconds from the intended active version. Show occupancy=101 is rejected and explain the stage responsible. Diagnose all divergence before claiming completion.

## Final check

Finish the checkpoint section in your sprint notebook with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Learning outcome

Deliverable: the cumulative end-to-end pipeline (train -> track -> register -> select active version -> exercise the selected inference path) reproduced from the declared clean state, with traceable code/data/configuration/environment lineage, reproducible setup/run instructions, inference evidence, and at least one non-trivial extension documented and explained.

## Summary

Harbor can inspect the explained extension, rebuild the connected lifecycle and verify the selected batch. The submission makes each acceptance claim traceable to an actual artifact or execution.
