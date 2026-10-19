# Contracts and bounded extensions

`Config(alpha=1.0, range_guard=False, autolog=False)` is immutable. Alpha must be finite and positive. Default training selects validation evaluation. Source `demand-v1.csv` has 168 train, 48 validation and 24 final rows. Every partition is fixed in the snapshot; do not resplit during the five-run matrix.

`preprocess(frame, config)` returns three numeric features ordered `temperature_c`, `hour`, `occupancy`. It preserves index and rows. `train` fits scaler statistics using train rows only. The target `demand_kwh`, `row_id` and `partition` never become model features. Both inference and training call the same feature contract.

## Guided extension

Inspect `validate_ranges`. The supported extension is enabled through `range_guard=True`. A deliberate baseline without it accepts numeric out-of-range readings; the extension rejects temperatures outside [-30,50], hours outside [0,23] or fractional hours, and occupancy outside [0,100]. It copies valid inputs rather than mutating them. This is a validation stage before preprocessing, not clipping and not learning from validation data.

Tests must cover exact lower/upper bounds, outside each bound, NaN/inf, fractional hour, missing features, valid row/index preservation and downstream baseline-vs-extension metric equality. Keep the model, split and metric unchanged when testing the extension. For the checkpoint, submit the actual completed source addition from the finite-only starter, or another bounded validation addition, with accepted/rejected examples and an explained diff. A second extension is not required; merely changing a flag in the already solved reference is insufficient.

## Five-run fixture

| alpha | Comparison |
|---:|---|
| 0.01 | Anchor |
| 0.1 | Alpha only versus anchor |
| 1 | Alpha only versus anchor |
| 10 | Alpha only versus anchor |
| 100 | Alpha only versus anchor |

All use the same source revision, snapshot, feature order, train/validation partition, scaling, solver and `range_guard=True`. Autologging can be enabled for all five; it changes logging, not the estimator. Changing the guard or partition requires a separately declared comparison. The helper labels the evaluation partition in its comparison_group tag; that tag alone is not proof that every control matches. `verify_summary` requires explicitly selected unique IDs and at least five distinct alpha configurations; it rejects missing fields, mixed groups, non-finite RMSE and changed data/code/guard/partition instead of silently excluding rows. It ranks RMSE; it cannot validate semantic claims such as deployment readiness.

## Lifecycle policy

Register logs `validation_status=pending`. `approve` requires a rationale, range guard and finite validation RMSE <= 5 kWh. Passing this teaching threshold does not imply real deployment readiness. `activate` requires approved status and a reason; rollback uses the same operation to reassign `active` to the previous approved version. Current alias state proves only the current pointer. JSONL events record timestamp, old/new versions, source run and reason for helper-mediated changes; direct UI/API mutations outside the helper are not captured. Retain both registry state and the events. A failed event write after alias reassignment is possible; compare them and reconcile rather than assume atomicity.

The environment manifest records every installed distribution version plus Python, operating-system family and machine architecture. A lock is the installation recipe; this observation detects an altered installed dependency even if the lock file itself was not changed. Reproduction compares this manifest before running.
