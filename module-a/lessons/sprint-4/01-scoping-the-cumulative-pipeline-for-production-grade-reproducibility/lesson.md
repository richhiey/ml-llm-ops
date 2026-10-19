✂️
# Scoping the cumulative pipeline for production-grade reproducibility

Linden Facilities has separate pipeline, tracking and registry evidence. The remaining work is to make one handoff that another engineer can run and verify without your notebook state.

## Your route through this lesson

Inventory actual proof, prioritize a blocking repair and bound any estimator transfer. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** A dependency-ordered scope record with one essential action and a justified deferral.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=handoff-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Inspect your current project against the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md), explained extension diff and lifecycle evidence. A **scope inventory** distinguishes demonstrated behavior from planned work; do not count a README promise as an executed check.

| Final criterion | Your scope record |
|---|---|
| Connected lifecycle | Observed evidence or explicit gap |
| Recoverable setup | Dependency and next verification command |
| Explained extension | Accepted/rejected examples and unchanged-stage proof |

## Begin with a receiver's questions

Inventory your actual project, not the reference notebook's outputs. Can someone find the chosen configuration? Can they locate its source and data? Can they run the connected lifecycle? Can they explain your changed validation stage? Can they repeat the result without your live notebook? These questions distinguish a finished component from a handoff ready for another engineer.

A **dependency** is work that must be completed before another task can be meaningfully verified. For example, you cannot prove an independently recoverable handoff before retaining the source/model artifacts it names. Listing “add monitoring” beside “export missing source” without priority hides that difference.

## Build an inventory you can act on

For each criterion, record one of `observed`, `missing` or `proposed`. An observed item needs a locator and what that item proves. A screenshot of an active alias does not prove fresh-environment reproduction; a passing stage test does not prove that inference calls the edited stage. Keep the claim as narrow as the observation.

| Inventory entry | Why it needs revision |
|---|---|
| “Tracking done” | Name the selected run and which fields/artifacts exist |
| “Reproducible because there is a lock” | Source/data/config and an actual clean execution remain unproven |
| “Extension: changed a comment” | No behavior or meaningful invariant changed |
| “Stage guard added; invalid occupancy rejected; valid metrics unchanged” | Useful bounded behavior with specific proof to retain |

Do not manufacture a second feature just to make the project look larger. The validated stage addition is a non-trivial extension when its actual logic, input/output contract, rejected cases and regression evidence are explained. Decide whether its proof is complete before selecting another feature.

## Prioritize the next investigation

Choose the missing item that blocks the receiver most directly. Name the smallest action that resolves it and the command or observation that would prove the repair. Then identify one attractive addition you will defer. A dashboard may be useful later, but it does not recover an absent model artifact or connect a mismatched source run.

For the optional T4 path, inspect compatibility before committing to transfer: same feature order and target, fitted `predict` interface, serializable fitted state, explicit loading requirements and separately pinned dependencies. A model that needs a different dataset or serving stack falls outside this bounded option. Do not mix its scores into the alpha-only experiment.

## Finish with an executable work order

Arrange your remaining tasks in dependency order and identify a final receiving check. The output should let you start work immediately: a gap, why it matters, its dependency, its next action and its acceptance evidence. Keep “proposed” visible until a check has actually run. A smaller project with complete, inspectable proof is more useful here than an inventory full of unsupported feature claims.

## Your task

Use the [scope starter](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/project-scope-starter.csv) to create `project-scope.md` with each final criterion, existing evidence, missing work, dependency and next verification command. Include train → track → register → select active → infer, connected lineage, setup, fresh-state proof and a non-trivial explained extension.

Keep the cumulative case and contracts. Decide whether your validated input stage is sufficient or needs another bounded invariant/report. Name accepted and rejected examples and how you will prove unchanged stages still run. Prioritize missing proof before adding features.

The optional T4 transfer path replaces only the baseline estimator inside `train`, using a compatible fitted `predict` interface. Keep feature/target schema, split, primary metric, logging, registry and selected batch contract. Pin any added dependencies, establish a new reference result under the declared reproducibility contract and rerun representative valid/invalid inputs and the full lifecycle. Do not mix its scores with the original alpha-only comparison. If your prior model needs an unrelated dataset or serving stack, choose the baseline path for this project.

## Working with documentation

Use [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md) to separate stable interfaces from a model-specific implementation detail. Read the code where an inventory claim depends on behavior.

## Hints

1. Mark each item “observed”, “missing” or “proposed” with a concrete evidence locator.
2. A new model can fit the scaffold only if its inputs/outputs preserve the same contract.
3. Reserve time for a second engineer's clean run; it is part of the deliverable.

## Checkpoints

Every final requirement has a proof plan. No new orchestration framework, external service or Module B dependency is needed. A peer can distinguish an actual result from an assumption by reading your inventory.

## Choose the smallest remaining work

Rank your gaps by whether they prevent another engineer from validating the handoff. Choose one essential repair and one tempting addition to defer; justify each from a missing evidence item. For a T4 transfer, first check the estimator's fitted `predict` output shape, serializability and dependency/model-loading requirements. Update the helper's model requirements as well as the lock if the replacement needs another library. Keep the declared course tolerance unless the instructor approves and records a justified transfer-specific contract before execution.

## Learning outcome

Continue the pipeline built across Sprints 1-3 and scope the remaining work needed to meet the final criteria. A T4 (AI track) model may replace the baseline model only as a deliberate transfer test inside the same scaffold.

## Summary

Your scope separates demonstrated behavior from missing proof. The final project can now focus on completing the cumulative handoff within the existing interfaces.
