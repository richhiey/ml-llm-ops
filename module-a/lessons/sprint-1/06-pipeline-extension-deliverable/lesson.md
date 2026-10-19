✂️
# Pipeline extension deliverable

Harbor Facilities sends a new supplier intake file with boundary values and several different contract violations. Your cumulative project must distinguish usable rows from invalid inputs, explain the responsible rules and preserve valid predictions.

**Notebook section:** **6 · Apply the contract to Harbor** in your [existing Sprint 1 notebook](../../../notebooks/01-pipeline-and-extension.ipynb). Read this page, then work through that section once. Keep answers in the same notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md) · [Optional Colab section](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=checkpoint-work).

## What you will work with

Open the [Harbor supplier intake](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/harbor-intake.csv), also available at `PACKAGE/exercises/harbor-intake.csv` in the notebook. Inspect it before applying the guard.

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md). The supplier file has exactly `row_id`, `temperature_c`, `hour` and `occupancy`; it has no historical target or partition. Keep its values and identifiers unchanged. Apply the feature guard directly rather than passing it to historical `ingest()` or training on it. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

| Intake field | Contract to apply |
|---|---|
| `temperature_c` | Inclusive `-30..50` |
| `hour` | Integer in `0..23` |
| `occupancy` | Inclusive `0..100` |

## As you work, keep these questions in mind

Which supplier rows should be rejected before training or inference? Can you explain the exact line responsible? Why does the original planning deadline favor your chosen inference pattern?

## Making improvements

### Task A — Validate an extension

Reuse your actual edited project, source diff and observed boundary/integration checks. Before running the guard on the new supplier input, classify each row as acceptable or rejected and name the rule. Test individual rows and the whole mixed intake with your loaded `project_guard`, preserving the raw data. A rejected intake must not be silently clipped or have bad rows dropped. Do not change the source snapshot or split.

### Task B — Explain the code

Reuse your explanation of each changed line, including reads, conditions, exception behavior, copies and returns. Include the existing diff and failing-before/passing-after record, plus your candidate review. You do not need a second code rewrite or a second explanation of the same lines.

### Task C — Choose inference

Recommend batch or real-time from the supplied 24-row/60-second brief. Address latency, throughput and resource cost, and name the observable completion evidence.

## Final check

Finish the checkpoint section in your sprint notebook and keep the same local project/output folder. Point to your existing contract-test result and edited batch CSV/metadata; do not rerun them merely to generate new IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. No new notebook, separate evidence report, registry setup, endpoint build or fresh-environment recovery is required for this checkpoint.

## Learning outcome

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## Summary

Harbor’s supplier change has been tested through an explained pipeline extension. The deliverable connects the code decision to observed contract and inference evidence.
