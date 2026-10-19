✂️
# Comparing multiple runs systematically

Linden Facilities has logged the matrix, but the planner needs a selection with comparable evidence. Your job is to use the MLflow interface to compare the runs and then verify the winning row against raw records.

**Continue here:** [Sprint 2 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb#scrollTo=experiment-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use the five configurations already logged in this sprint notebook. Their IDs are in `matrix-run-ids.json` inside the printed `ws.path`. Keep that same state for the UI comparison; you do not need another five runs. The notebook prints the command for your actual store. If you are recovering lost practice state, the optional `prepare-practice.py matrix` fixture can create a new one, but it is not an additional assignment.

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
| You need raw comparison data | [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md) |

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
