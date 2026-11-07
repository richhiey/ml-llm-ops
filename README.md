# Catalog MLOps

Train, evaluate and serve a small Fashion-MNIST CNN on a local CPU. Threadline Retail's catalog team uses it to investigate category suggestions and measurable improvements.

This is the same instruction sequence as the [pipeline walkthrough](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/02-reading-the-provided-pipeline-scaffold/lesson.md). Each Python command names a file you can open. Uvicorn starts the FastAPI server; curl makes the HTTP request. The project functions inside the files assemble the underlying PyTorch, NumPy and scikit-learn operations.

Use VS Code or a terminal. Install [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/) first. Run all commands from the repository root. Python `3.12.12` is selected by the project. [Setup and troubleshooting](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md)

## 1. Get the project and inspect the data

```bash
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --frozen
uv run --frozen python scripts/prepare_data.py
uv run --frozen python scripts/inspect_dataset.py
```

Expect `12,000` training and `3,000` validation images, selected from the original research training file. Open `work/training-examples.png`. Keep the official test split reserved until model selection is complete.

## 2. Train from scratch

```bash
uv run --frozen python scripts/train.py --config configs/baseline.json --output work/runs/baseline
```

Expect four epoch observations and a retained run in `work/runs/baseline`. Existing run directories are protected. Resume by inspecting them; choose a new output only for a deliberate new run.

## 3. Evaluate the saved model and inspect its mistakes

```bash
uv run --frozen python scripts/evaluate.py --run work/runs/baseline
uv run --frozen python scripts/inspect_results.py --run work/runs/baseline
```

Expect `3000` validation predictions, accuracy, macro F1 and per-category results. Open `work/learning-history.png` and `work/confusion-matrix.png`. The author's observed baseline reached accuracy `0.8380` and macro F1 `0.8322`; your own saved observations are the evidence for your run.

## 4. Predict a batch of incoming images

```bash
uv run --frozen python scripts/export_samples.py --count 20 --output work/intake
uv run --frozen python scripts/predict_batch.py --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/baseline
```

Expect `20` identified rows in `work/batches/baseline/predictions.csv` and a `batch.json` record identifying the model used.

## 5. Start the HTTP server in a second terminal

Keep your first terminal open. In a **second terminal**, change to this repository's root and run:

```bash
uv run --frozen uvicorn scripts.api:app --host 127.0.0.1 --port 8000
```

Wait for application startup to complete. The explicit `RUN_DIRECTORY` in [scripts/api.py](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/api.py) pins `work/runs/baseline`. The [FastAPI implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/service.py) exposes `/health` and `/predict`. Uvicorn is the long-running server process.

## 6. Send one request from the first terminal

```bash
uv run --frozen python scripts/prepare_request.py --image work/intake/56368.png --image-id train:56368 --output work/intake/request.json
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary @work/intake/request.json http://127.0.0.1:8000/predict
```

Open `work/intake/request.json` to inspect the exact body sent: an identifier and raw pixels. The Python file only converts the PNG to JSON; curl sends it. Windows PowerShell users should use `curl.exe`. The command needs curl with `--fail-with-body` support (7.76 or later).

Expect a prediction, loaded model identity and service-side processing time. Compare the class and model hash with the matching batch row; top scores should agree within `1e-6`. Stop the server with **Ctrl+C in the second terminal**.

## Continue the project

The [Campus lessons](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/README.md) guide the intake extension and independent work. The [companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) shows complete native-package implementations for deeper inspection. Read the [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) and [dataset card](https://github.com/richhiey/ml-llm-ops/blob/main/docs/dataset-card.md) for operational requirements, limitations and attribution.

| Location | Purpose |
|---|---|
| `scripts/` | Readable files for dataset inspection, training, evaluation and prediction; explicit FastAPI startup |
| `src/catalog_mlops/` | Reusable pipeline implementation built on the real packages |
| `configs/` | Declared training settings |
| `tests/` | Checks of pipeline behavior and artifact integrity |
| `notebooks/` | Optional implementation detail and learner investigations |
| `docs/course/` | Lessons and separately labeled exercise fixtures |
| `work/`, `data/` | Ignored local results and verified dataset cache |

## Sprint 2: track and compare experiments

Continue after the intake extension. Keep the source and evaluation conditions fixed for the controlled study. The following sequence reproduces the [MLflow walkthrough](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/04-revisiting-mlflow-in-a-pipeline-context/lesson.md), followed by the comparison and autologging practice commands. Keep your original saved baseline as historical evidence.

### Confirm a tracked baseline

```bash
uv run --frozen python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline --state work/mlflow --name baseline
```

Expect a retained local run and `work/experiments/baseline.tracking.json` containing the full run ID and native logged-model URI.

### Run the five reference candidates

```bash
uv run --frozen python scripts/track_experiment.py --config configs/experiments/longer-training.json --output work/experiments/longer-training --state work/mlflow --name longer-training
uv run --frozen python scripts/track_experiment.py --config configs/experiments/lower-learning-rate.json --output work/experiments/lower-learning-rate --state work/mlflow --name lower-learning-rate
uv run --frozen python scripts/track_experiment.py --config configs/experiments/weight-decay.json --output work/experiments/weight-decay --state work/mlflow --name weight-decay
uv run --frozen python scripts/track_experiment.py --config configs/experiments/dropout.json --output work/experiments/dropout --state work/mlflow --name dropout
uv run --frozen python scripts/track_experiment.py --config configs/experiments/translation.json --output work/experiments/translation --state work/mlflow --name translation
```

Expect five additional configurations and receipts. Preserve regressions as well as gains. Each candidate changes one factor against baseline.

### Start MLflow in a second terminal

```bash
uv run --frozen mlflow ui --backend-store-uri sqlite:///work/mlflow/tracking.db --host 127.0.0.1 --port 5001
```

Open `http://127.0.0.1:5001`, choose **Experiments → threadline-cnn**, and inspect the actual parameters, metrics, histories, artifacts and model. Select baseline plus the five candidates and choose **Compare**. Inspect `validation_macro_f1` and the category tradeoffs. Keep this terminal running; stop it with `Ctrl+C` when finished.

### Verify your raw comparison

Replace each capitalized ID token with the full run ID from your own ledger/receipt. Make the UI decision first; the comparison file checks raw prediction metrics, controls and model attribution.

```bash
uv run --frozen python scripts/compare_runs.py --state work/mlflow --baseline BASELINE_ID --runs LONGER_ID LOWER_LR_ID WEIGHT_DECAY_ID DROPOUT_ID TRANSLATION_ID --output work/comparison.json
```

Expect five distinct eligible candidates and a selected native model URI. Keep the resulting decision file intact. This ranks the controlled study; a new partner business policy is documented separately.

### Check genuine autologging in the first terminal

```bash
uv run --frozen python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline-autolog --state work/mlflow --name baseline-autolog --autolog
```

Expect the baseline configuration to repeat, with four `auto/` metric histories at steps 1–4 and `autolog_hook=tensorboard`. Final decision metrics, lineage and artifacts remain explicitly logged. This is an instrumentation repeat, not another distinct improvement candidate.

Continue with the [assistant validation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/07-validating-an-assistant-generated-experiment-summary/lesson.md) and partner assessment. The [optional native-package notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) inspects your actual records and raw predictions. [Actual authored reference observations](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/evidence/sprint-2) are provided for feedback; they are not a preloaded tracking store.
