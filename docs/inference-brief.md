# Linden inference decision brief

Fictional acceptance brief: all 24 planned hourly inputs arrive together. A planner needs a complete CSV within 60 seconds on the learner's local machine. There is no interactive caller. Record one output row per unique `row_id`, finite `prediction_kwh`, the fitted artifact's source run, its model URI and the serving-source revision. The primary model-selection metric is validation RMSE in kWh because large demand errors matter more than small errors in this teaching brief; MAE is diagnostic. The initial teaching validation threshold is RMSE <= 5 kWh.

A **run** identifies the training execution; a **model URI** identifies the stored fitted artifact. Before registry work, `batch_predict(..., model_uri=record["model_uri"])` loads that explicit artifact and legitimately records `resolved_version=None`. Once the registry selects an active model, omit `model_uri`: the job must also record its actual resolved registered version and matching source run. Both routes must satisfy the same row, identity, finiteness and measured completion checks. A registry version is additional identity evidence for alias-based delivery, not a prerequisite for the initial direct-artifact batch.

| Pattern | Latency | Cost | Throughput | Fit here |
|---|---|---|---|---|
| Batch (implemented) | Job completion including model load and output write | Work during scheduled job, no idle HTTP server | Amortizes model loading across 24 rows | Chosen: inputs and deadline are shared |
| Request serving (prepared architectural comparison) | Per-request queue/network/model latency; usually requires warm process | Always-available service, monitoring and concurrency | Depends on workers, batching and resource limits | Useful if planner needs individual immediate responses; not this brief |

No measured request-serving benchmark is supplied. Do not invent a speedup or price. The batch implementation records observed elapsed seconds and rows/second in the named job's JSON; timings vary with hardware and cache. `complete_within_60s` is the acceptance check. In alias mode, `active` resolves once before loading the version URI, so a later alias update affects the next job, not rows in the current job.
