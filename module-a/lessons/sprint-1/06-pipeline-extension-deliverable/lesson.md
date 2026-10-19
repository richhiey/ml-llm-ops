✂️
# Pipeline extension deliverable

Harbor Facilities sends a new supplier intake file with boundary values and several different contract violations. Your cumulative project must distinguish usable rows from invalid inputs, explain the responsible rules and preserve valid predictions.

**Continue here:** [Sprint 1 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=checkpoint-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## What you will work with

Open the [Harbor supplier intake](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/harbor-intake.csv), also available at `PACKAGE/exercises/harbor-intake.csv` in the notebook. Inspect it before applying the guard.

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

| Intake field | Contract to apply |
|---|---|
| `temperature_c` | Inclusive `-30..50` |
| `hour` | Integer in `0..23` |
| `occupancy` | Inclusive `0..100` |

## As you work, keep these questions in mind

Which supplier rows should be rejected before training or inference? Can you explain the exact line responsible? Why does the original planning deadline favor your chosen inference pattern?

## Making improvements

### Task A — Validate an extension

Deliver a real validation-stage addition in your project copy, with input/output contract, accepted and rejected examples, boundary checks and unchanged-stage regression evidence. Use the fractional-hour supplier change to test transfer; do not change the source snapshot or split.

### Task B — Explain the code

Annotate every changed line, including reads, conditions, exception behavior, copies and returns. Explain at least one correction required in generated code. Include the diff and the failing-before/passing-after case.

### Task C — Choose inference

Recommend batch or real-time from the supplied 24-row/60-second brief. Address latency, throughput and resource cost, and name the observable completion evidence.

## Final check

Finish the checkpoint section in your sprint notebook with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Learning outcome

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## Summary

Harbor’s supplier change has been tested through an explained pipeline extension. The deliverable connects the code decision to observed contract and inference evidence.
