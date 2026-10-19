# demand-v1 snapshot card

Confirmed teaching data: 240 synthetic hourly records generated once with Python's `random.Random(731)`. Temperature uniform [-5,32], hour cycles 0..23, occupancy integer 0..100; target formula `45 - 0.7*temperature + 0.3*hour + 0.55*occupancy + Gaussian(0,1.5)`, rounded to six decimals. Generator provenance explains the artifact; bundled CSV bytes, not regeneration, define the snapshot.

| Field | Meaning |
|---|---|
| row_id | Unique synthetic record identifier |
| temperature_c | Forecast temperature, degrees Celsius |
| hour | Planned hour 0..23 |
| occupancy | Planned occupancy percentage 0..100 |
| demand_kwh | Synthetic energy demand target |
| partition | Fixed train (168), validation (48), final (24) |

No personal or operational data. Rows with index modulo 10 in {0,1} are validation; 2 is final; others train. This interleaved teaching split is not a time-series evaluation design. `batch-v1.csv` has 24 planned rows with the same three features and no target. `row_id` aligns outputs; it is never a feature. Snapshots are tracked by SHA256 in each manifest. This snapshot is deliberately simple so operational evidence stays central; do not infer real forecasting readiness.
