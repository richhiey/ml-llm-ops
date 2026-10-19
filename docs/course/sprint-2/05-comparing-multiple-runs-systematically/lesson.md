✂️
# Comparing multiple runs systematically

Linden Facilities has logged the matrix, but the planner needs a selection with comparable evidence. Your job is to use the MLflow interface to compare the runs and then verify the winning row against raw records.


## Work in the repository

Start `uv run linden-mlops ui` if the existing server is stopped. In the `linden-demand` experiment, identify and select the five IDs in `work/project.json`. Open their comparison, display `alpha` and validation `rmse_kwh`, and sort by the metric's declared direction. Check controls in the raw rows before deciding. Save your choice explicitly:

```sh
uv run linden-mlops select --run-id ACTUAL_RUN_ID
```

The comparison chart may initially show `training_mean_squared_error`. Use the **Metrics** table’s `rmse_kwh` row, or choose `rmse_kwh` in the chart’s metric selector; the default graph does not change your declared decision metric.

Use the actual chosen ID, not the placeholder. Expect its full recipe in `work/selected-config.json`. This is the selection carried into registry and recovery. A rejected choice needs diagnosis against the raw evidence.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Starting point

Use the five configurations saved in `work/project.json` and raw rows in `work/runs.csv`. Reopen the same store for UI comparison; no new runs are needed.

| Starting evidence | What to inspect |
|---|---|
| matrix-run-ids.json | Five actual execution identities |
| MLflow comparison | Parameter controls and primary/diagnostic metrics |
| Raw selected rows | Unrounded values and source/data identity |

## Your task

Run the printed UI command prefixed with `uv run` in a module terminal and browse to `http://127.0.0.1:5050`. In `linden-demand`, select the five relevant runs and use the comparison control. Display alpha, guard, evaluation partition, validation RMSE and MAE. Find the best configuration for `rmse_kwh` and record the full run ID, value and metric direction.

Save evidence from the actual UI: a comparison capture or a written UI inspection record naming the displayed rows and columns. Check the chosen ID and score in `export_runs(ws)`. If older baseline runs also exist, explicitly select the five fixture runs rather than treating every visible row as part of your declared experiment.

Explain one rejected comparison and why a training metric cannot replace the primary validation metric. Keep final-partition results separate.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need run UI context | [MLflow tracking](https://mlflow.org/docs/3.5.1/ml/tracking/) |
| You need raw comparison data | [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) |

## Hints

1. Inspect controls before sorting any score.
2. RMSE is an error measure. Decide its direction explicitly.
3. Run display names repeat; the unique run ID ties your choice to the artifact.

## Checkpoints

Show five distinct configurations, not five executions of the same alpha. Verify the winning row's raw `data_sha256`, `evaluation_partition` and score. If the UI and export disagree, stop and compare workspace paths before making a recommendation.

## Learning outcome

Use the MLflow UI to compare 5+ experiment runs against each other and identify the best-performing configuration for a given metric.

## Summary

You used the comparison view to identify a configuration and checked its raw run record. The choice is now tied to specific evaluation conditions and a full run ID.
