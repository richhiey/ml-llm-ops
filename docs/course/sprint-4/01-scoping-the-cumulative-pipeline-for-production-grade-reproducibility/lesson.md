✂️
# Scoping the cumulative pipeline for production-grade reproducibility

Linden Facilities has separate pipeline, tracking and registry evidence. The remaining work is to make one handoff that another engineer can run and verify without your working notes state.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Scoping the cumulative pipeline for production-grade reproducibility** using its Campus activity ID **A-S4-01**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Start with `uv run linden-mlops status` and inspect existing source, selection, registry and batch files. Make your scope inventory before running more pipeline work. Keep it in one local `work/HANDOFF.md` that you will improve as you go. Reuse the validated extension and previous evidence; choose only gaps that remain.


## Starting point

Inspect your current project against the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md), explained extension diff and lifecycle evidence. A **scope inventory** distinguishes demonstrated behavior from planned work; do not count a README promise as an executed check.

| Final criterion | Your scope record |
|---|---|
| Connected lifecycle | Observed evidence or explicit gap |
| Recoverable setup | Dependency and next verification command |
| Explained extension | Accepted/rejected examples and unchanged-stage proof |

## Your task

Add a scope table in your working notes with each final criterion, existing evidence, missing work, dependency and next verification command. Include train → track → register → select active → infer, connected lineage, setup, fresh-state proof and a non-trivial explained extension.

Keep the cumulative case and contracts. Decide whether your validated input stage is sufficient or needs another bounded invariant/report. Name accepted and rejected examples and how you will prove unchanged stages still run. Prioritize missing proof before adding features. Identify one artifact that looks complete but is insufficient by itself, explain the missing proof, and choose your next action from that gap. For example, decide what an existing batch CSV can and cannot establish without its model-resolution metadata. Do not count the example as your full inventory.

The optional T4 transfer path replaces only the baseline estimator inside `train`, using a compatible fitted `predict` interface. Keep feature/target schema, split, primary metric, logging, registry and selected batch contract. Pin any added dependencies, establish a new reference result under the declared reproducibility contract and rerun representative valid/invalid inputs and the full lifecycle. Do not mix its scores with the original alpha-only comparison. If your prior model needs an unrelated dataset or serving stack, choose the baseline path for this project.

## Working with documentation

Use [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) to separate stable interfaces from a model-specific implementation detail. Read the code where an inventory claim depends on behavior.

## Hints

1. Mark each item “observed”, “missing” or “proposed” with a concrete evidence locator.
2. A new model can fit the scaffold only if its inputs/outputs preserve the same contract.
3. Reserve time for a second engineer's clean run; it is part of the deliverable.

## Checkpoints

Every final requirement has a proof plan. No new orchestration framework, external service or extra platform dependency is needed. A peer can distinguish an actual result from an assumption by reading your inventory.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** a bounded inventory with one evidence locator or explicit gap for each final criterion, followed by a dependency-ordered plan. Existing execution evidence is reused where source, data and selection still match. A CSV alone can show prediction rows; it cannot identify the registry version used, establish elapsed time, or prove a fresh environment.

**How to check:** follow each claimed proof to the actual file or record. If a row says “reproducible” but links only to a README or a same-environment replay, mark the fresh receiving proof as missing. If you choose the T4 path, its changed estimator/dependencies require a new reference and representative contract checks inside this scaffold; it is not an extra requirement for the baseline path. If the inventory mostly lists new features, replace those with commands that resolve the missing acceptance evidence first.

</details>

## Learning outcome

Continue the pipeline built across Sprints 1-3 and scope the remaining work needed to meet the final criteria. A T4 (AI track) model may replace the baseline model only as a deliberate transfer test inside the same scaffold.

## Summary

Your scope separates demonstrated behavior from missing proof. The final project can now focus on completing the cumulative handoff within the existing interfaces.
