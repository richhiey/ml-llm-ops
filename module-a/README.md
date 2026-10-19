# Campus MLOps helper 0.1.1

Linden Facilities is a fictional team preparing 24 hourly energy-demand estimates for a planning handoff. This repository is the reusable source of truth for Module A. The [Campus learning path](lessons/README.md) versions learner Markdown and assets here; instructor support remains in the authoring workspace. The reusable code, exercises and notebooks live together here in the shared Modules A/B GitHub repository.

## Supported local setup

Install Python **3.12** and [uv](https://docs.astral.sh/uv/getting-started/installation/). Commands below run from this directory, containing `pyproject.toml`. Setup downloads public packages; subsequent data access and model execution are local. No credentials are needed.

```sh
uv sync --locked
uv run pytest -q
uv run campus-mlops bootstrap --state state
uv run campus-mlops matrix --state state --autolog
uv run campus-mlops ui --state state
```

Open `http://127.0.0.1:5050` while the last command is running; stop it with Ctrl+C. Use the `linden-demand` experiment. `bootstrap` trains and registers an approved guarded baseline and sets `dev.linden-demand@active`. Repeating it adds versions; it does not reset the store. `matrix` adds five alpha configurations. For an empty starting state choose a new, nonexistent directory such as `state-second`; never delete evidence to get a clean run.

## Read the stages

| Stage | Implementation | Contract |
|---|---|---|
| Ingestion | `pipeline.ingest` | Fixed CSV -> 240 complete unique rows; train/validation/final labels |
| Preprocessing | `pipeline.preprocess` | Exact feature order; optional range check; no fitted statistics from held-out data |
| Training | `pipeline.train` | Train rows only -> fitted `StandardScaler` + `Ridge(solver='svd')` |
| Evaluation | `pipeline.evaluate` | Held-out rows -> RMSE primary, MAE diagnostic, kWh, lower is better |
| Inference | `lifecycle.batch_predict` | Active alias resolved once -> pinned version, one prediction per input row and timing evidence |

`run_pipeline` connects the first four stages without tracking. `Workspace.run` wraps them in MLflow. The scaler is fitted inside training and stored with the model; `preprocess` extracts features and validates inputs. See [contracts](docs/contracts.md), [inference brief](docs/inference-brief.md), [clean state](docs/clean-state.md), [data card](src/campus_mlops/data/README.md) and [API examples](examples/lifecycle.py).

## Outputs

Within the chosen state directory: `mlflow.db`, `artifacts/`, `evidence/<run_id>/manifest.json`, `source.tar.gz`, `config.json`, `environment.txt`, plus `batch.csv`, `batch.json`, and `audit.jsonl` after bootstrap/handoff. MLflow also stores the model and reproduction package as artifacts. A run ID, model ID and registered version identify different objects; never substitute one for another.

`uv run campus-mlops handoff --state state-final --range-guard --autolog` is the integrated run. Use the chosen `--alpha` from validation comparisons. For the reserved final evaluation after selection, run `uv run campus-mlops train --state state-final-evaluation --alpha 0.01 --range-guard --autolog --partition final` with your selected alpha. It belongs to a different comparison group and cannot be approved by the validation-based promotion policy. Do not attach `--partition final` to `handoff`.

## Notebook workflow

From this repository, run `uv run python notebooks/execute_notebooks.py` to execute the five notebooks with this interpreter. For interactive work start Jupyter in your preferred editor and select this `.venv/bin/python`. Notebook setup checks helper `0.1.1` and the content revision in `notebooks/helper-pin.json`. Relative paths resolve from the notebook folder or this repository; do not copy helper functions into cells. See the notebook README for release synchronization.

## Versioned code and recovery

Clone [richhiey/ml-llm-ops](https://github.com/richhiey/ml-llm-ops) and work in `module-a`. The notebooks pin an immutable source commit and a source-content hash. Git identifies the repository snapshot; the content hash identifies the pipeline/package/data files used by the reproduction contract. Keep these distinct.

`source.tar.gz` contains the package source, bundled data, project declaration and `uv.lock`; restore it into a new folder and sync the lock before rerunning. Do not overwrite working files to reproduce an earlier run. [Colab setup](docs/colab.md) explains the hosted notebook path and its environment limits.

## Scope

This is a single-user local teaching scaffold. SQLite and JSONL audit evidence do not implement production access control, concurrent deployment, immutable audit, drift detection, or an orchestration service. Batch timing includes model load and CSV writing and is machine dependent. Synthetic metrics cannot establish real demand forecasting quality.


## Learner project versus reference notebooks

Four notebooks are complete guided references. `00-learner-workspace.ipynb` is an unsolved start for independent work. Keep them on the exact published helper pin. For an editable cumulative project, from this helper folder run `uv run python exercises/make-stage-lab.py --destination ../project-helper`, then enter that folder and run `uv sync --locked`. The starter has a deliberately finite-only validation stage: its contract test fails until the learner implements domain checks. Follow the stage walkthrough. Track your changed source revision using project CLI/tests; do not disable the reference notebook's pin assertion. The project uses the same public API and snapshot.

Prepared states are available from the project/helper root with `uv run python exercises/prepare-practice.py CASE --state NEW_PATH` for `matrix`, `past-run`, `rollback` and `registry-assessment`. Each stops before the target learner operation. The matrix writes `matrix-run-ids.json`; keep these IDs and pass only those rows to the numeric recommendation check. The file is replaced by a subsequent matrix CLI invocation, so copy it with submitted evidence.

## Learn through the complete path

The [26 Campus lessons](lessons/README.md) explain the concepts and mechanisms, then distinguish guided execution, independent investigation and client checkpoints. Each lesson links the code and its appropriate Colab section. The [execution guide](docs/learning-guide.md) explains local/Colab equivalents and keeps changed project code separate from notebook imports.
