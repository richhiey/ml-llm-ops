✂️
# Reproducible pipeline deliverable

Harbor Facilities is the receiving team for your completed cumulative pipeline. Its acceptance reviewer will use an independent environment and an input with occupancy=101 to check whether your handoff is trustworthy.

## Your route through this lesson

Submit the connected system for an independent receiving run and contract probe. Use your cumulative project and the supplied client inputs. Plan and perform the taught work independently. Keep the starting state and actual evidence; the reviewer uses separate validation material.

**Finish with:** Recoverable final package with explained extension, connected serving and clean-reproduction proof.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=checkpoint-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## What you will work with

Use your cumulative helper project, its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

Can the receiving engineer run your written commands without your help? Does the active version produce the submitted CSV? Does your extension reject a new invalid input while preserving valid behavior?

## What Harbor is accepting

Harbor is accepting a runnable, explainable handoff. Its engineer will start from the declared clean state, execute your instructions and judge the resulting identities, evaluation and output. Your authoring notebook and an old successful model object will not be available as hidden dependencies.

The assessed skill is the cumulative infrastructure work: a bounded extension, controlled configuration, connected lifecycle, selected serving path and recoverable reproduction. No new platform or first-time technique is required here. The optional T4 estimator is acceptable only inside the same interfaces with its own established validation/dependency evidence.

## Package the claim and its proof together

| Claim | Evidence to include |
|---|---|
| The extension changes meaningful behavior | Source diff, statement explanation, failing-before/passing-after probes |
| This is the selected configuration | Controlled comparison and corrected recommendation |
| One run reaches registration and serving | Run/model/version/active/batch identity chain |
| Another engineer can reconstruct the recipe | Source/data/config/environment/model package and exact commands |
| Rebuilding agrees with the original | Invariant comparison and absolute RMSE delta |
| The planner receives a usable result | Aligned finite 24-row CSV and completion/version evidence |

Put an evidence index at the package entry point. Use locators that survive relocation and explain the purpose of each file. Preserve original and new manifests, not only a screenshot saying the run passed. Export model/reproduction artifacts while they are still accessible from the original store.

## Prepare for an independent receiving run

Test your final instructions in a new source folder and locked environment, with no inherited tracking store or notebook variables. Keep the original comparison record and the complete result of the receiving run. The receiving engineer should be able to inspect an invalid occupancy probe and choose an additional boundary case from the taught contract without being coached through the code.

State the contract before the check: valid rows are preserved; invalid requests reject; the active version is resolved at the job's start; a complete valid batch must finish within 60 seconds. Numerical reproduction uses absolute RMSE difference <= `1e-6` kWh and matching recorded lineage. These are separate acceptance conditions, so passing one cannot hide failure of another.

## Decide whether the package is ready

Before submitting, follow every named path, rerun the documented command and ask whether the report depends on knowledge only you have. Correct the package when a receiving attempt reveals a missing step, then repeat in a new destination. Retain the failed attempt and diagnosis as evidence of the correction.

Conclude with a precise statement of what was demonstrated and any unresolved limitation. A useful handoff makes gaps inspectable. An unexplained mismatch, missing artifact or undocumented manual repair means the clean handoff is not yet established, even when individual components worked earlier.

## Making improvements

### Task A — Submit the connected system

Deliver the existing cumulative train → track → register → select active → batch pipeline, with at least one non-trivial validated extension and a line-by-line explanation. The optional T4 estimator transfer stays inside the same interfaces and has separately established validation evidence.

### Task B — Hand over a recoverable package

Include source revision/archive, fixed data/hash, exact config, Python/package/lock environment, model artifact/source run, setup/run commands and accepted evidence. Give the reviewer the declared clean starting state, not your running notebook.

### Task C — Prove clean execution and serving

Execute the handoff in a new source folder, environment and state. Compare lineage and RMSE within 1e-6 kWh. Prove 24 aligned finite predictions within 60 seconds from the intended active version. Show occupancy=101 is rejected and explain the stage responsible. Diagnose all divergence before claiming completion.

## Final check

Submit an evidence index with actual file paths, run IDs and observed checks. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before submission. Use only previously practiced interfaces; no new platform is required.

## Independent receiving check

The receiving reviewer will execute your documented command from a new source folder/environment/state and submit a separate input-contract probe. Retain your own pre-run classification and the actual rejection without changing the probe file. The reviewer must be able to inspect one original-to-new lineage comparison, one connected active-version batch and the explained extension diff. Neither a pre-existing model prediction nor a README alone proves the handoff was rebuilt.

## Learning outcome

Deliverable: the cumulative end-to-end pipeline (train -> track -> register -> select active version -> exercise the selected inference path) reproduced from the declared clean state, with traceable code/data/configuration/environment lineage, reproducible setup/run instructions, inference evidence, and at least one non-trivial extension documented and explained.

## Summary

Harbor can inspect the explained extension, rebuild the connected lifecycle and verify the selected batch. The submission makes each acceptance claim traceable to an actual artifact or execution.
