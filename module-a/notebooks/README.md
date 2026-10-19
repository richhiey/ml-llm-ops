# Guided notebooks and an unsolved learner workspace

Linden's planner needs a result another engineer can explain and rebuild. The four guided notebooks show the complete reference path. The learner workspace starts with an empty store and supplies tools for your own investigation. Independent practices ask you to make decisions in your own project or prepared state.

| Notebook | Focus | Open in Colab |
|---|---|---|
| [00 — Learner workspace](00-learner-workspace.ipynb) | Start unsolved; edit projects, investigate cases and keep your own decisions | [Open workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb) |
| [01 — Pipeline and extension](01-pipeline-and-extension.ipynb) | Follow rows, explain the guard, check predictions | [Open 01](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb) |
| [02 — Tracking and evidence](02-tracking-and-evidence.ipynb) | Controlled runs, autologging and checked recommendations | [Open 02](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb) |
| [03 — Registry and reproduction](03-registry-and-reproduction.ipynb) | Approve, activate, roll back and reproduce | [Open 03](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb) |
| [04 — Cumulative handoff](04-cumulative-handoff.ipynb) | Connect the lifecycle, final holdout and handoff | [Open 04](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb) |

**Colab:** start a fresh Python 3.12 CPU runtime and run setup first. It clones the immutable commit in [helper-pin.json](helper-pin.json), installs locked runtime dependencies and imports the package. Read [Colab guidance](../docs/colab.md) before relying on hosted storage, environment reproduction or a localhost UI address.

**Local:** from `module-a`, run `uv sync --locked`, select `.venv/bin/python` in your notebook editor, and run from the top. To verify all five notebooks in separate kernels:

```sh
uv run python notebooks/execute_notebooks.py
```

Every notebook creates a fresh state directory. No notebook depends on another's variables or store. Package implementations live in `../src/campus_mlops`; cells only call and inspect that API. Keep the exact reference source pin; create an editable project with `uv run python exercises/make-stage-lab.py --destination ../project-helper` for your cumulative extension. Do not remove the pin assertion to accept changed code.

After committing a source change, run `uv run python authoring/make_notebooks.py --source-commit COMMIT_SHA` from `module-a` to generate notebooks and their pin together, then execute all five. The generator checks that tracked package source matches that commit; it overwrites reference cells, so keep learner edits in a separate copy. Actual local execution is recorded separately from hosted Colab verification. A saved output is a worked example, not proof of your own UI comparison, assistant request or project work.

The [complete Campus learning path](../lessons/README.md) and [setup/execution guide](../docs/learning-guide.md) map lesson purposes, starting states and completion checks to the notebook sections. The [learning-path manifest](../learning-path.json) is checked against each lesson and notebook anchor with `uv run python authoring/verify_learning_path.py`. Its synchronization checks do not replace instructional review.
