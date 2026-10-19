# Export and recover a selected run

The selected validation run from the experiment is the handoff recipe. Do not replace it with default flags or train another baseline just to write instructions. First inspect `uv run linden-mlops status` and the run's `reproduction/manifest.json`.

## Create portable files in the original project

```sh
uv run linden-mlops export --destination work/handoff-export
uv run linden-mlops restore-source --bundle work/handoff-export --destination ../linden-received
```

Both destinations must be new. Export defaults to the saved selection; `--run-id ACTUAL_RUN_ID` selects another recorded run explicitly. The export contains `manifest.json`, `config.json`, `environment.txt`, `source.tar.gz`, fitted `model/` files and a SHA256 index in `bundle.json`. Keep the export available at an absolute path. A copied SQLite file alone is insufficient because local artifact locations are absolute.

## Receive from a new source folder and environment

Read `environment.python` in the export’s `manifest.json` before installing: use that exact patch version for `--python` if it differs from the interpreter selected by `3.12`. Your runbook should name the recorded version.

In a new terminal, replace `/ABSOLUTE/PATH/handoff-export` below with the export's actual location:

```sh
cd ../linden-received
uv sync --locked --python 3.12
uv run pytest -q
uv run linden-mlops reproduce-export --bundle /ABSOLUTE/PATH/handoff-export --destination work/received
```

This command verifies export checksums, current source/data/environment against the manifest, reruns the recorded configuration on validation rows, registers and approves the resulting version using the local metric policy, activates it and delivers a new batch. The original database and its artifacts are not read. Tests are a separate command because an approval reason does not execute tests.

Read `work/received/recovery-check.json`, `batch.csv`, `batch.json` and `audit.jsonl`. `passed` must be true, all invariant checks true, absolute RMSE delta at most `0.000001` kWh, and the batch complete within 60 seconds. Independently inspect the 24 finite predictions and preserved `row_id` order. New run IDs, paths and version counters may differ; config, data, source, partition and recorded environment must agree.

Keep the original tracking store unavailable during the receiving run when testing portability. Preserve it intact elsewhere; do not delete your work. If a command fails, keep the failure, diagnose the first mismatching invariant and repair your instructions or restore the recorded recipe before trying a new destination.

## Smaller past-run replay

While the original store is available, `uv run linden-mlops reproduce --destination work/past-replay` uses the saved selected run and a new store. It verifies the recipe and validation RMSE, but reuses your installed source and environment. This is useful in registry practice; it is not the fresh-environment receiving test above.

## Final observation

Only after fixing the validation-based selection, run `uv run linden-mlops final`. It evaluates the selected configuration on the reserved final rows and caches that observation in `work/project.json`. Do not retune using that result or promote the final-evaluation run. Registration and recovery continue to refer to the selected validation run.
