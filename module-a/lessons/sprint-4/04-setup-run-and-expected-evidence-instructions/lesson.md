✂️
# Setup, run, and expected-evidence instructions

Linden Facilities wants an engineer who has never opened your notebook to run the project. The handoff must name what to start with, what to execute and how to tell whether it worked.

**Continue here:** [Sprint 4 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb#scrollTo=handoff-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use the helper's [clean-state contract](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md), your source/data/config/environment bundle and actual inference/reproduction evidence. A **handoff** is a recoverable package plus instructions and acceptance checks, not a list of tools.

| Receiving engineer needs | Package must supply |
|---|---|
| Recoverable inputs | Source/data/config/environment/model files |
| Exact execution | Working directory, commands and output locations |
| Decision rule | Lineage invariants, tolerance and inference checks |

## Your task

Write `HANDOFF.md` from the declared clean state: new source folder, Python `3.12`, new locked environment, no inherited MLflow state, and a new output directory. Name the helper version/content revision and snapshot hash. Include exact setup and execution commands with your chosen alpha, guard, logging mode and evaluation partition.

State where another engineer should find the source run, model URI, registered version, validation evidence, active alias, audit events, batch CSV and timing. Specify `24` complete finite predictions within `60` seconds and absolute RMSE difference <= `1e-6` kWh with matching lineage. Explain expected differences in run IDs, timestamps, paths and version counters.

Add recovery instructions for a mismatched source revision, missing artifact directory, wrong interpreter and existing state directory. Give the handoff to a peer or run the exact written commands in a separate folder; record every correction needed.

## Working with documentation

Use [uv locked sync](https://docs.astral.sh/uv/concepts/projects/sync/) for environment reconstruction. Package versions alone cannot replace source/data/config evidence.

## Hints

1. Write the working directory before each command group.
2. Replace every placeholder run ID with a clearly explained value from the actual output.
3. Separate acceptance checks from illustrative author values.

## Checkpoints

Every named file exists in the package. Commands run without notebook variables or private paths from your computer. A second engineer can find and compare all lineage fields, then judge inference and RMSE without asking what “close enough” means.

## Learning outcome

Produce environment/setup and run instructions that start from the clean-state verification specification's declared clean state, name the data snapshot and exact execution command, and state the expected lineage fields, inference evidence, and result tolerance a second engineer must verify.

## Summary

Another engineer now has recoverable inputs, exact commands and concrete acceptance checks. The handoff explains how to diagnose a mismatch instead of relying on your notebook memory.
