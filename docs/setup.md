# Set up the demand-model project

Install [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/). Run in a terminal:

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --locked --python 3.12
uv run pytest -q
uv run linden-mlops status
```

`uv` creates `.venv` and installs the versions in `uv.lock`. Run subsequent commands from this repository root. A successful test run checks the input contract, model lifecycle, durable selection and portable recovery. Python must be 3.12; a different interpreter or untracked package installation can invalidate a recovery comparison.

## Work in the repository

Edit `src/linden_mlops/` in your editor. Use `uv run python your_script.py` to run your own scripts with the same environment. The [API reference](api-reference.md) explains the objects you can connect; `uv run linden-mlops --help` lists terminal operations.

Follow the [course journey](course/README.md). Practical lessons include commands or API tasks; checkpoints reuse your work and check what you understand. You do not need to submit files or maintain a separate report for every lesson.

Keep this clone and `work/` between sprints. `work/project.json` stores the declared experiment plan, five actual run IDs, selected configuration and registry identity. `work/tracking/` stores MLflow's SQLite database and artifacts. Both are local and ignored by Git. A kernel restart or a new terminal does not erase them. `--work-dir work/another-comparison` starts a deliberately separate project; do not use it simply to continue the next sprint.

## Optional notebooks

Open one of the [four notebooks](../notebooks/README.md) in VS Code or your notebook editor. Choose `.venv/bin/python` as the kernel. The notebooks operate on this same source tree and `work/`; they provide guided probes and room for independent attempts. Run cells in order. The Sprint 1 stage exercise deliberately demonstrates a failing contract before restoring the full implementation. Run saved-source checks in a fresh process after edits to avoid stale imports.

For a hosted notebook, use a Python 3.12 runtime and clone this repository into a persistent project folder. The notebook setup explains the matching environment. Retain your project files and `work/` before ending a temporary runtime. Local execution is required for the MLflow UI and the fresh-environment receiving test; hosted execution is optional.

## Open MLflow

After logging runs:

```sh
uv run linden-mlops ui
```

Keep that terminal running and open `http://127.0.0.1:5050`. Use a full-width browser window for MLflow’s run table; a narrow side panel can hide selection and comparison controls. Find the `linden-demand` experiment. Compare your saved run IDs, not every execution in the store. Stop the server with Ctrl+C. For a separate incident use its actual store, for example `uv run linden-mlops ui --state work/rollback`.

## If something fails

Check `pwd`, `uv run python --version`, and `uv run linden-mlops status`. Missing saved IDs usually means a different `work/` or tracking store. A source mismatch means your code changed after the experiment: restore the recorded source, or deliberately start a new comparison. Do not erase evidence to bypass a check. For another engineer's machine, use a [portable recovery export](recovery.md); copying SQLite alone does not relocate absolute artifact paths.
