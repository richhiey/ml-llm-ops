📝
# Revisiting MLflow in a pipeline context

Threadline has five proposed training changes intended to improve its clothing-category suggestions. The catalog lead needs to see which change helped and retrieve the model that produced that result. You will use MLflow to keep each training attempt's recipe, measurements and saved model together.

Keep your completed intake source fixed for this study. The [README](https://github.com/richhiey/ml-llm-ops/blob/main/README.md) repeats the commands below. Work in your local clone with its `.venv` activated; keep the original untracked baseline as historical evidence.

# 1. Connect the familiar pipeline to MLflow

A **run** is one execution of a recipe. **Parameters** record its settings, **metrics** record measured results, and **artifacts** are saved files. The following excerpt shows those three MLflow operations inside an active run. Here, `metrics` is the evaluation report already calculated from validation predictions.

```python
mlflow.log_params({"epochs": 4, "learning_rate": 0.001})
mlflow.log_metric("validation_macro_f1", metrics["macro_f1"])
mlflow.log_artifact("work/runs/baseline/model.pt")
```

`mlflow.start_run()` opens the record to which those calls belong. The checkpoint `model.pt` contains the learned weights used to reload the CNN. The supplied tracking implementation applies these package operations around the existing PyTorch training function. A **callback** is a function invoked at a particular point in an operation. This callback runs after each epoch, recording how the measurements change over training. [Tracking implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/tracking.py)

For project assembly, `track_experiment.py` reads the configuration, calls `tracked_train()` and prints the saved identities. Trace that call into the source to see where it invokes training and the MLflow operations above. Training uses the existing CNN and pixel preparation. Keep this Python code fixed while the recipe files vary. [Training entry script](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/track_experiment.py)

# 2. Confirm a baseline with unchanged code

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline --state work/mlflow --name baseline
```

Expect four epochs, a completed local result and `work/experiments/baseline.tracking.json`. This **receipt** is a small saved record connecting the local result to its MLflow run. Its run ID identifies the execution. Its **model URI** is the address MLflow returns for loading that run's logged model. Keep both actual values, since another machine creates different identities.

The baseline is the reference configuration for your comparisons. Each run constructs a new CNN, and the fixed seed repeats its initial weight values within this environment. The source code, image split and starting weights are recorded so these conditions can be checked.

The author reference reproduced accuracy `0.8380` and macro F1 `0.8322` after the intake extension. Accuracy counts correct predictions overall, while macro F1 gives each category equal weight. The extension controls which incoming images are accepted. Inspect your own training result and stop if the data or configuration differs unexpectedly.

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

In a second terminal at the same repository root, start MLflow's own browser interface, or **UI**.

```bash
source .venv/bin/activate
mlflow ui --backend-store-uri sqlite:///work/mlflow/tracking.db --host 127.0.0.1 --port 5001
```

Open `http://127.0.0.1:5001` in your browser. Choose **Experiments → threadline-cnn**, then open `baseline`. Keep this terminal running while using the UI. **SQLite** is the database storing run records in `tracking.db`. Saved artifacts live in a separate directory. Together they form the **tracking store**, the local records and files needed to retrieve this study.

| Inspect in the run | What to verify |
|---|---|
| Parameters | All declared settings, including unchanged controls |
| Metrics | Final `validation_macro_f1`, accuracy and per-category results |
| Metric history | `manual/train_loss` and validation observations at steps `1–4` |
| Artifacts | `recipe/` includes configuration, predictions, source archive and checkpoint |
| Logged model | The saved PyTorch model is connected to this source run |
| Tags | Labels recording source/data/split identities and completed pipeline status |

Open the validation prediction CSV artifact and connect its image IDs to the fixed split. The logged CNN accepts prepared floating-point image arrays, `float32` tensors shaped `(N, 1, 28, 28)`, and returns **logits**, the ten raw category scores. Its expected pixel scale and category order travel with it. Reload verification checks that the saved model has the same learned weights as the evaluated checkpoint.

# 5. Keep a usable run ledger

Your **run ledger** is the list connecting each planned comparison to its execution. Record each full run ID beside its hypothesis, changed factor and configuration path in `work/experiment-plan.md`. Explain how another person can follow one row from settings to measured results and saved weights.

If model logging is interrupted after local training succeeds, inspect the receipt and retained files. Repeating the identical command resumes logging under the same known ID without retraining. A changed recipe/source/store is rejected. A completed repeat does not count as a new experiment. Preserve a failed attempt instead of concealing it with a new name.

# Watch out for

A blank UI usually means the server points to a different database or you opened the wrong experiment. Keep the Python code fixed between candidates. A run ID identifies an execution, while the returned model URI loads its saved model. The current pipeline explicitly records its final metrics and artifacts. Automatic capture from the training tool is a separate logging option. Stop the UI with `Ctrl+C` when finished.

# Quick reference

| MLflow operation | Evidence |
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
