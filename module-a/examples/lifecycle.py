"""Run from helper root: uv run python examples/lifecycle.py (new state-example)."""
from campus_mlops import Workspace, run_matrix, export_runs, register, approve, activate, batch_predict, reproduce
ws = Workspace("state-example")
runs = run_matrix(ws, autolog=True)
rows = export_runs(ws)
rows.to_csv(ws.path / "runs.csv", index=False)
best = rows.sort_values("rmse_kwh").iloc[0]
version = register(ws, best.run_id)
approve(ws, version, "Five comparable configurations; range contract tests passed; best validation RMSE")
print(activate(ws, version, "Validated candidate"))
print(batch_predict(ws)[1])
print(reproduce(ws, best.run_id, "state-example-reproduced"))
