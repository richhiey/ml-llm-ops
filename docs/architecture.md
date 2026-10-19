# Architecture

Linden Facilities needs one complete file of 24 hourly demand predictions within 60 seconds. The bundled data is synthetic. Batch delivery fits this scheduled need; the project does not need an HTTP service to meet it.

```text
historical CSV -> ingest -> validate/preprocess -> fit scaler + Ridge
                                            -> validation metrics + fitted model
planned CSV -> same feature contract -> saved active model -> prediction CSV
```

`pipeline.py` owns deterministic stage contracts. Only training rows fit the scaler and regressor. Validation rows select configuration; the reserved final rows are observed after selection is fixed. `range_guard=True` rejects invalid inputs without clipping or mutating them.

`lifecycle.py` owns MLflow execution records, model artifacts, pending/approved tags, the `active` alias and batch execution. A version points to its source run. A batch resolves the alias once, loads that exact version and records row count, source run and complete elapsed time.

`project.py` persists the experiment plan and the student's explicit selection. Notebooks and the CLI reopen the same records instead of training a new baseline. `recovery.py` exports a run's recorded source, environment, data, configuration and model, then checks a receiving execution against those bytes and the declared tolerance.

`scenarios.py` creates isolated client incidents for practice; it never changes the main project's selection. `dev.py` runs saved-source probes in fresh processes for notebook exploration. The CLI is an entry point to these same APIs, which you can inspect and use in your own scripts.

The SQLite store, validation policy and mutable JSONL alias log are single-user local infrastructure. See [contracts](contracts.md) for limits. Completing this project is practice in traceability and recovery, not a claim that a local alias is a secured production deployment.
