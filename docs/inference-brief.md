# Linden inference decision brief

Fictional acceptance brief: all 24 planned hourly inputs arrive together. A planner needs a complete CSV within 60 seconds on the learner's local machine. There is no interactive caller. One output row per unique `row_id`, finite `prediction_kwh`, active model version and source run must be recorded. The primary model-selection metric is validation RMSE in kWh because large demand errors matter more than small errors in this teaching brief; MAE is diagnostic. The initial teaching validation threshold is RMSE <= 5 kWh.

| Pattern | Latency | Cost | Throughput | Fit here |
|---|---|---|---|---|
| Batch (implemented) | Job completion including model load and output write | Work during scheduled job, no idle HTTP server | Amortizes model loading across 24 rows | Chosen: inputs and deadline are shared |
| Request serving (prepared architectural comparison) | Per-request queue/network/model latency; usually requires warm process | Always-available service, monitoring and concurrency | Depends on workers, batching and resource limits | Useful if planner needs individual immediate responses; not this brief |

No measured request-serving benchmark is supplied. Do not invent a speedup or price. The batch implementation records observed elapsed seconds and rows/second in `batch.json`; timings vary with hardware and cache. `complete_within_60s` is the acceptance check. Alias resolves once before loading the version URI, so a later alias update affects the next job, not rows in the current job.
