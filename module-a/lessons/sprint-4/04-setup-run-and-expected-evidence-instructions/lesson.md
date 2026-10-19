✂️
# Setup, run, and expected-evidence instructions

Linden Facilities wants an engineer who has never opened your notebook to run the project. The handoff must name what to start with, what to execute and how to tell whether it worked.

## Your route through this lesson

Write and test instructions from the receiving engineer’s starting state. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Recoverable package, exact commands, acceptance rules and tested recovery notes.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=handoff-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use the helper's [clean-state contract](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md), your source/data/config/environment bundle and actual inference/reproduction evidence. A **handoff** is a recoverable package plus instructions and acceptance checks, not a list of tools.

| Receiving engineer needs | Package must supply |
|---|---|
| Recoverable inputs | Source/data/config/environment/model files |
| Exact execution | Working directory, commands and output locations |
| Decision rule | Lineage invariants, tolerance and inference checks |

## Write for someone who cannot see your filesystem

The receiving engineer does not know which terminal you used, which notebook variable holds a run ID or where a temporary Colab directory was created. Your instructions must replace that missing context with explicit starting files, working directories and commands. Do not assume that your absolute paths exist on their machine.

Separate **rebuilding** from **comparing**. Rebuilding uses the recovered source/data/config and a new environment/store. Comparing uses the original manifest and preserved evidence. The receiver needs both, but should not have to keep your old SQLite artifact paths alive to train a new result.

## Design the package before polishing the prose

| Package part | Receiver should be able to do |
|---|---|
| Source plus lock and bundled data | Create the declared project/environment |
| Original manifest and configuration | Know exactly which recipe/result to compare |
| Exported fitted model | Inspect or load the selected artifact independently |
| Explained extension diff | Review the behavioral change and its tests |
| Inference/evaluation evidence | Apply the delivery and numerical acceptance rules |
| Instructions | Navigate and execute without your notebook memory |

Inventory the actual files before writing links. Export source/reproduction files and the logged model while the original store is available. A URI is a locator, not the artifact itself. Keep the original record as evidence and train into a new state at the receiving location.

## Draft instructions in the order they will be used

Begin with runtime requirements and how to obtain/extract the supplied source. Name the folder containing `pyproject.toml`, the locked sync and test commands, then the exact lifecycle command using your selected alpha, enabled guard and logging setting. State which command creates which output directory.

Next describe acceptance. Give field names for source/data/config/partition/environment equality; state absolute RMSE difference <= `1e-6` kWh; name expected changes such as IDs and paths. Then define batch acceptance: 24 aligned finite predictions, intended resolved version/source run and completion within 60 seconds. A receiver should not have to infer these rules from a screenshot.

## Test the document as an interface

Follow your own text in another folder without relying on shell history or notebook variables. Mark every moment where you supply undocumented knowledge. Add the missing instruction and repeat from another fresh destination. If a peer is available, ask them to execute the document rather than narrating over their shoulder.

Include recovery notes for at least one source/environment mismatch and one missing artifact. “Try again” is not a diagnosis. A useful note says what observation indicates the issue, what original evidence to inspect and which preserved source/package to restore. Keep a short correction log so the final handoff reflects what a receiving run actually required.

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

## A handoff must survive relocation

Ask a second engineer to point to each artifact from the package alone. An absolute `file:///...` artifact location in the original SQLite store will not relocate automatically. Export the model/reproduction files you intend to hand over and name the original store only as comparison evidence. Run the training/lifecycle command against a new store at the new location. Include one concrete recovery for a missing artifact and one for a source/environment mismatch.

## Learning outcome

Produce environment/setup and run instructions that start from the clean-state verification specification's declared clean state, name the data snapshot and exact execution command, and state the expected lineage fields, inference evidence, and result tolerance a second engineer must verify.

## Summary

Another engineer now has recoverable inputs, exact commands and concrete acceptance checks. The handoff explains how to diagnose a mismatch instead of relying on your notebook memory.
