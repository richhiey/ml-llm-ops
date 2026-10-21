✂️
# Autologging and reducing manual tracking overhead

Linden Facilities wants less manual logging work without losing control of its acceptance metric. **Autologging** attaches library-specific hooks that record metadata when fitting happens. It does not know which business metric the team intended to use.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) in your local project environment. Find the section for **Autologging and reducing manual tracking overhead** using its Campus activity ID **A-S2-06**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Use the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) and `Workspace.run` in `src/linden_mlops/lifecycle.py` to choose the logging configuration for a small local comparison script. Reuse the existing autologged `alpha=1` matrix run, create one matching manual run only, and retain both IDs as `logging_pair` in `work/project.json`. The pair must be reused when your script is reopened. No second five-run matrix is needed.


## Starting point

Use the tracked pipeline and [MLflow autolog guidance](https://mlflow.org/docs/3.5.1/ml/tracking/autolog/). The helper's `Config(autolog=True)` enables the sklearn hook before fitting and disables automatic model logging; the fitted model is logged explicitly once.

| Held fixed | Deliberately changed |
|---|---|
| Model/data/evaluation | Autologging disabled versus enabled |
| Primary validation metric | Compare added parameter/metric key sets |
| Explicit model artifact | Automatic model logging remains disabled |

## Your task

Reuse the autologged anchor and create one otherwise identical manual run. Use separate run IDs and compare raw parameter and metric keys. Before executing, predict one parameter or diagnostic that should appear only with autologging and one acceptance field that should remain in both records. Configure the matching run through `Config`, then identify actual added keys and compare them with that prediction. Explain why the auto-generated training score is not the validation decision metric.

Inspect the helper's `mlflow.sklearn.autolog` call and justify `log_models=False`. Record where the hook is enabled relative to fitting, what is still logged explicitly, and how the hook is reset after the run. Use those observations to explain the convenience/control tradeoff. Keep the two saved records and add your configuration explanation; do not repeat the pair of runs.

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

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** two distinct IDs with matching alpha, guard, data/source and evaluation partition; only the logging flag differs. Both contain explicit validation `rmse_kwh` and agree within `1e-6` kWh. The autologged record additionally has estimator keys such as `ridge__alpha` and training diagnostics. The `autolog=True` parameter alone does not prove the hook captured anything.

**How to check:** construct the manual `Config` from the anchor's settings with `autolog=False`, save its returned ID, and compare `run.data.params` and `run.data.metrics` key sets. In `Workspace.run`, the sklearn hook is configured before `run_pipeline` fits the estimator; the `finally` block disables it afterwards. `log_models=False` avoids an additional automatic model copy because `log_model` explicitly records the model with its signature and example. These checks explain convenience and retained control using actual fields. If scores differ, inspect controls before blaming logging. The [worked comparison](https://github.com/richhiey/ml-llm-ops/blob/main/docs/experiments.md#compare-logging-without-repeating-the-matrix) is available after your attempt if script structure is blocking progress.

</details>

## Learning outcome

Configure autologging for the pipeline and explain the tradeoff between autologging convenience and control over what gets logged.

## Summary

You can show which fields autologging adds and which acceptance fields remain explicit. Less manual logging has not changed the model-selection question.
