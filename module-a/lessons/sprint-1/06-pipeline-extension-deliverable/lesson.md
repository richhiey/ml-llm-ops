✂️
# Pipeline extension deliverable

Harbor Facilities sends a new supplier intake file with boundary values and several different contract violations. Your cumulative project must distinguish usable rows from invalid inputs, explain the responsible rules and preserve valid predictions.

## Your route through this lesson

Apply the validated extension and inference decision to the client intake. Use your cumulative project and the supplied client inputs. Plan and perform the taught work independently. Keep the starting state and actual evidence; the reviewer uses separate validation material.

**Finish with:** Supplier classifications, observed contract/regression results and justified serving proof.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=checkpoint-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## What you will work with

Use your cumulative helper project, its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

| Intake field | Contract to apply |
|---|---|
| `temperature_c` | Inclusive `-30..50` |
| `hour` | Integer in `0..23` |
| `occupancy` | Inclusive `0..100` |

## As you work, keep these questions in mind

Which supplier rows should be rejected before training or inference? Can you explain the exact line responsible? Why does the original planning deadline favor your chosen inference pattern?

## The client brief

Harbor wants to reuse your pipeline for a supplier's planning inputs. The supplier file contains a mixture of usable rows and contract violations. Harbor must not receive a file where invalid measurements were silently clipped or rows disappeared. It also needs to know whether batch delivery fits the original planning deadline.

This checkpoint brings together skills already practiced: extending the bounded guard, explaining changed statements, testing accepted/rejected inputs, preserving valid behavior and justifying an inference pattern. It does not ask for a new model family or a new serving stack. Use your own edited project, not the untouched solved helper as a substitute for an extension.

## Start without a hidden solution state

Keep the source snapshot and planned representative batch unchanged. Save the Harbor intake separately. Before running any supplier probe, make a classification table containing each `row_id`, your predicted acceptance decision and the responsible contract. Then execute the individual probes and compare predicted versus observed behavior. You decide which test distinguishes a range failure, integer-hour failure and caller mutation.

A mixed input is one request under the current whole-batch contract. Preserve the raw file, and do not “fix” it by dropping rejected rows before testing. Test individual rows separately when investigating which rules they exercise. Those investigations do not turn the mixed request into a valid one.

## Deliver a reviewable package

| Item | What the reviewer should be able to establish |
|---|---|
| Changed source and diff | A real bounded stage addition exists and is reached |
| Statement-level explanation | You understand reads, checks, exceptions, copies and returns |
| Probe table and outputs | Predictions were tested against accepted, boundary and invalid examples |
| Regression evidence | Valid features/index and downstream results remain consistent |
| Inference decision | Pattern follows input arrival, delivery time, throughput and resource obligations |
| Representative batch | 24 aligned predictions and actual completion evidence |

Use real output from your project. IDs and timing will differ from examples. Explain what each file proves so the reviewer does not have to infer the claim from a screenshot.

## Check readiness before submission

A reviewer should be able to choose an additional boundary probe and ask you to point to the statement that determines its result. If you can only repeat the assistant's explanation, revisit the function and probes. If the reference helper passes but your project does not, the project remains incomplete.

Your short serving recommendation should explain why the actual 24-row/60-second brief favors the chosen pattern and what measurement would establish success. Keep the hypothetical request-serving alternative separate from implemented evidence. Submit the evidence first, then a bounded conclusion about what the pipeline can now do for Harbor.

## Making improvements

### Task A — Validate an extension

Deliver a real validation-stage addition in your project copy, with input/output contract, accepted and rejected examples, boundary checks and unchanged-stage regression evidence. Use the fractional-hour supplier change to test transfer; do not change the source snapshot or split.

### Task B — Explain the code

Annotate every changed line, including reads, conditions, exception behavior, copies and returns. Explain at least one correction required in generated code. Include the diff and the failing-before/passing-after case.

### Task C — Choose inference

Recommend batch or real-time from the supplied 24-row/60-second brief. Address latency, throughput and resource cost, and name the observable completion evidence.

## Final check

Submit an evidence index with actual file paths, run IDs and observed checks. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Supplier acceptance evidence

Use [Harbor intake](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/harbor-intake.csv). Before running it, label each `row_id` as accepted or rejected under the existing contract and name the field/rule. Submit your predictions, then the observed results. A mixed batch must reject rather than silently drop bad rows. Keep the original intake unchanged; use separate requests when testing individual rows. Also retain the representative `24`-row batch proof and explain your serving decision from the original deadline.

## Learning outcome

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## Summary

Harbor’s supplier change has been tested through an explained pipeline extension. The deliverable connects the code decision to observed contract and inference evidence.
