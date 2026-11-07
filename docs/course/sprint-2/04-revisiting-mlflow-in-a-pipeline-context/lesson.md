📝
# Revisiting MLflow in a pipeline context

Threadline has five hypotheses and configuration files. Now the team needs every training attempt to retain its settings, learning observations and evaluated model together. You will run the planned study through MLflow and inspect what was actually recorded.

Keep your completed intake source fixed for this study. The [README](https://github.com/richhiey/ml-llm-ops/blob/main/README.md) repeats the commands below. Work in your local clone with its `.venv` activated; keep the original untracked baseline as historical evidence.

# 1. Connect the familiar pipeline to MLflow

The underlying MLflow operations are small. This excerpt shows the purpose of each call inside an active run; `metrics` is the evaluation report already calculated from validation predictions.

```python
mlflow.log_params({"epochs": 4, "learning_rate": 0.001})
mlflow.log_metric("validation_macro_f1", metrics["macro_f1"])
mlflow.log_artifact("work/runs/baseline/model.pt")
```

Parameters record the recipe, the metric records an observation, and the artifact preserves a file. `mlflow.start_run()` supplies the run context connecting them. The supplied [tracking implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/tracking.py) applies these package operations around the existing PyTorch training function. Its epoch callback records the learning curve automatically as the pipeline runs.

For project assembly, [track_experiment.py](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/track_experiment.py) reads your configuration, calls the training/tracking adapter and prints the retained IDs. Open that file and follow its call to `tracked_train()`. Training, evaluation and the input scale retain their existing implementations.

# 2. Confirm a baseline under the frozen source

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline --state work/mlflow --name baseline
```

Expect four epochs, a completed local result and `work/experiments/baseline.tracking.json`. The receipt records a full run ID and a native MLflow model URI. Keep these actual values; another machine creates different IDs. The source, split and initial weights are recorded so later comparisons can check their controls.

The author reference reproduced accuracy `0.8380` and macro F1 `0.8322` after the intake extension. That extension changes incoming-image acceptance rather than weight updates. Inspect your own result and stop if the data or configuration differs unexpectedly.

# 3. Execute the five candidate recipes

This guided sequence adopts the reference matrix. Before running, keep your original proposal and record a reconciled plan in `work/experiment-plan.md`: either confirm that your five files match the reference values, or explain each difference and why you are adopting the reference setting for this shared study. Then execute the named reference files below. Each candidate starts from the same baseline settings, with only its named factor changed.

```bash
python scripts/track_experiment.py --config configs/experiments/longer-training.json --output work/experiments/longer-training --state work/mlflow --name longer-training
python scripts/track_experiment.py --config configs/experiments/lower-learning-rate.json --output work/experiments/lower-learning-rate --state work/mlflow --name lower-learning-rate
python scripts/track_experiment.py --config configs/experiments/weight-decay.json --output work/experiments/weight-decay --state work/mlflow --name weight-decay
python scripts/track_experiment.py --config configs/experiments/dropout.json --output work/experiments/dropout --state work/mlflow --name dropout
python scripts/track_experiment.py --config configs/experiments/translation.json --output work/experiments/translation --state work/mlflow --name translation
```

Expect five additional run IDs and five retained result directories. Each starts from fresh weights. Leave the code and evaluation conditions fixed between commands. A candidate's score can decrease; retain that result too.

# 4. Inspect the actual tracking store

In a second terminal at the same repository root, start the native MLflow service.

```bash
source .venv/bin/activate
mlflow ui --backend-store-uri sqlite:///work/mlflow/tracking.db --host 127.0.0.1 --port 5001
```

Open `http://127.0.0.1:5001` in your browser. Choose **Experiments → threadline-cnn**, then open `baseline`. Keep this terminal running while using the UI. The SQLite file stores tracking records; the experiment's file artifact directory retains its files. Both are local and needed to retrieve the study.

| Inspect in the run | What to verify |
|---|---|
| Parameters | All declared settings, including unchanged controls |
| Metrics | Final `validation_macro_f1`, accuracy and per-category results |
| Metric history | `manual/train_loss` and validation observations at steps `1–4` |
| Artifacts | `recipe/` includes configuration, predictions, source archive and checkpoint |
| Logged model | The native PyTorch model is connected to this source run |
| Tags | Source/data/split identities and completed pipeline status |

Open the validation prediction CSV artifact and connect its image IDs to the fixed split. The tracked model accepts normalized float32 tensors shaped `(N, 1, 28, 28)` and returns logits. Its preprocessing declaration and class order travel with it. Model reload verification checks the actual learned weights, not just a filename.

# 5. Keep a usable run ledger

Record each full run ID beside its hypothesis, changed factor and configuration path in `work/experiment-plan.md`. Explain how parameters, metrics and artifacts let another person audit one row.

If model logging is interrupted after local training succeeds, inspect the receipt and retained files. Repeating the identical command resumes logging under the same known ID without retraining. A changed recipe/source/store is rejected. A completed repeat does not count as a new experiment. Preserve a failed attempt instead of concealing it with a new name.

# Watch out for

A blank UI usually means the server points to a different database or you opened the wrong experiment. Do not edit source between candidates. Keep full run IDs distinct from logged-model IDs. The current pipeline logs its final metrics and artifacts explicitly; autologging will be investigated separately. Stop the UI with `Ctrl+C` when finished.

# Quick reference

| Native operation | Evidence |
|---|---|
| `mlflow.log_params()` | Declared recipe |
| `mlflow.log_metric()` | Named numeric observation |
| `mlflow.log_artifact()` / `log_artifacts()` | Retained files |
| `MlflowClient.get_run()` | Raw recorded run data |
| `mlflow ui` | Local inspection and comparison |

## Learning outcome

Use the provided MLflow setup to log parameters, metrics, and artifacts automatically as part of the cumulative pipeline, building on basic experiment logging from T4 (AI track).

## Summary

Threadline has six connected runs: baseline plus five focused candidates. Each score can be traced to its configuration, predictions and learned model, ready for a controlled comparison.
