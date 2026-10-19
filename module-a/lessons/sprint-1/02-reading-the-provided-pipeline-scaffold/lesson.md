📝
# Reading the provided pipeline scaffold

Linden Facilities has a runnable helper, but a planner's CSV passes through several objects before predictions appear. We will follow that path and match each stage to an observable result.

## Your route through this lesson

Trace actual rows, masks, a fitted object and the written batch output. Run the explained blocks in order, pausing to compare each result with its interpretation. Use the local Python 3.12 setup or the linked Colab route. Terminal commands and notebook Python are different interfaces; the setup guide shows their equivalents.

**Finish with:** A record-level stage trace supported by executed object/file checks.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=raw-to-features). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Before you start

Follow the [helper setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/README.md), work from its folder, and select its Python 3.12 environment. A **virtual environment** isolates the course packages. Open the [pipeline notebook](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb); each code block below runs in that environment.

## Know what you are tracing

The source table has one row per synthetic observation. `row_id` identifies the row; three measured features describe it; `demand_kwh` is the known target; `partition` declares its fitting or evaluation role. A pandas **DataFrame** is the table object passed between functions. Selecting columns changes which values the model receives; selecting rows changes which observations can influence fitting or evaluation.

Keep a short trace table with `stage`, `input object`, `output object` and `check`. Fill it while running the steps. You should finish able to explain a historical evaluation and a planned prediction, including where their paths differ. The repository is the implementation; the notebook is an executable view of it.

## 1. Inspect the raw input

Run the following to see the snapshot rather than guess its shape:

```python
from campus_mlops import *
frame = ingest()
print(frame.groupby('partition').size())
print(frame.head())
```

**Expected:** `final: 24`, `train: 168`, `validation: 48` (printed alphabetically). Check `row_id`, three feature fields, `demand_kwh`, and `partition`. Ingestion checks completeness and unique identifiers; it does not fit a model.

## 2. Follow the feature contract

```python
features = preprocess(frame, Config())
print(features.columns.tolist())
```

**Expected:** `['temperature_c', 'hour', 'occupancy']`. Check the row count and index against `frame`. Removing the target and partition prevents them from becoming accidental predictors. Preprocessing extracts features; the learned scaling is fitted inside training.

## Inspect the rows that each stage receives

After creating `frame` and `features`, run:

```python
train_rows = frame['partition'].eq('train')
validation_rows = frame['partition'].eq('validation')
print(int(train_rows.sum()), int(validation_rows.sum()))
print(features.shape, features.index.equals(frame.index))
assert not (train_rows & validation_rows).any()
```

**Expected:** `168 48`, then `(240, 3) True`. A Boolean **mask** contains one true/false decision per row; `.loc[mask]` selects the rows marked true. The assertion checks that no row is both a fitting row and a validation row. Selecting features for all rows is safe here because this function only checks/extracts values. Fitting a scaler on all those rows would be different: it would learn statistics from held-out inputs.

Open `train` in `pipeline.py`. Its two named steps, `scale` and `ridge`, create a scikit-learn `Pipeline`. Calling its `fit` fits the scaler on the supplied training features and fits Ridge on their transformed values. Calling `predict` later reuses those fitted statistics. Record which object owns them; it is not a separate notebook variable you must recreate for tomorrow's batch.

## 3. Connect training to evaluation

```python
model, metrics, observed = run_pipeline(Config())
print(metrics)
```

**Expected:** validation `rmse_kwh` approximately `1.443003925`, and `mae_kwh` approximately `1.223427215`. RMSE is root mean squared error in the target's units; lower is better. Read `run_pipeline` in `src/campus_mlops/pipeline.py`: it fits on train rows and evaluates on validation rows. Check those masks before accepting the number.

Inside `train`, scikit-learn's `Pipeline` fits the scaler and Ridge model in sequence. Its stored scaler then transforms validation and planned rows before prediction. This library object handles fitted preprocessing; the wider course pipeline also owns ingestion, evaluation and inference. Both use the word pipeline, but cover different boundaries.

## Inspect the fitted object instead of treating it as a black box

After `run_pipeline` returns `model`, inspect:

```python
print(model.named_steps.keys())
print(model.named_steps['scale'].n_features_in_)
print(model.named_steps['ridge'].alpha)
assert model.named_steps['scale'].n_features_in_ == 3
```

**Expected:** named steps `scale` and `ridge`, three input features, and alpha `1.0`. The trailing underscore in scikit-learn attributes such as `n_features_in_` indicates information established by fitting. `alpha` is a configuration setting, while the fitted scaler's statistics and regression coefficients are learned state.

Return to the evaluation masks. `evaluate` calls this model's `predict` on validation features and compares predictions with validation targets. The approximately `1.443` kWh result is tied to those rows and this recipe. If you accidentally evaluate fitting rows, you have changed the question even if the output dictionary still says `rmse_kwh`.

## 4. Follow a planned row into inference

In a terminal run:

```sh
uv run campus-mlops bootstrap --state state
```

In Colab run `course_cli("bootstrap", "--state", str(state/"trace"))` and use that explicit path when reading the output below.

**Expected:** a training manifest, registered version, alias event and inference evidence. A **registry** stores named model versions; an **alias** points to the chosen version. The prepared bootstrap handles these mechanics so you can trace inference now. Open `state/batch.csv` and `state/batch.json`: expect `24` predictions and `resolved_version` matching the bootstrap version. Read `batch_predict` to see that it extracts the same features and loads a fixed version after resolving `active` once.

## Close the trace at the output file

Open the actual planned input and output after bootstrap. This code assumes the terminal command used `--state state` in the same working directory:

```python
from pathlib import Path
import json
import pandas as pd
from campus_mlops.pipeline import DATA
planned = pd.read_csv(DATA / 'batch-v1.csv')
served = pd.read_csv(Path('state') / 'batch.csv')
batch_record = json.loads((Path('state') / 'batch.json').read_text())
assert planned['row_id'].tolist() == served['row_id'].tolist()
print(planned.columns.tolist(), served.columns.tolist())
print(batch_record['resolved_version'], batch_record['rows'])
```

**Expected:** the input has identifiers and the three features; the output has `row_id` and `prediction_kwh`. All 24 identifiers retain their order. In your trace, show where the target disappears, where the fitted model is loaded, and which file becomes useful to the planner. The output alone cannot establish prediction error because tomorrow's observed demand is absent.

For Colab, use the learner workspace's `course_cli('bootstrap', '--state', str(state/'trace'))`, then inspect that printed state path. A local terminal uses `uv run campus-mlops ...`. Do not mix the path from one command with files from the other.

## Watch out for

Run commands from the helper root. `uv --project` selects dependencies but does not change your terminal's working directory. Repeating bootstrap adds a version; a fresh directory starts a separate store. If expected metrics differ, check the helper pin and snapshot before changing the expected value.

## Quick reference

| Inspect | Purpose |
|---|---|
| `ingest()` | Snapshot schema and partitions |
| `preprocess(frame, Config())` | Feature order |
| `run_pipeline(Config())` | Train and held-out evaluation |
| `state/batch.json` | Active-version inference evidence |

![Reading the provided pipeline scaffold: evidence path](assets/reading-the-provided-pipeline-scaffold__01__en.png)

## Trace one record yourself

Choose a `row_id` printed by `ingest()`. Record its partition, three input values and whether its target is used for fitting or held-out evaluation. Then open `batch-v1.csv` and identify a planned row: explain why it has no target and where its prediction is written. Your five-stage map should name concrete objects and files, not only stage labels.

## Learner checklist

- I can locate the three feature fields, the fitting/evaluation masks, and the planned input/output row path.
- I can name one failure and the evidence needed to diagnose it.

## Learning outcome

Trace how data moves through the provided training/inference pipeline scaffold from raw input to served prediction, and label each stage's purpose.

## Summary

You traced raw rows, ordered features, a fitted pipeline and a versioned batch output. Those boundaries give you specific places to check when an extension changes behavior.
