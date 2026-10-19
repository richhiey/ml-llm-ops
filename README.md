# MLOps / LLMOps course code

Linden Facilities needs 24 hourly energy-demand estimates for its planning handoff. Module A takes that small job from explicit pipeline stages to tracked experiments, model registration, rollback and a reproducible handoff.

This is the shared code repository for **Module A and Module B**. Start with [Module A](module-a/README.md). [Module B](module-b/README.md) has a reserved folder and will be added separately.

## Get started locally

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops/module-a
uv sync --locked
uv run pytest -q
uv run campus-mlops bootstrap --state state-first
```

Use Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/). The package and data are local after installation; model runs need no API key. Open the [four teaching notebooks](module-a/notebooks/README.md) for the explained reference path, or create an editable project using the Module A stage lab.

## Repository boundaries

- `module-a/src/campus_mlops`: reusable pipeline, tracking and registry code.
- `module-a/notebooks`: guided references that import that package; also open in Colab.
- `module-a/exercises`: starting-state generators and the unseen intake data.
- `module-a/docs`, `tests`, `examples`: contracts, recovery instructions and executable checks.
- `module-b`: reserved for the next module; no Module B runtime is required for Module A.

Campus lessons and instructor rubrics are authored separately. Runtime stores, model artifacts, credentials and local environments are ignored. Use new state directories to preserve earlier evidence. This is a single-user teaching system with synthetic data, not a production deployment.
