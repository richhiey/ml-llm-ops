# MLOps / LLMOps course code

Linden Facilities needs 24 hourly energy-demand estimates for its planning handoff. Module A takes that small job from explicit pipeline stages to tracked experiments, model registration, rollback and a reproducible handoff.

This is the shared code repository for **Module A and Module B**. Start with the [Module A learning path](module-a/lessons/README.md) and its [setup guide](module-a/docs/learning-guide.md). [Module B](module-b/README.md) has a reserved folder and will be added separately.

## Get started locally

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops/module-a
uv sync --locked
uv run pytest -q
uv run campus-mlops bootstrap --state state-first
```

Use Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/). The package and data are local after installation; model runs need no API key. Open the [guided notebooks and learner workspace](module-a/notebooks/README.md) for the explained reference path, or create an editable project using the Module A stage lab.

## Repository boundaries

- `module-a/src/campus_mlops`: reusable pipeline, tracking and registry code.
- `module-a/notebooks`: guided references that import that package; also open in Colab.
- `module-a/exercises`: starting-state generators and the unseen intake data.
- `module-a/docs`, `tests`, `examples`: contracts, recovery instructions and executable checks.
- `module-b`: reserved for the next module; no Module B runtime is required for Module A.

Learner Campus Markdown and assets live in `module-a/lessons` alongside the code and notebooks. The authoring workspace points to those canonical files. Instructor guides and rubrics stay separate. Runtime stores, model artifacts, credentials and local environments are ignored. Use new state directories to preserve earlier evidence. This is a single-user teaching system with synthetic data, not a production deployment.
