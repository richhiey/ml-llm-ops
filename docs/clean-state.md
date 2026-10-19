# Clean-state verification contract

A complete receiving test starts with a new source folder restored from the selected run's export, a new `.venv` installed with Python 3.12 and `uv sync --locked`, and a new state directory. It must succeed without consulting the original tracking store or inherited notebook variables. OS download caches may exist; the model must be retrained from the recorded recipe.

Follow the exact [export and receiving procedure](recovery.md). Source/data SHA256, config, evaluation partition and recorded environment must match. The environment includes Python patch version, installed distribution versions, OS family/architecture and lock hash. A different platform is a deliberate portability investigation, not an identical-environment reproduction.

Acceptance is matching lineage **and** absolute validation RMSE delta at most **0.000001 kWh**, plus the [inference brief](inference-brief.md): 24 finite predictions, preserved input identity/order and complete batch within 60 seconds. Run IDs, paths, timestamps and version counters are expected to differ. Measure batch completion separately from training and setup time.

Diagnose in order: export checksums, source, data, config/partition, Python/package/lock versions, registered source run, then numerical difference. Do not widen tolerance to hide a mismatch. The final partition is reserved until selection is fixed; its result cannot be compared with validation RMSE as if they measured the same rows.
