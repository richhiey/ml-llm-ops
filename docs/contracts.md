# Application input, model and delivery contracts

## Historical training input

`ingest()` accepts the exact column order `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh`, `partition`. Rows must be nonempty, uniquely identified, complete and numeric/finite where required. The provided fixed snapshot has `168` train, `48` validation and `24` reserved final rows. `row_id` and `partition` are not features. Final targets remain closed during development and configuration selection.

## Shared feature validation

`validate_features(frame)` requires a nonempty table containing the three finite numeric features. The completed `validate_ranges(frame)` additionally rejects temperatures outside inclusive `[-30, 50]` degrees Celsius, hours outside inclusive `[0, 23]` or fractional hours, and occupancy outside inclusive `[0, 100]` percent. It rejects the whole invalid call and returns a deep independent copy of valid input, preserving columns, values, order and index. It never clips or filters.

`preprocess(frame, config)` applies the chosen validation boundary and selects the three features in their declared order. `train` fits a `StandardScaler` and Ridge estimator only on training rows. Inference reuses both fitted objects without fitting on planned input.

## Planned input and delivery

The general `batch_predict` entrypoint reads a CSV with complete unique `row_id` and the three valid features. It supports a nonempty input of any size; the baseline does not enforce an exact planned-input column list or `24` input rows. These additional complete-plan guarantees are a concrete new intake-boundary requirement, distinct from the existing correct feature-range guard.

Linden's planner requires all `24` planned predictions in one CSV within `60` seconds. Acceptance checks verify the full `row_id` sequence, finite predictions, exact output columns `row_id`/`prediction_kwh` and actual elapsed time. The timer includes artifact loading, prediction and CSV writing, excluding environment setup and training. Whole-job throughput is delivered rows divided by seconds, not network-request latency.

A batch takes an explicit logged-model URI or resolves `active` once and pins that model version. Metadata records source run, model URI, resolved version when applicable, input path/hash and `serving_code_revision`. Source-run training identity and current serving source are separate facts. Existing CSV/JSON names are never overwritten.

## Experiment and lifecycle policies

Application plans accept a nonempty set of distinct positive finite `alpha` values. A particular experiment may specify five configurations; that population size is not a universal runtime constraint. Comparisons require distinct actual IDs/configurations, shared data/source identity, guarded validation rows and finite nonnegative primary error. Lower validation `rmse_kwh` decides; `mae_kwh` and training metrics diagnose behavior.

Registry approval requires a rationale, `range_guard=True`, validation evaluation and finite RMSE `<=5` kWh. Only approved versions may be active. This is a local single-user application policy, not built-in MLflow authorization. The mutable audit log covers helper-mediated changes and is not a tamper-proof control plane.

A release descriptor binds an approved active version to its actual source run and completed batch. Export consumes that verified descriptor or an explicitly named run. Recovery requires matching source/data/config/partition/environment and absolute validation RMSE difference `<=1e-6` kWh, plus independent delivery acceptance. See [recovery](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md).

## Source identity at release

An intermediate batch can investigate a new serving validation change with an existing fitted model. A final release must use one matching current training and serving source revision: the exported source is the training-time archive. If source changes afterward, revalidate/retrain the intended recipe from the completed source in a deliberate new experiment, then produce a fresh named batch before exporting. The release verifier rejects a source mismatch before creating an export directory.
