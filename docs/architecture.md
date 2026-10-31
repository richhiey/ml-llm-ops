# Architecture

Linden Facilities needs one complete file of 24 hourly demand predictions within 60 seconds. The bundled data is synthetic. Batch delivery fits this scheduled need; the project does not need an HTTP service to meet it.

```text
historical CSV -> ingest -> validate/preprocess -> fit scaler + Ridge
                                            -> validation metrics + fitted model
planned CSV -> intake checks -> shared feature contract
                            -> explicit logged model or pinned active version
                            -> prediction CSV + job metadata
```

`pipeline.py` owns deterministic stage contracts. Only training rows fit the scaler and regressor. Validation rows select configuration; the reserved final rows are observed after selection is fixed. `range_guard=True` rejects invalid inputs without clipping or mutating them.

`lifecycle.py` owns MLflow execution records, model artifacts, pending/approved tags, the `active` alias and batch execution. A version points to its source run. A batch can load an explicitly identified logged model before registry selection is needed. In alias mode it resolves `active` once and loads that exact version. Each named job records its source run, serving-source revision, input identity, row count and complete delivery time; existing output files cannot be overwritten.

`project.py` persists an explicitly declared experiment population and selection. The CLI and other API consumers reopen those records instead of silently training a new baseline. The historical experiment winner remains separate from the operationally active version after a justified response.

`operations.py` compares reference/current windows with one pinned model and a declared policy. Separate labeled validation data can justify a candidate; comparison and promotion retain their input/model identities. An incident joins actual observations, action events and a fresh job with an explanation and owned follow-up.

`release.py` verifies a declared version, source run and named job against actual registry and output records. Training, serving and current application source must agree. `recovery.py` exports that explicitly selected recipe, including its exact `training-data.csv`, fitted model, source, configuration and environment. Receiving rebuilds it in new source/environment/state and compares lineage and validation results against the recorded tolerance.

The CLI exposes these application operations. Course inputs and provisioning tools under `docs/course/exercises/` are separate consumers of the app APIs; they are neither installed runtime modules nor part of a model's source archive. Notebooks also call the reusable app functions. They do not supply a second implementation or a lesson-progression engine.

The SQLite store, validation policy and mutable JSONL alias log are single-user local infrastructure. See [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) for limits. Completing this project is practice in traceability and recovery, not a claim that a local alias is a secured production deployment.
