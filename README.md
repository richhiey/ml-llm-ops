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
