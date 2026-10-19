# Linden demand pipeline

A reproducible energy-demand pipeline: validate inputs, train a model, compare experiments in MLflow, manage the active model, and deliver a timed prediction batch.

The repository is the working project. Make changes in `src/linden_mlops/`, test them, and keep configuration and execution evidence with the run that produced them.

```sh
uv sync --locked --python 3.12
uv run pytest -q
uv run linden-mlops handoff --config configs/baseline.json --state work/first-run
```

The example uses bundled synthetic data. It produces 24 planned predictions and records the source, data, configuration, environment, model identity and completion time. See [setup](docs/setup.md) before the first run.

```text
src/linden_mlops/   Pipeline, tracking, registry, project records and recovery
configs/           Declared experiment and baseline settings
notebooks/         Four sprint notebooks operating on this source tree
tests/            Contract, lifecycle, continuity and recovery checks
docs/             Setup, architecture, references and course material
work/             Local progress, runs and exports (ignored by Git)
```

[Architecture](docs/architecture.md) · [Course journey](docs/course/README.md) · [Experiment workflow](docs/experiments.md) · [Recovery](docs/recovery.md)

The optional notebooks share `work/project.json` and the same experiment store. They do not create another repository or choose a new baseline silently. The Campus lessons also provide terminal commands and Python API tasks. There is nothing to submit. Keep the clone and `work/` between sprints; use a portable export when handing a run to another engineer.

The local SQLite registry and JSONL change log are inspectable teaching infrastructure. They are not an access-controlled production deployment or immutable audit service. [Contracts and limits](docs/contracts.md) describe the boundaries.
