✂️
# Setup, run, and expected-evidence instructions

Linden Facilities wants an engineer who has never opened your working notes to run the project. The handoff must name what to start with, what to execute and how to tell whether it worked.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Setup, run, and expected-evidence instructions** using its Campus activity ID **A-S4-04**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Use the complete [export and receiving procedure](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md) as your reference. Export the saved selected run with `uv run linden-mlops export --destination work/handoff-export`. In `work/HANDOFF.md`, adapt the receiving commands to your actual export, source location and observed recipe. Do not substitute default `alpha=1`. This is a working runbook for another engineer, not a separate assignment report.


## Starting point

Use the helper's [clean-state contract](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md), your source/data/config/environment bundle and actual inference/reproduction evidence. A **handoff** is a recoverable package plus instructions and acceptance checks, not a list of tools.

| Receiving engineer needs | Package must supply |
|---|---|
| Recoverable inputs | Source/data/config/environment/model files |
| Exact execution | Working directory, commands and output locations |
| Decision rule | Lineage invariants, tolerance and inference checks |

## Your task

Write `HANDOFF.md` from the declared clean state: new source folder, Python `3.12`, new locked environment, no inherited MLflow state, and a new output directory. Name the helper version/content revision and snapshot hash. Include exact setup and execution commands with your chosen alpha, guard, logging mode and evaluation partition.

State where another engineer should find the source run, model URI, registered version, validation evidence, active alias, audit events, batch CSV and timing. Specify `24` complete finite predictions within `60` seconds and absolute RMSE difference <= `1e-6` kWh with matching lineage. Explain expected differences in run IDs, timestamps, paths and version counters.

Add recovery instructions for a mismatched source revision, missing artifact directory, wrong interpreter and existing state directory. Review the handoff as a receiving engineer: identify one command that would fail if your original checkout/store disappeared and repair it before execution. Give it to a peer or perform the separate-folder receiving test in the clean-run task; use that same test as evidence for both activities and record every correction needed.

## Working with documentation

Use [uv locked sync](https://docs.astral.sh/uv/concepts/projects/sync/) for environment reconstruction. Package versions alone cannot replace source/data/config evidence.

## Hints

1. Write the working directory before each command group.
2. Replace every placeholder run ID with a clearly explained value from the actual output.
3. Separate acceptance checks from illustrative author values.

## Checkpoints

Every named file exists in the package. Commands run without notebook variables or private paths from your computer. A second engineer can find and compare all lineage fields, then verify inference and RMSE without asking what “close enough” means.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** a runbook that reconstructs source and a new locked Python `3.12` environment, reads the exported selected recipe, and writes into a new state directory. It names actual portable inputs, lineage comparisons, absolute `1e-6` kWh tolerance and the `24`-row/`60`-second batch checks. It explains why new run IDs and version counters are expected.

**How to check:** trace each command's inputs backwards to something included in the export or explicitly available in the declared clean state. Replace original-store absolute paths and implicit notebook variables with the receiving procedure. Copying a fitted model alone proves neither retraining nor setup. If instructions use default alpha `1` despite a different selected recipe, repair the command; if they assume an artifact directory outside the package, repair the export. Keep one actual receiving test for the clean-run evidence rather than repeating it for documentation alone.

</details>

## Learning outcome

Produce environment/setup and run instructions that start from the clean-state verification specification's declared clean state, name the data snapshot and exact execution command, and state the expected lineage fields, inference evidence, and result tolerance a second engineer must verify.

## Summary

Another engineer now has recoverable inputs, exact commands and concrete acceptance checks. The handoff explains how to diagnose a mismatch instead of relying on your working notes memory.
