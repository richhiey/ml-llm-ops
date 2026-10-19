📝
# Revisiting MLflow in a pipeline context

You have logged parameters and metrics in MLflow before. Linden now needs that record to be created whenever the pipeline runs, including from a terminal. We will trace where the run starts, which calls record its results, and how its model and recovery files stay connected.


## Work in the repository

Use the plan you already declared:

```sh
uv run linden-mlops matrix
uv run linden-mlops compare
uv run linden-mlops ui
```

Expect five actual IDs saved in `work/project.json` and raw rows in `work/runs.csv`. Repeating `matrix` reopens these IDs. Open `http://127.0.0.1:5050`, select `linden-demand`, find one saved ID and open its parameters, metrics and artifacts. Expand `reproduction` to inspect the manifest/config/source archive. Compare those fields with `Workspace.run` in `src/linden_mlops/lifecycle.py`. The table's `rmse_kwh` is the explicit held-out metric. Keep this UI open for the comparison task.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Follow one tracked execution

Use the commands above to run the declared matrix and inspect its raw evidence. A `Workspace` owns a local tracking store. A run is one execution, identified by its unique run ID; an artifact is a stored file from that execution.

1. **Execute the declared configurations.** Keep the five returned run IDs. The fixture varies `alpha` while holding data, split, feature order, scaler fitting, solver, guard and evaluation fixed. Expect five comparable validation rows.
2. **Read the raw record.** Inspect parameters, metrics and the artifact list for one returned ID. Expect explicit held-out `rmse_kwh` and `mae_kwh`, an autologged `ridge__alpha`, training diagnostics and reproduction files. A training metric answers a different question from validation RMSE.
3. **Connect the wrapper to the pipeline.** `Workspace.run` opens a run, calls the pipeline, logs configuration/metrics and stores the fitted model plus recovery metadata. Autologging hooks fitting; the wrapper still records the course's primary validation metric explicitly.
4. **Inspect the same run in MLflow.** Locally, run `uv run linden-mlops ui` in a terminal and open `http://127.0.0.1:5050`. Find the same run ID in `linden-demand`, then inspect its parameters, metrics and artifacts. Keep this UI open for the comparison activity.

## Watch out for

Another successful execution may already be in the store. Select by the five returned IDs rather than every row displayed. A hosted Colab `localhost` URL does not open a server on your laptop; the UI activity uses local execution.

## Quick reference

| Record | Question it answers |
|---|---|
| Parameter | What configuration ran? |
| Validation metric | How did it score on the declared held-out rows? |
| Model artifact | What fitted object was saved? |
| Reproduction manifest | Which recipe and environment produced it? |

## Check your result

Choose one actual run and locate its `alpha`, validation RMSE and recovery manifest in both saved output and MLflow. Explain why the run name alone is insufficient to identify it.

![Revisiting MLflow in a pipeline context: evidence path](assets/revisiting-mlflow-in-a-pipeline-context__01__en.png)

## Learning outcome

Use the provided MLflow setup to log parameters, metrics, and artifacts automatically as part of the cumulative pipeline, building on basic experiment logging from T4 (AI track).

## Summary

The pipeline’s run now carries parameters, validation metrics, a model artifact and recovery files together. You checked the same record through both the API and the local UI.
