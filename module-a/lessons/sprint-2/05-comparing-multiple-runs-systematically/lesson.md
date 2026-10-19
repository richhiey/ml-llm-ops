✂️
# Comparing multiple runs systematically

Linden Facilities has logged the matrix, but the planner needs a selection with comparable evidence. Your job is to use the MLflow interface to compare the runs and then verify the winning row against raw records.

## Your route through this lesson

Inspect the selected population and controls in the actual MLflow UI, then verify raw values. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** A UI inspection record with five full IDs and a defensible metric winner.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=experiment-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use the five configurations you declared and logged. Retain their full run IDs in `matrix-run-ids.json`. For a prepared practice state, run `uv run python exercises/prepare-practice.py matrix --state state-compare` from your project/helper root. This creates five runs and the ID file but does not compare them for you. Use `--state state-compare` when opening the UI. If using your own state, substitute that path consistently. The same-named file produced by the `matrix` CLI identifies only its latest invocation; copy it with your evidence before another matrix run.

| Starting evidence | What to inspect |
|---|---|
| matrix-run-ids.json | Five actual execution identities |
| MLflow comparison | Parameter controls and primary/diagnostic metrics |
| Raw selected rows | Unrounded values and source/data identity |

## Start with a store you can actually inspect

The UI runs locally for this activity. If you used Colab for earlier Python work, clone the repository locally, complete the locked setup and create a local matrix with the prepared command below. Those local executions will have different run IDs. Use their own ID file and raw table; do not expect a Colab runtime's temporary SQLite path to appear on your computer.

Before opening the browser, establish the absolute state path and count the selected IDs. Your starting state must have at least five distinct declared configurations. If it has five repeats of one configuration, return to the plan rather than performing a comparison that cannot answer the question.

## Investigate the view before trusting its ranking

Use three passes through the Runs view. In the first, identify the exact population: experiment and retained run IDs. In the second, inspect controls: snapshot, source, guard and evaluation partition. In the third, display the primary metric and determine the direction before selecting a candidate. This order prevents the most visually prominent score from deciding which question you are answering.

The UI's comparison plot may show a useful trend, but a plot without its controls can still compare incompatible observations. Display alpha alongside validation RMSE and the diagnostic MAE. If a training metric is selected by default, change the displayed metric and record why. You are testing your interpretation of the tool, not just finding a button named Compare.

## Keep an inspection record another person can follow

| Record | Why the receiver needs it |
|---|---|
| Absolute state path and experiment | Reopen the same backend |
| Five full run IDs | Recreate the selected population |
| Displayed parameters/metrics | Know what was compared |
| Selected ID, raw metric and direction | Check the ranking |
| Excluded observation and reason | Understand the comparison boundary |

A screenshot can support this record, but it should not be the only place a clipped ID or rounded value appears. A written UI inspection is acceptable when it names what you actually observed. An API-only sort is useful corroboration, but it does not fulfill the UI part of this task.

## Resolve disagreement instead of choosing the convenient source

If the UI winner and exported winner differ, inspect the state path, selected IDs, filters and metric before blaming the model. A nearby raw score may have rounded to the same displayed value. A later matrix run may have replaced the ID file. A baseline could be included in one population and omitted from the other.

Your final recommendation should specify “best under the declared validation metric among these selected runs”. Then explain one thing that still needs separate evidence before activation. Do not infer that the graph establishes real-world demand forecasting quality or serving readiness.

## Your task

Open `uv run campus-mlops ui --state state-compare` and browse to `http://127.0.0.1:5050`. In `linden-demand`, select the five relevant runs and use the comparison control. Display alpha, guard, evaluation partition, validation RMSE and MAE. Find the best configuration for `rmse_kwh` and record the full run ID, value and metric direction.

Save evidence from the actual UI: a comparison capture or a written UI inspection record naming the displayed rows and columns. Check the chosen ID and score in `export_runs(ws)`. If older baseline runs also exist, explicitly select the five fixture runs rather than treating every visible row as part of your declared experiment.

Explain one rejected comparison and why a training metric cannot replace the primary validation metric. Keep final-partition results separate.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need run UI context | [MLflow tracking](https://mlflow.org/docs/3.5.1/ml/tracking/) |
| You need raw comparison data | [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md) |

## Inspect the interface

In the experiment's Runs view, select exactly your retained IDs and choose **Compare**. Inspect the parameter and metric tables. The plot may initially select a training diagnostic: change it to the declared validation metric. Match full IDs and raw values in your export; displayed rounding is not sufficient for a close comparison. A screenshot is optional evidence, but it must show the actual tool, and your record must identify all five selected runs.

## Hints

1. Inspect controls before sorting any score.
2. RMSE is an error measure. Decide its direction explicitly.
3. Run display names repeat; the unique run ID ties your choice to the artifact.

## Checkpoints

Show five distinct configurations, not five executions of the same alpha. Verify the winning row's raw `data_sha256`, `evaluation_partition` and score. If the UI and export disagree, stop and compare workspace paths before making a recommendation.

## Resolve a close result

If two displayed values round to the same number, use the unrounded `rmse_kwh` values before selecting a winner. Explain separately whether the observed difference is large enough to matter for this synthetic brief; the supplied data does not establish real forecasting uncertainty. An interface ranking is evidence for a metric choice, not proof that a model should become active.

## Learning outcome

Use the MLflow UI to compare 5+ experiment runs against each other and identify the best-performing configuration for a given metric.

## Summary

You used the comparison view to identify a configuration and checked its raw run record. The choice is now tied to specific evaluation conditions and a full run ID.
