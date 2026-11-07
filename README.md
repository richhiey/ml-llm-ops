# Catalog MLOps

Build a category-suggestion aid for Threadline Retail, the course's fictional online clothing shop. A wrongly categorized product can be missed by a shopper using category filters. Train, evaluate and use a small image model to suggest categories that catalog staff can check, then investigate measurable improvements.

This is the same instruction sequence as the [pipeline walkthrough](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/02-reading-the-provided-pipeline-scaffold/lesson.md). Each Python command names a file you can open. Uvicorn starts the FastAPI server; curl makes the HTTP request. The project functions inside the files assemble the underlying PyTorch, NumPy and scikit-learn operations.

Use VS Code or a terminal. Install [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/) first. Activate `.venv` once in each terminal; then run plain tool commands. Use the Windows activation command in the setup guide when applicable. Run all commands from the repository root. Python `3.12.12` is selected by the project. [Setup and troubleshooting](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md)

## 1. Get the project and inspect the data

```bash
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --frozen
source .venv/bin/activate
python scripts/prepare_data.py
python scripts/inspect_dataset.py
```

Expect `12,000` training and `3,000` validation images, selected from the original research training file. Open `work/training-examples.png`. Keep the official test split reserved until model selection is complete.

## 2. Train from scratch

```bash
python scripts/train.py --config configs/baseline.json --output work/runs/baseline
```

Expect four epoch observations and a retained run in `work/runs/baseline`. Existing run directories are protected. Resume by inspecting them; choose a new output only for a deliberate new run.

## 3. Evaluate the saved model and inspect its mistakes

```bash
python scripts/evaluate.py --run work/runs/baseline
python scripts/inspect_results.py --run work/runs/baseline
```

Expect `3000` validation predictions, accuracy, macro F1 and per-category results. Open `work/learning-history.png` and `work/confusion-matrix.png`. The author's observed baseline reached accuracy `0.8380` and macro F1 `0.8322`; your own saved observations are the evidence for your run.

## 4. Predict a batch of incoming images

```bash
python scripts/export_samples.py --count 20 --output work/intake
python scripts/predict_batch.py --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/baseline
```

Expect `20` identified rows in `work/batches/baseline/predictions.csv` and a `batch.json` record identifying the model used.

## 5. Start the HTTP server in a second terminal

Keep your first terminal open. In a **second terminal**, change to this repository's root and run:

```bash
source .venv/bin/activate
uvicorn scripts.api:app --host 127.0.0.1 --port 8000
```

Wait for application startup to complete. The explicit `RUN_DIRECTORY` in [scripts/api.py](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/api.py) pins `work/runs/baseline`. The [FastAPI implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/service.py) exposes `/health` and `/predict`. Uvicorn is the long-running server process.

## 6. Send one request from the first terminal

```bash
python scripts/prepare_request.py --image work/intake/56368.png --image-id train:56368 --output work/intake/request.json
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary "@work/intake/request.json" http://127.0.0.1:8000/predict
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

## Adding and validating a bounded pipeline stage

This sequence reproduces the [guided intake extension](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/03-adding-and-validating-a-bounded-pipeline-stage/lesson.md). Keep the saved baseline and original intake. Use the already activated project terminal and restart the already activated service terminal only when indicated.

### Observe the missing input check

```bash
cp docs/course/exercises/test_intake_quality.py tests/test_intake_quality.py
pytest -q tests/test_intake_quality.py
```

Expect three failures and one pass before the source change. These checks run the actual batch command.

### Add and connect the bounded change

In `src/catalog_mlops/preprocessing.py`, which already imports NumPy as `np`, add this function after `validate_images()`:

```python
def validate_contrast(images: np.ndarray, minimum_range: int = 20) -> np.ndarray:
    raw = validate_images(images)
    if not 0 <= minimum_range <= 255:
        raise ValueError("Minimum range must be between 0 and 255")
    ranges = np.ptp(raw, axis=(1, 2))
    failing_positions = np.flatnonzero(ranges < minimum_range)
    if failing_positions.size:
        raise ValueError(
            f"Insufficient contrast at batch positions {failing_positions.tolist()}"
        )
    return raw
```

Replace the first assignment inside `preprocess()` with the following, keeping the rest of its tensor conversion and fixed scaling unchanged:

```python
raw = validate_contrast(images, minimum_range=20)
```

### Verify the boundary and unchanged pipeline

```bash
pytest -q tests/test_intake_quality.py
pytest -q
git diff -- src/catalog_mlops/preprocessing.py
```

Expect all four intake cases and the existing checks to pass. Retain the source diff and explain the changed lines.

### Observe a rejected delivery

```bash
python docs/course/exercises/prepare_quality_intake.py
python scripts/predict_batch.py --run work/runs/baseline --manifest work/quality-intake/manifest.csv --output work/batches/quality-rejection
```

The batch failure is intentional: constant gray `86` has range `0`, and the requested complete batch directory must remain absent. The fixture also writes a manifest and HTTP request body.

### Verify the accepted delivery

```bash
python scripts/predict_batch.py --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/after-quality-stage
```

Expect 20 predictions matching the original valid batch; accepted pixels and saved weights are unchanged.

### Restart the service and check both request outcomes

In the already activated service terminal, restart the actual server after the source edit.

```bash
uvicorn scripts.api:app --host 127.0.0.1 --port 8000
```

In the project terminal, send the constructed invalid input.

```bash
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary "@work/quality-intake/request.json" http://127.0.0.1:8000/predict
```

Expect HTTP 422 and a nonzero curl exit for insufficient contrast. Then send the retained valid request.

```bash
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary "@work/intake/request.json" http://127.0.0.1:8000/predict
```

Expect a matching valid prediction and the same saved model identity. Stop the service with Ctrl+C.

The subsequent partner assessment changes the active call threshold to `24` while retaining this function's default `20`. Update the copied test module's `ACTIVE_MINIMUM_RANGE` to the declared partner policy and retain its passing boundary evidence. Complete that assessment and keep the application source fixed before the controlled experiment study.

## Sprint 2: track and compare experiments

Continue after the intake extension. Keep the source and evaluation conditions fixed for the controlled study. The following sequence reproduces the [MLflow walkthrough](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/04-revisiting-mlflow-in-a-pipeline-context/lesson.md), followed by the comparison and autologging practice commands. Keep your original saved baseline as historical evidence.

### Confirm a tracked baseline

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline --state work/mlflow --name baseline
```

Expect a retained local run and `work/experiments/baseline.tracking.json` containing the full run ID and native logged-model URI.

### Run the five reference candidates

```bash
python scripts/track_experiment.py --config configs/experiments/longer-training.json --output work/experiments/longer-training --state work/mlflow --name longer-training
python scripts/track_experiment.py --config configs/experiments/lower-learning-rate.json --output work/experiments/lower-learning-rate --state work/mlflow --name lower-learning-rate
python scripts/track_experiment.py --config configs/experiments/weight-decay.json --output work/experiments/weight-decay --state work/mlflow --name weight-decay
python scripts/track_experiment.py --config configs/experiments/dropout.json --output work/experiments/dropout --state work/mlflow --name dropout
python scripts/track_experiment.py --config configs/experiments/translation.json --output work/experiments/translation --state work/mlflow --name translation
```

Expect five additional configurations and receipts. Preserve regressions as well as gains. Each candidate changes one factor against baseline.

### Start MLflow in a second terminal

```bash
source .venv/bin/activate
mlflow ui --backend-store-uri sqlite:///work/mlflow/tracking.db --host 127.0.0.1 --port 5001
```

Open `http://127.0.0.1:5001`, choose **Experiments → threadline-cnn**, and inspect the actual parameters, metrics, histories, artifacts and model. Select baseline plus the five candidates and choose **Compare**. Inspect `validation_macro_f1` and the category tradeoffs. Keep this terminal running; stop it with `Ctrl+C` when finished.

### Verify your raw comparison

Replace each capitalized ID token with the full run ID from your own ledger/receipt. Make the UI decision first; the comparison file checks raw prediction metrics, controls and model attribution.

```bash
python scripts/compare_runs.py --state work/mlflow --baseline BASELINE_ID --runs LONGER_ID LOWER_LR_ID WEIGHT_DECAY_ID DROPOUT_ID TRANSLATION_ID --output work/comparison.json
```

Expect five distinct eligible candidates and a selected native model URI. Keep the resulting decision file intact. This ranks the controlled study; a new partner business policy is documented separately.

### Check genuine autologging in the first terminal

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline-autolog --state work/mlflow --name baseline-autolog --autolog
```

Expect the baseline configuration to repeat, with four `auto/` metric histories at steps 1–4 and `autolog_hook=tensorboard`. Final decision metrics, lineage and artifacts remain explicitly logged. This is an instrumentation repeat, not another distinct improvement candidate.

Continue with the [assistant validation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/07-validating-an-assistant-generated-experiment-summary/lesson.md) and partner assessment. The [optional native-package notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) inspects your actual records and raw predictions. [Actual authored reference observations](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/evidence/sprint-2) are provided for feedback; they are not a preloaded tracking store.

## Sprint 3: registry, replay and monitoring

This sequence reproduces the [guided registry walkthrough](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/02-registering-and-promoting-a-model/lesson.md). Complete the prior controlled study and keep its actual ledger. Follow Threadline's equal-category selection here; Morrow's different policy is assessed separately. Each of the three phases can be a separate sitting. Use the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/reproducibility.md) and [platform equivalents](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md).

### 1. Register an identified model

Use the current project terminal at the repository root with its `.venv` already active. Replace `SELECTED_ID` with your actual selected Threadline run. Inspect the pending version and record its actual number; replace every `VERSION` below with that number.

```bash
python scripts/register_model.py --name threadline-catalog --run-id SELECTED_ID --actor catalog-engineer --reason "Retain the selected Threadline experiment"
python scripts/inspect_registry.py --name threadline-catalog
```

### 2. Retrieve the original recipe

Start with no existing `work/replay` folder. Preserve earlier attempts under another name; native downloads, extraction and shell redirection can overwrite. The native MLflow environment variable refers to the database from the repository root. Inspect the retrieved configuration, dataset and environment records.

```bash
export MLFLOW_TRACKING_URI=sqlite:///work/mlflow/tracking.db
mlflow artifacts download --run-id SELECTED_ID --artifact-path recipe --dst-path work/replay
python -m zipfile -l work/replay/recipe/source.zip
python -m zipfile -e work/replay/recipe/source.zip work/replay/code
```

### 3. Execute the archived code in a fresh environment

Open a **new replay terminal at the repository root**. The extracted project must have no existing `.venv` or repeated-training output. This terminal alone changes into the archived code and installs/activates its own environment. Save the interpreter/import paths and actual outputs. Close this replay terminal after the final command; leave the original project terminal unchanged.

```bash
cd work/replay/code
uv sync --frozen
source .venv/bin/activate
python -c "import sys, catalog_mlops; print(sys.executable); print(catalog_mlops.__file__)"
python scripts/prepare_data.py
python scripts/evaluate.py --run ../recipe > ../saved-evaluation.json
python scripts/train.py --config ../recipe/config.json --output ../retrained
python scripts/evaluate.py --run ../retrained > ../retrained-evaluation.json
```

### 4. Apply the declared checks

Return to the **original project terminal**, still at the repository root with its existing `.venv` active. Expect matching recipe identities, saved-score agreement within `1e-12` and independent-training accuracy/macro-F1 differences at most `0.002`. This is 0.2 percentage points. Retain execution evidence separately. Stop on failed checks.

```bash
python scripts/verify_reproduction.py --run-id SELECTED_ID --recipe work/replay/recipe --retrained work/replay/retrained --saved-evaluation work/replay/saved-evaluation.json --retrained-evaluation work/replay/retrained-evaluation.json --output work/replay/verification.json
```

### 5. Record validation and assign the active alias

Expect replay-passed tags with a retrievable evidence address, followed by an actual active-alias assignment and completed audit events. The replay scope does not replace the separate Threadline business-selection decision.

```bash
python scripts/validate_model.py --name threadline-catalog --version VERSION --evidence work/replay/verification.json --actor catalog-engineer --reason "Clean archived-source replay passed"
python scripts/assign_alias.py --name threadline-catalog --version VERSION --expected-current none --evidence work/replay/verification.json --actor catalog-engineer --reason "Threadline comparison and category tradeoffs reviewed"
python scripts/inspect_registry.py --name threadline-catalog
```

### 6. Check a newly loaded batch and service

Use the retained 20-image intake. Run the first block in the project terminal. For the second block, open a **new service terminal at the repository root**, activate once and wait for Uvicorn startup. Run the final block in the original project terminal. Match actual model identities and the same-image prediction to the batch, then stop the service with **Ctrl+C**.

```bash
python scripts/predict_registry_batch.py --name threadline-catalog --manifest work/intake/manifest.csv --output work/batches/registry-selected
```

```bash
source .venv/bin/activate
uvicorn scripts.registry_api:app --host 127.0.0.1 --port 8000
```

```bash
python scripts/prepare_request.py --image work/intake/56368.png --image-id train:56368 --output work/registry/request.json
curl --fail-with-body -sS http://127.0.0.1:8000/health
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary "@work/registry/request.json" http://127.0.0.1:8000/predict
```

### 7. Compare image groups before labels arrive

Stay in the original project terminal. The fixture exports reference/current research groups and explicit current copies with brightness multiplied by 0.45. Prediction never receives their labels. Expect same-model distribution comparisons; unlabeled reports have no measured correctness.

```bash
python docs/course/exercises/prepare_monitoring_cohorts.py
python scripts/predict_registry_batch.py --name threadline-catalog --manifest work/cohorts/reference/manifest.csv --output work/batches/reference
python scripts/predict_registry_batch.py --name threadline-catalog --manifest work/cohorts/current/manifest.csv --output work/batches/current
python scripts/predict_registry_batch.py --name threadline-catalog --manifest work/cohorts/shifted-current/manifest.csv --output work/batches/shifted-current
python scripts/monitor_batch.py --batch work/batches/reference --output work/monitoring/reference-unlabeled.json
python scripts/monitor_batch.py --batch work/batches/current --output work/monitoring/current-unlabeled.json
python scripts/monitor_batch.py --batch work/batches/shifted-current --output work/monitoring/shifted-current-unlabeled.json
python scripts/compare_cohorts.py --reference work/monitoring/reference-unlabeled.json --current work/monitoring/current-unlabeled.json --output work/monitoring/current-unlabeled-comparison.json
python scripts/compare_cohorts.py --reference work/monitoring/reference-unlabeled.json --current work/monitoring/shifted-current-unlabeled.json --output work/monitoring/shifted-unlabeled-comparison.json
```

### 8. Use known labels to check quality

Add the separate labels to calculate actual quality. Reference/current are different groups; current/darkened-current share source IDs but have changed pixels. Retain both comparisons without confusing a different group with training improvement. Investigation thresholds are declared exercise policy, not universal guarantees.

```bash
python scripts/monitor_batch.py --batch work/batches/reference --labels work/cohorts/reference/labels.csv --output work/monitoring/reference-labeled.json
python scripts/monitor_batch.py --batch work/batches/current --labels work/cohorts/current/labels.csv --output work/monitoring/current-labeled.json
python scripts/monitor_batch.py --batch work/batches/shifted-current --labels work/cohorts/shifted-current/labels.csv --output work/monitoring/shifted-current-labeled.json
python scripts/compare_cohorts.py --reference work/monitoring/reference-labeled.json --current work/monitoring/shifted-current-labeled.json --output work/monitoring/shifted-labeled-comparison.json
python scripts/compare_cohorts.py --reference work/monitoring/current-labeled.json --current work/monitoring/shifted-current-labeled.json --output work/monitoring/paired-brightness-comparison.json
```

### 9. Report the fixed model's final holdout result

Only after selection is fixed, report the approved model on the reserved 10,000-image official test set. Keep the result as final reporting evidence; do not use it to rank new recipes.

```bash
python scripts/evaluate_holdout.py --name threadline-catalog --output work/final-holdout.json
```

Continue with the independent replay, actual bad-version recovery and Morrow handoff in the [Campus lessons](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/README.md). The [optional native-package notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb) exposes model loading, source checks and raw NumPy/scikit-learn observations. [Actual reference evidence](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/evidence/sprint-3) is not a preloaded learner tracking store.
