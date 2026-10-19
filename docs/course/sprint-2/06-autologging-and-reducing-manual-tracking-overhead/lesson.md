✂️
# Autologging and reducing manual tracking overhead

Linden Facilities wants less manual logging work without losing control of its acceptance metric. **Autologging** attaches library-specific hooks that record metadata when fitting happens. It does not know which business metric the team intended to use.


## Work in the repository

Use the [logging comparison](https://github.com/richhiey/ml-llm-ops/blob/main/docs/experiments.md#compare-logging-without-repeating-the-matrix) as an API starting point for your local script. Reuse the existing autologged `alpha=1` matrix run, create one matching manual run only, and retain both IDs in `work/project.json`. Compare keys and metrics through `ws.client.get_run`. No second five-run matrix is needed.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Starting point

Use the tracked pipeline and [MLflow autolog guidance](https://mlflow.org/docs/3.5.1/ml/tracking/autolog/). The helper's `Config(autolog=True)` enables the sklearn hook before fitting and disables automatic model logging; the fitted model is logged explicitly once.

| Held fixed | Deliberately changed |
|---|---|
| Model/data/evaluation | Autologging disabled versus enabled |
| Primary validation metric | Compare added parameter/metric key sets |
| Explicit model artifact | Automatic model logging remains disabled |

## Your task

Reuse the autologged anchor and create one otherwise identical manual run. Use separate run IDs and compare raw parameter and metric keys. Identify at least one field supplied by autologging, such as `ridge__alpha`, and one explicitly supplied acceptance field, `rmse_kwh`. Explain why the auto-generated training score is not the validation decision metric.

Inspect the helper's `mlflow.sklearn.autolog` call and justify `log_models=False`. Describe the convenience/control tradeoff: captured estimator defaults reduce omissions, while explicit metric names and model logging keep the course contract unambiguous. Keep the two saved records and add your configuration explanation; do not repeat the pair of runs.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need hook behavior and settings | [MLflow autolog](https://mlflow.org/docs/3.5.1/ml/tracking/autolog/) |
| You need actual logged keys | `ws.client.get_run(run_id).data` |

## Hints

1. Compare sets of keys, not just the displayed RMSE.
2. A hook must be enabled before `fit` to observe training.
3. Log the business metric explicitly even when training diagnostics appear automatically.

## Checkpoints

Both runs should have the same validation result within `1e-6` kWh if only logging changed. Confirm an actual autolog-specific field exists; a config flag alone is weak evidence. Changing logging mode does not justify changing the split or model factors.

## Learning outcome

Configure autologging for the pipeline and explain the tradeoff between autologging convenience and control over what gets logged.

## Summary

You can show which fields autologging adds and which acceptance fields remain explicit. Less manual logging has not changed the model-selection question.
