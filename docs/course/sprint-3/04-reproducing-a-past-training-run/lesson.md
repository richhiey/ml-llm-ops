✂️
# Reproducing a past training run

Linden Facilities asks you to rebuild a previously approved result rather than train something that happens to score similarly. **Reproduction** requires matching the recorded lineage before checking the numeric result.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb) in your local project environment. Find the section for **Reproducing a past training run** using its Campus activity ID **A-S3-04**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Inspect the selected run's `reproduction/manifest.json` in MLflow, then use the API/CLI reference to replay that recorded recipe into a new store. The terminal route is:

```sh
uv run linden-mlops reproduce --destination work/past-replay
```

Inspect `work/past-replay/reproduction-check.json`. The new run ID must differ; lineage must agree and absolute validation RMSE delta must be at most `1e-6` kWh. Keep this result rather than rerun for each question. This task reuses the environment; the fresh-source/environment proof follows in the handoff work.


## Starting point

Use the saved selected validation run and its reproduction artifacts, registry lineage and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md). Use the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) to inspect its recipe before replaying it.

| Recorded input | Recovery evidence |
|---|---|
| Source/data/config | Archive bytes and original manifest |
| Environment | Python, installed distributions, platform and lock |
| Registered artifact | Version source run and logged model URI |

## Your task

Create a lineage inventory with source revision, data hash, exact config, evaluation partition, Python/package/lock versions, model URI and registered version/source run. Recover the corresponding content. If your source differs, restore the archived source into a new folder and rebuild its environment; do not edit the original evidence.

Rerun the recorded configuration into a new state directory. Compare the same evaluation partition using absolute RMSE difference <= `1e-6` kWh. In your working notes, record original and new run IDs, lineage comparison, numeric difference, pass/fail and diagnosis of any mismatch.

Do not replace the original run with a fresh “best” run. A new registry version number may differ; trace its artifact to the source run rather than expecting identical counters.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need the acceptance contract | [Clean state](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md) |
| You need artifact/source relationships | [Registry workflow](https://mlflow.org/docs/3.5.1/ml/model-registry/workflow/) |

## Hints

1. Compare recorded source/data/environment before training.
2. `reproduce` refuses an already existing destination so a stale result cannot masquerade as clean output.
3. Reproduce validation against validation, or final against final. A different partition is a different question.

## Checkpoints

First show recoverable files, not only hash strings. Then show the new execution and metric difference. If either lineage or tolerance fails, diagnose and retain both records. A matching score alone does not pass. Before opening the self-check, decide whether an identical score with a different data hash is a reproduction, and whether a new run ID with matching lineage is a failure. Explain both decisions using the contract rather than executing additional runs.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** a different reproduced run ID, matched source/data/config/partition/environment, and an absolute validation RMSE difference no greater than `0.000001` kWh. Your inventory also connects the original registered version to its source run and recoverable model artifact. A new ID is expected; an equal score with different data fails the lineage requirement.

**How to check:** read the original manifest before the receiving report and compare the underlying values, not filenames. `reproduce` checks source/data/environment before executing and refuses an existing destination. If it refuses, retain the error and restore the mismatched prerequisite; do not change the original manifest. This new-store replay reuses the environment and cannot establish the later fresh-source/environment claim. If your note calls it a clean installation, correct the scope of that claim.

</details>

## Learning outcome

Given a past experiment logged in MLflow, use its recorded code, data, configuration, environment, and registry lineage to reproduce the evaluation result within the tolerance declared in the clean-state verification specification.

## Summary

You rebuilt the approved result from its recorded inputs and compared lineage before RMSE. The report shows which conditions agree and which changes in identifiers are expected.
