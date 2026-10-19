📝
# Reading the provided pipeline scaffold

Linden Facilities has a runnable helper, but a planner's CSV passes through several objects before predictions appear. We will follow that path and match each stage to an observable result.

**Continue here:** [Sprint 1 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=raw-to-features). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Follow the data in the notebook

1. **Inspect the input** at **Inspect the stage boundaries**. Group by `partition` and read the feature columns. Expect `168` training, `48` validation and `24` reserved final rows. `row_id` aligns records; `demand_kwh` is the target. Neither is a feature.
2. **Trace fitting** at **Trace preparation, fitting and evaluation**. The Boolean masks select matching features and targets. `StandardScaler` learns training means and scales inside the fitted model; validation calls `predict` without fitting again. Expect validation RMSE near `1.443003925` kWh.
3. **Inspect fitted state**. The model contains `scale` and `ridge`, with three input features. Contrast learned scaler statistics with the configured `alpha`. Check that the training and validation masks never overlap.
4. **Follow planned rows** at **Complete the inference stage**. The supplied lifecycle setup makes a model available for the batch. Inspect the returned CSV and version. Expect `24` finite predictions, in the same `row_id` order as the planned input, within the `60`-second brief. Planned rows have no known demand, so this output cannot measure prediction error.

## Watch out for

A matching row count can hide reordered records. Compare identifiers as well as counts. Fitting a new scaler on planned data changes the feature representation; reuse the stored scaler and estimator together.

## Quick reference

| Object | Purpose |
|---|---|
| `ingest()` | Read and check historical rows |
| `preprocess()` | Validate and select ordered features |
| `train()` / `evaluate()` | Fit on training rows / score held-out rows |
| `batch_predict()` | Resolve the selected model and write planned predictions |

## Check your trace

Choose one historical row and one planned row. Explain which has a known target, where fitting occurs, and which fitted object reaches inference. Point to the notebook output that checks row alignment.

![Reading the provided pipeline scaffold: evidence path](assets/reading-the-provided-pipeline-scaffold__01__en.png)

## Learning outcome

Trace how data moves through the provided training/inference pipeline scaffold from raw input to served prediction, and label each stage's purpose.

## Summary

You traced raw rows, ordered features, a fitted pipeline and a versioned batch output. Those boundaries give you specific places to check when an extension changes behavior.
