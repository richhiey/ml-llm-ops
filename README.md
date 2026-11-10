# Fashion-MNIST MLOps

A local image-classification pipeline with a scikit-learn logistic regression baseline. The pipeline records dataset and source identities, tracks experiments in MLflow, and serves predictions from a saved or registered model.

## Quick start

Install Git and `uv`, then run the following commands from the repository root. TorchVision downloads Fashion-MNIST on first use.

```bash
uv sync --frozen
source .venv/bin/activate
pytest -q
python scripts/prepare_data.py
python scripts/train.py --config configs/baseline.json --output work/runs/baseline
python scripts/evaluate.py --run work/runs/baseline
```

For PowerShell, activate with `.\.venv\Scripts\Activate.ps1`. Keep new runs in separate output directories.

## Project layout

| Path | Contents |
|---|---|
| `src/` | Dataset, features, training, inference, tracking and registry code |
| `scripts/` | Command-line entry points and HTTP service |
| `configs/` | Model and experiment settings |
| `tests/` | Automated tests |
| `examples/` | Synthetic input fixtures and a release starter |

Use `python scripts/track_experiment.py --help` to fit and track a configuration and `python scripts/predict_batch.py --help` to run a saved model over a manifest.

## Model registry

After tracking a run, open the local MLflow UI from the repository root.

```bash
mlflow ui --backend-store-uri sqlite:///work/mlflow/tracking.db --host 127.0.0.1 --port 5001
```

Open the run's logged model and use **Register model** to create a version. Open that version to inspect its source run, tags and aliases. When a clean replay passes, `python scripts/assign_alias.py --help` shows how to use `--approve` to retain the replay report and select the reviewed version. Use `--rollback` with the earlier approval to restore a previously selected version. Both selections record the alias before and after the change in `work/mlflow/registry-audit.jsonl`.
