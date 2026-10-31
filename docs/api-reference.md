# Application API reference

Use the repository root after `uv sync --locked`. Each operation consumes actual inputs and returned run/version identities. The application has no course progression API.

| Need | Interface | Result / contract |
|---|---|---|
| Model settings | `Config(alpha=1, range_guard=False, autolog=False)` | Immutable config; finite positive alpha |
| Historical input | `ingest(path=None)` | Checked ordered historical schema |
| Feature input | `preprocess(frame, config)` | Validated three features in fixed order |
| Train/evaluate | `run_pipeline(config, partition="validation", data_path=None)` | Fitted model, metrics, historical table; train rows fit, validation rows score |
| Tracking | `Workspace(path)` | Explicit SQLite/artifact store; `path`, `uri`, `client`, `experiment_id` |
| Tracked training | `ws.run(config, name="baseline", partition="validation", data_path=None)` | Manifest with actual run ID, logged-model URI, metrics and recipe |
| Declared experiment | `run_matrix(ws, range_guard=True, autolog=False, alphas=None)` | Runs supplied alpha values; default range is a convenience, no five-run population gate |
| Raw records | `export_runs(ws)` / `ws.client.get_run(run_id)` | Actual params/metrics/tags; select intended IDs before comparing |
| Registration | `register(ws, run_id)` | Pending registered version string |
| Approval | `approve(ws, version, evidence)` | Rationale plus guarded finite validation RMSE `<=5` |
| Selection/rollback | `activate(ws, version, reason)` | Explicit approved alias target and audit event |
| Batch job | `batch_predict(ws, input_path=None, output_name="batch", model_uri=None)` | Output table and metadata; new output name required |
| Numeric recommendation | `verify_summary(rows, recommended_run_id)` | Argmin check on a nonempty declared comparable population; does not review prose |
| Same-environment replay | `reproduce(ws, run_id, destination)` | New store and validation score agreement; exact recipe required |

The public functions above are imported from `linden_mlops`, except `run_pipeline`/feature helpers also live in `linden_mlops.pipeline`. `MODEL_NAME` is in `linden_mlops.lifecycle`.

## Artifact serving and registry serving

An explicit `model_uri` must be an actual logged-model address such as `models:/m-...`, obtained from `Workspace.run`. Its source run is resolved through MLflow; a registry is unnecessary. Metadata has `resolved_version=None` in that mode. With no explicit URI, the job resolves the `active` registry alias once and records its actual version/source run. `input_path` identifies the file whose bytes were hashed. `serving_code_revision` identifies loaded application source independently from the model's training-source record.

## Durable experiment decisions

`Project` from `linden_mlops.project` persists actual experiment decisions in `work/project.json`. `plan(alphas)` accepts distinct positive values; `record_matrix(ws, manifests)` retains actual IDs; `matrix(ws)` reopens them under the same controls/source; `select(ws, run_id)` checks the declared lowest validation RMSE; `selected()` checks retained data/source identity. A completed plan cannot be silently replaced: use a deliberate new `work_dir` for another comparison. It has no lesson-completion flags or required alpha anchor.

## Release and recovery

`verify_release(ws, path)` and `write_release(ws, version, batch_name, destination)` are in `linden_mlops.release`. A user-authored descriptor requires `model_name`, `version`, `run_id`, `batch_name`. Verification checks current active/approved identity, guarded validation lineage and the corresponding actual input/output job. Optional `config`, `data_sha256`, `code_revision`, `serving_code_revision` and `batch_input_sha256` must agree if present; the writer includes these observed fields.

`export_run(ws, run_id, destination, release=None)`, `verify_bundle(bundle)`, `restore_source(bundle, destination)` and `reproduce_bundle(bundle, destination)` are in `linden_mlops.recovery`. A supplied release is verified and its run must match; the enriched descriptor is indexed in the export. CLI export requires `--release FILE` or `--run-id ID`; it never chooses a historical selection implicitly.

```sh
uv run linden-mlops export --release work/release.json --destination work/operational-export
uv run linden-mlops reproduce --state CLIENT_STORE --run-id CLIENT_SOURCE_RUN_ID --destination NEW_REPLAY_STORE
```

Use actual observed values for placeholders. `--state` chooses a store; `--run-id` chooses a recipe. Replay in the installed environment does not prove a new source/environment receiving setup.

## Operational evidence and figures

`monitor`, `train_candidate`, `compare_candidate`, `promote_candidate` and `write_incident` in `linden_mlops.operations` consume explicit file paths and actual candidate versions. See [operations](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md). Input generation and invented incident setup are outside application runtime.

`plot_contract`, `plot_experiments`, `plot_identity` and `plot_recovery` in `linden_mlops.visuals` return Matplotlib Figures with inspectable `linden_data`; monitoring/candidate plots are in `operations`. `save_figure(figure, destination_base)` exports SVG and PNG from one layout and returns a dictionary containing the two output paths. Plots reject missing/incompatible data rather than showing invented passing evidence. See [figure interpretation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/visualizations.md).

## Source identity at release

An intermediate batch can investigate a new serving validation change with an existing fitted model. A final release must use one matching current training and serving source revision: the exported source is the training-time archive. If source changes afterward, revalidate/retrain the intended recipe from the completed source in a deliberate new experiment, then produce a fresh named batch before exporting. The release verifier rejects a source mismatch before creating an export directory.
