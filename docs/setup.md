# Set up the demand application in VS Code

Install [Git](https://git-scm.com/downloads), [uv](https://docs.astral.sh/uv/getting-started/installation/) and [VS Code](https://code.visualstudio.com/). Add the [Python extension](https://code.visualstudio.com/docs/languages/python) if needed.

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --locked --python 3.12
uv run python --version
uv run pytest tests/test_spine.py::test_contract_extension_and_unchanged_pipeline -q
uv run linden-mlops status
```

Expect Python `3.12.x`, one passing existing input-contract test and a project location under `work`. Open this folder in VS Code and choose this clone's `.venv` using **Python: Select Interpreter**. The terminal must be at the folder containing `pyproject.toml`. `uv run` uses the environment without activation.

## Work on the actual application

| Location | Responsibility |
|---|---|
| `src/linden_mlops/pipeline.py` | Ingestion, existing valid range guard, feature order and fitted model |
| `src/linden_mlops/lifecycle.py` | Tracking, model lifecycle and batch prediction |
| `configs/` | Explicit model and experiment settings |
| `tests/` | Ordinary application regression tests |
| `work/` | Local run/job records and your engineering notes |

The supplied range guard is complete. No setup command replaces it with broken code. A new requirement is implemented as an actual source change on your branch, with distinguishing tests and `git diff` as the change record. The Campus walkthrough introduces a new planned-batch intake boundary; that learner-created module is intentionally absent from this baseline.

```sh
git switch -c planned-batch-validation
```

If that branch already exists, reopen it instead of creating another. Keep the same clone and `work/` through the journey. The application does not require a sprint directory or a completion flag. An existing valid model can be reused for a new serving validation change; inspect the batch metadata's `serving_code_revision` separately from its training run's source identity.

## Run and inspect actual operations

Use a small Python script or the application CLI. Training produces a fitted artifact and a run ID; inference takes an explicit logged-model URI or the registry's active version. [API reference](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) and [experiment workflow](https://github.com/richhiey/ml-llm-ops/blob/main/docs/experiments.md) document those interfaces. Every new batch needs a new output name; retained output is not an instruction to train again.

Start MLflow in a second terminal when UI inspection is required:

```sh
uv run linden-mlops ui
```

Open `http://127.0.0.1:5050` in your browser and inspect the same full run ID/store as your script. The terminal stays occupied until `Ctrl+C`; stopping it preserves records. A port already in use is a reason to inspect the existing server before starting another.

## Resume or recover

A fresh setup creates an initial application environment, not evidence of work completed earlier. To resume a lesson, reopen the saved branch, actual source patch, your focused tests, recorded failing/passing observations, relevant run/job files and explanation. If they do not exist, carry out the missing activity; do not copy a solved reference and claim prior evidence.

| Symptom | Recovery |
|---|---|
| Missing import/file | Confirm clone root and run `uv sync --locked --python 3.12` |
| Source edit appears ignored | Save it and run a new `uv run` process; select this `.venv` in the editor |
| Contract test fails | Inspect the exact assertion, retain failure, repair its cause and rerun that test |
| Existing batch name | Inspect/reuse that actual job, or choose a fresh name for a deliberate new execution |
| Missing saved experiment | Inspect `status`; `LINDEN_WORK_DIR` selects a different project if explicitly set |
| Source differs from saved comparison | Preserve history; declare a new experiment in a deliberate new work directory |

The [four local notebooks](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/README.md) are optional core-API companions; use the same `.venv` kernel. They do not install a starter or reset source. Before assistant-summary work, confirm access to the institution-approved assistant for one actual request. No provider key or runtime integration is needed.

[Course intake preparation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/README.md) is a separate setup responsibility. [Recovery](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md) creates an actual new receiving source/environment/store; copying a local database alone does not relocate its artifacts.
