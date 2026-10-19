✂️
# Autologging and reducing manual tracking overhead

Linden Facilities wants less manual logging work without losing control of its acceptance metric. **Autologging** attaches library-specific hooks that record metadata when fitting happens. It does not know which business metric the team intended to use.

## Your route through this lesson

Vary logging only, inspect added fields and explain what remains explicit. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Two source records, key differences, metric agreement and convenience/control explanation.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=experiment-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use the tracked pipeline and [MLflow autolog guidance](https://mlflow.org/docs/3.5.1/ml/tracking/autolog/). The helper's `Config(autolog=True)` enables the sklearn hook before fitting and disables automatic model logging; the fitted model is logged explicitly once.

| Held fixed | Deliberately changed |
|---|---|
| Model/data/evaluation | Autologging disabled versus enabled |
| Primary validation metric | Compare added parameter/metric key sets |
| Explicit model artifact | Automatic model logging remains disabled |

## Use logging as the factor, not the model

Choose one alpha and declare the same snapshot, source, guard and validation partition for both executions. Create a new workspace for the pair or retain their returned IDs separately from your model-selection matrix. The question is what the logging hook adds; changing alpha or the evaluation rows would confound that investigation.

The earlier logging mechanism is still present: the helper records its held-out metrics and named model explicitly. With `autolog=True`, MLflow's sklearn hook also observes fitting. You should therefore look for added fields while checking that the model's validation result remains unchanged within the declared tolerance.

## Read a raw record before comparing two

For each chosen ID, inspect `ws.client.get_run(run_id).data`. Parameters and metrics are dictionaries with field names as keys. Comparing their key sets reveals which names appear only in the autolog-enabled execution; comparing only a UI's visible columns may hide fields that were captured but not displayed.

Distinguish three classes in your report:

| Class | What to investigate |
|---|---|
| Explicit run context | Alpha, source/data identities and evaluation partition |
| Explicit acceptance metric | Validation `rmse_kwh` and diagnostic `mae_kwh` |
| Autolog additions | Estimator settings such as `ridge__alpha` and training diagnostics |

The estimator can appear as a nested step in a scikit-learn pipeline. A name such as `ridge__alpha` records that estimator's parameter; it is not a second experiment factor you deliberately changed. Training RMSE, when present, describes the fitting rows. Keep it separate from validation RMSE even though both are error measures.

## Decide what convenience is worth keeping

Explain one omission that autologging could prevent for a teammate, and one decision it cannot make for them. Capturing defaults can help reconstruct an estimator. Choosing the primary business metric, deciding the evaluation population and approving a version remain explicit responsibilities.

Inspect `log_models=False`: the helper disables automatic model logging because it already logs one explicitly named fitted model. A second automatically logged model could make the artifact choice ambiguous. The setting is a deliberate course design choice, not a rule that automatic model artifacts are always undesirable.

## Diagnose an unexpected result

If no additional fields appear, verify that the enabled configuration actually reached `Workspace.run` and that the run finished. If the scores differ, inspect configs and source/environment before concluding that logging improved the model. If a fit fails, hooks should still be disabled afterward; the helper's `finally` cleanup is worth locating because later executions share the Python process.

Submit the two IDs, key-set differences, one inspected added value, primary-metric comparison and your convenience/control explanation. The checkbox `autolog=True` alone is not enough to establish that fitting was observed.

## Your task

Run the same guarded alpha configuration with autologging disabled and enabled. Use separate run IDs and compare raw parameter and metric keys. Identify at least one field supplied by autologging, such as `ridge__alpha`, and one explicitly supplied acceptance field, `rmse_kwh`. Explain why the auto-generated training score is not the validation decision metric.

Inspect the helper's `mlflow.sklearn.autolog` call and justify `log_models=False`. Describe the convenience/control tradeoff: captured estimator defaults reduce omissions, while explicit metric names and model logging keep the course contract unambiguous. Save the two raw records and your configuration explanation.

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

## Control the logging experiment

Choose one alpha and keep guard, snapshot, source and validation partition fixed. Vary only the logging mode, then report the set of parameter/metric keys added with autologging. State why those extra fields would help another engineer diagnose a result. If the primary metrics differ, investigate changed configuration or process state instead of crediting logging with a model improvement. Capture the two IDs separately from the five-run selection population.

## Learning outcome

Configure autologging for the pipeline and explain the tradeoff between autologging convenience and control over what gets logged.

## Summary

You can show which fields autologging adds and which acceptance fields remain explicit. Less manual logging has not changed the model-selection question.
