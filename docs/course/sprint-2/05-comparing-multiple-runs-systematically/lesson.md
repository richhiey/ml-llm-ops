✂️
# Comparing multiple runs systematically

Linden Facilities has logged the matrix, but the planner needs a selection with comparable evidence. Your job is to use the MLflow interface to compare the runs and then verify the winning row against raw records.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) in your local project environment. Find the section for **Comparing multiple runs systematically** using its Campus activity ID **A-S2-05**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Start `uv run linden-mlops ui` if the existing server is stopped. In the `linden-demand` experiment, identify and select the five IDs in `work/project.json`. Open their comparison, display `alpha` and validation `rmse_kwh`, and sort by the metric's declared direction. Check controls in the raw rows before deciding. Save your choice explicitly:

```sh
uv run linden-mlops select --run-id ACTUAL_RUN_ID
```

The comparison chart may initially show `training_mean_squared_error`. Use the **Metrics** table’s `rmse_kwh` row, or choose `rmse_kwh` in the chart’s metric selector; the default graph does not change your declared decision metric.

Use the actual chosen ID, not the placeholder. Expect its full recipe in `work/selected-config.json`. This is the selection carried into registry and recovery. A rejected choice needs diagnosis against the raw evidence.


## Starting point

Use the five configurations saved in `work/project.json` and raw rows in `work/runs.csv`. Reopen the same store for UI comparison; no new runs are needed.

| Starting evidence | What to inspect |
|---|---|
| `work/project.json` → `matrix_run_ids` | Five actual execution identities |
| MLflow comparison | Parameter controls and primary/diagnostic metrics |
| Raw selected rows | Unrounded values and source/data identity |

## Your task

Run the printed UI command prefixed with `uv run` in a module terminal and browse to `http://127.0.0.1:5050`. In `linden-demand`, select the five relevant runs and use the comparison control. Display alpha, guard, evaluation partition, validation RMSE and MAE. Find the best configuration for `rmse_kwh` and record the full run ID, value and metric direction.

Save evidence from the actual UI: a comparison capture or a written UI inspection record naming the displayed rows and columns. Check the chosen ID and score in `export_runs(ws)`. If older baseline runs also exist, explicitly select the five fixture runs rather than treating every visible row as part of your declared experiment.

Explain one rejected comparison and why a training metric cannot replace the primary validation metric. If two displayed RMSE values look tied, decide how to resolve that before saving your selection. State which raw evidence would make you withhold a recommendation even if a row shows the lowest score. Keep final-partition results separate.

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

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** the chosen ID belongs to your five saved configurations and has the smallest unrounded validation `rmse_kwh` among comparable rows. Its data/source controls match the group. Your UI record identifies those rows, the alpha values and the displayed primary metric; the raw record supplies the precision needed to settle rounded ties. A different source hash or evaluation partition is a reason to exclude a row, not a reason to celebrate its lower score.

**How to check:** filter by the saved full IDs, check controls, then rank ascending by `rmse_kwh`. For an exact numeric tie the scaffold orders by `run_id`; record that rule rather than inventing a meaningful quality difference. A training diagnostic measures fitted-data behavior and cannot answer the held-out selection question. If your UI and raw winner differ, check the metric selector, rounding and tracking URI before running anything again.

</details>


## Read the notebook figure

![Five observed alpha configurations with validation RMSE and diagnostic MAE in kWh](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/sprint-2/05-comparing-multiple-runs-systematically/assets/experiment-comparison__01__en.png)

This verified reference uses five declared alpha values: 0.2, 0.4, 1, 5 and 20. The horizontal axis is logarithmic; each point is an observed run, without interpolation. The star identifies the smallest unrounded validation RMSE: alpha 0.2, approximately 1.435429 kWh. MAE is diagnostic. Your declared matrix can rank differently; a small lead here does not establish statistical significance or production readiness.

Regenerate this figure from your actual records in the sprint notebook. The [editable SVG](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/05-comparing-multiple-runs-systematically/assets/experiment-comparison__01__en.svg) and [reference observations](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/figures/reference-observations.json) make this author example inspectable.

## Learning outcome

Use the MLflow UI to compare 5+ experiment runs against each other and identify the best-performing configuration for a given metric.

## Summary

You used the comparison view to identify a configuration and checked its raw run record. The choice is now tied to specific evaluation conditions and a full run ID.
