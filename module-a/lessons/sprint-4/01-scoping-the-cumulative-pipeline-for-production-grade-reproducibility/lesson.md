✂️
# Scoping the cumulative pipeline for production-grade reproducibility

Linden Facilities has separate pipeline, tracking and registry evidence. The remaining work is to make one handoff that another engineer can run and verify without your notebook state.

**Continue here:** [Sprint 4 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb#scrollTo=handoff-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Inspect your current project against the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md), explained extension diff and lifecycle evidence. A **scope inventory** distinguishes demonstrated behavior from planned work; do not count a README promise as an executed check.

| Final criterion | Your scope record |
|---|---|
| Connected lifecycle | Observed evidence or explicit gap |
| Recoverable setup | Dependency and next verification command |
| Explained extension | Accepted/rejected examples and unchanged-stage proof |

## Your task

Add a scope table in this notebook with each final criterion, existing evidence, missing work, dependency and next verification command. Include train → track → register → select active → infer, connected lineage, setup, fresh-state proof and a non-trivial explained extension.

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

## Learning outcome

Continue the pipeline built across Sprints 1-3 and scope the remaining work needed to meet the final criteria. A T4 (AI track) model may replace the baseline model only as a deliberate transfer test inside the same scaffold.

## Summary

Your scope separates demonstrated behavior from missing proof. The final project can now focus on completing the cumulative handoff within the existing interfaces.
