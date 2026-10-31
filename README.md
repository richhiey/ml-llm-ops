# Linden energy-demand application

A local Python application for training an energy-demand model, tracking comparable experiments in MLflow, delivering identified prediction CSVs, managing approved model versions and recovering a recorded recipe. It uses a fixed synthetic demand snapshot; the fixture demonstrates engineering behavior rather than real building forecasting quality.

```sh
uv sync --locked --python 3.12
uv run pytest tests/test_spine.py::test_contract_extension_and_unchanged_pipeline -q
uv run linden-mlops train --config configs/baseline.json
```

Training returns an actual run ID, logged-model URI, validation metrics and source/data/environment manifest. To predict without a registry, pass that actual URI:

```sh
uv run linden-mlops batch --model-uri ACTUAL_LOGGED_MODEL_URI --output-name first-delivery
```

Replace the placeholder with the training result's `model_uri`. A batch job never overwrites a prior CSV or its metadata. Use a fresh job name for another execution. The default planned input contains `24` rows; the planner's acceptance contract requires a complete aligned file within `60` seconds.

[Setup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md) · [Contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) · [Experiments](https://github.com/richhiey/ml-llm-ops/blob/main/docs/experiments.md) · [API](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md)

[Operations](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md) covers explicit monitoring inputs and candidate decisions. [Recovery](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md) covers verified release descriptors, explicit exports and a new receiving source/environment/store.

Application code contains no lesson progression, source resetter or assessment generator. [Campus lessons](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/README.md), four optional notebooks and clearly labeled course intake assets are separate from the runtime source archive. Work on a Git feature branch, write ordinary regression tests and retain actual run/job identities. Course fixture preparation is external instructor tooling and cannot establish a learner's work.
