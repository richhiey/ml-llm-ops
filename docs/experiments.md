# Compare experiments and keep the selected recipe

Finish the range-contract edit and tests before running the comparison. Keep code and data fixed for the five runs. Edit `configs/experiment.json` to declare five distinct positive `alpha` values, including `1` as the logging-comparison anchor. `alpha` controls Ridge regularisation. The declared decision is lowest held-out validation `rmse_kwh`; MAE and training diagnostics help explain behavior.

```sh
uv run linden-mlops plan --config configs/experiment.json
uv run linden-mlops matrix
uv run linden-mlops compare
uv run linden-mlops ui
```

`matrix` executes a completed plan once and saves its IDs in `work/project.json` and raw rows in `work/runs.csv`. Calling it again reopens the same five runs. It does not silently add trials. In MLflow select those five IDs, compare validation RMSE, and inspect equal data/code hashes, guard, partition and distinct alphas. The comparison chart may default to a training diagnostic. Read the `rmse_kwh` row under **Metrics**, or select it explicitly for plotting. Do not compare a final-holdout or different-code run in this group.

Choose the actual best run after checking the table and UI:

```sh
uv run linden-mlops select --run-id ACTUAL_RUN_ID
uv run linden-mlops status
```

Replace `ACTUAL_RUN_ID` with your recorded ID. Selection saves its full config in `work/selected-config.json` and lineage in `work/project.json`. Later registry and recovery operations use that choice, including a custom matrix whose winning alpha differs from the supplied example.

## Compare logging without repeating the matrix

The matrix already includes an autologged run at `alpha=1`. Reuse it. For the independent task, create just one matching manual run; save its ID rather than repeat it on every inspection:

```python
from linden_mlops import Workspace, Config
from linden_mlops.project import Project
p = Project()
ws = Workspace(p.tracking)
rows = p.matrix(ws)
auto_id = rows.loc[rows.alpha.astype(float).eq(1), 'run_id'].iloc[0]
if not p.data.get('logging_pair'):
    manual = ws.run(Config(alpha=1, range_guard=True, autolog=False), name='manual-anchor')
    p.save(logging_pair={'autolog': auto_id, 'manual': manual['run_id']})
for mode, run_id in p.require('logging_pair').items():
    run = ws.client.get_run(run_id)
    print(mode, run_id, run.data.params, run.data.metrics)
    print([a.path for a in ws.client.list_artifacts(run_id)])
```

Put this in a local script and use `uv run python your_script.py`, or explore it in the notebook. Inspect which estimator parameters and training diagnostics autologging adds. The wrapper records validation RMSE, lineage and recovery files explicitly in both cases. Changing logging should not change held-out predictions.

## Review assistant advice

Give your approved assistant only the five comparable raw rows. Ask it to name a run ID using lower validation `rmse_kwh`, explain controls, and distinguish measurements from claims needing other evidence. Keep its actual response in a local note if useful. Check the proposed ID with `verify_summary(p.matrix(ws), proposed_id)` and inspect every prose claim yourself. This numeric check cannot establish cost, future accuracy or production readiness.

A fully accurate response needs no invented correction. Mark each claim supported, inaccurate or unsupported and explain only actual issues. The supplied [example response](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/assistant-summary-reference.md) is a practice fixture, not a substitute for requesting and checking an actual response.
