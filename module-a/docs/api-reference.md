# API lookup for independent work

This page names interfaces and failure conditions; choose and connect them yourself. Work in the helper/project root after `uv sync --locked`. Use a Python script, editor or notebook kernel with that environment.

| Need | Public interface | Return / check |
|---|---|---|
| Declare model/logging settings | `Config(alpha=1, range_guard=False, autolog=False)` | Immutable settings; alpha finite and positive |
| Read the snapshot | `ingest()` | Table with row_id, temperature_c, hour, occupancy, demand_kwh, partition |
| Build features | `preprocess(frame, config)` | Three ordered numeric features; guard optional |
| Train/evaluate without tracking | `run_pipeline(config, partition='validation')` | model, metric dictionary, source table |
| Open a local store | `Workspace(path)` | `ws.path`, `ws.uri`, `ws.client`, experiment_id; an existing path reopens evidence |
| Track the pipeline | `ws.run(config, name='baseline', partition='validation')` | Manifest containing actual run ID, metrics and recovery lineage |
| Prepare the reference matrix | `run_matrix(ws, range_guard=True, autolog=False)` | Five manifests; retain returned run IDs |
| Inspect records | `export_runs(ws)` / `ws.client.get_run(run_id)` | Table / raw MLflow record; select your declared IDs explicitly |
| Register a logged artifact | `register(ws, run_id)` | Version string with pending validation tag |
| Validate a candidate | `approve(ws, version, evidence)` | Tags or ValueError; rationale, guard and finite validation RMSE<=5 required |
| Select or roll back | `activate(ws, version, reason)` | Active alias reassigned to an approved version plus audit event |
| Exercise serving | `batch_predict(ws, input_path=None, output_name='batch')` | Output table and observed completion/version evidence |
| Rebuild a past result | `reproduce(ws, run_id, destination)` | New-state comparison; loaded source/data/environment must match; destination must not exist |
| Check numeric advice | `verify_summary(selected_rows, recommended_run_id)` | Winner check; requires 5+ distinct guarded validation configurations, unique IDs and consistent controls |

Lookup reminder: `get_model_version` and `get_model_version_by_alias` are methods on `ws.client`; `MODEL_NAME` is imported from `campus_mlops.lifecycle`. Tagging approval is a course policy, not built-in authorization from MLflow. The helper log covers helper-mediated alias changes only.
