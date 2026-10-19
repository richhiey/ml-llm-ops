✂️
# Reproducible pipeline deliverable

Harbor Facilities is the receiving team for your completed cumulative pipeline. Its receiving engineer uses an independent environment and an input with occupancy=101 to check whether your handoff is trustworthy.


## Work in the repository

Reuse the actual receiving result and handoff note. In that receiving environment, probe a copy containing `occupancy=101` with the taught guard/API; expect rejection without changing the original data. Check the complete lifecycle and lineage from existing records rather than build it again. After validation-based selection is fixed, observe the reserved final partition once using `uv run linden-mlops final` in the original cumulative project. Keep this observation separate from promotion and do not retune. This checkpoint is for your own verification; there is nothing to submit.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Can the receiving engineer run your written commands without your help? Does the active version produce the delivered CSV? Does your extension reject a new invalid input while preserving valid behavior?

## Making improvements

### Task A — Inspect the connected system

Inspect the existing cumulative train → track → register → select active → batch pipeline, with at least one non-trivial validated extension and a line-by-line explanation. The optional T4 estimator transfer stays inside the same interfaces and has separately established validation evidence.

### Task B — Hand over a recoverable package

Include source revision/archive, fixed data/hash, exact config, Python/package/lock environment, model artifact/source run, setup/run commands and accepted evidence. Give the receiving engineer the declared clean starting state, not your running notebook.

### Task C — Prove clean execution and serving

Execute the handoff in a new source folder, environment and state. Compare lineage and RMSE within 1e-6 kWh. Prove 24 aligned finite predictions within 60 seconds from the intended active version. Show occupancy=101 is rejected and explain the stage responsible. Diagnose all divergence before claiming completion.

## Final check

Check your existing working notes with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before relying on them. Use only previously practiced interfaces; no new platform is required.

## Learning outcome

Deliverable: the cumulative end-to-end pipeline (train -> track -> register -> select active version -> exercise the selected inference path) reproduced from the declared clean state, with traceable code/data/configuration/environment lineage, reproducible setup/run instructions, inference evidence, and at least one non-trivial extension documented and explained.

## Summary

Harbor can inspect the explained extension, rebuild the connected lifecycle and verify the selected batch. The working package makes each acceptance claim traceable to an actual artifact or execution.
