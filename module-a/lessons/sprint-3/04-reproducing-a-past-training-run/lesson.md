✂️
# Reproducing a past training run

Linden Facilities asks you to rebuild a previously approved result rather than train something that happens to score similarly. **Reproduction** requires matching the recorded lineage before checking the numeric result.

**Continue here:** [Sprint 3 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=registry-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use a real past run in your tracking store. If you need a standalone starting state, run `uv run python exercises/prepare-practice.py past-run --state state-past` and read its returned run ID. Use its reproduction artifacts, the registry version linked to that run and the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Use the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md) as an API reference, then choose a past run yourself.

| Recorded input | Recovery evidence |
|---|---|
| Source/data/config | Archive bytes and original manifest |
| Environment | Python, installed distributions, platform and lock |
| Registered artifact | Version source run and logged model URI |

## Your task

Create a lineage inventory with source revision, data hash, exact config, evaluation partition, Python/package/lock versions, model URI and registered version/source run. Recover the corresponding content. If your source differs, restore the archived source into a new folder and rebuild its environment; do not edit the original evidence.

Rerun the recorded configuration into a new state directory. Compare the same evaluation partition using absolute RMSE difference <= `1e-6` kWh. In the notebook, record original and new run IDs, lineage comparison, numeric difference, pass/fail and diagnosis of any mismatch.

Do not replace the original run with a fresh “best” run. A new registry version number may differ; trace its artifact to the source run rather than expecting identical counters.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need the acceptance contract | [Clean state](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) |
| You need artifact/source relationships | [Registry workflow](https://mlflow.org/docs/3.5.1/ml/model-registry/workflow/) |

## Hints

1. Compare recorded source/data/environment before training.
2. `reproduce` refuses an already existing destination so a stale result cannot masquerade as clean output.
3. Reproduce validation against validation, or final against final. A different partition is a different question.

## Checkpoints

First show recoverable files, not only hash strings. Then show the new execution and metric difference. If either lineage or tolerance fails, diagnose and retain both records. A matching score alone does not pass.

## Learning outcome

Given a past experiment logged in MLflow, use its recorded code, data, configuration, environment, and registry lineage to reproduce the evaluation result within the tolerance declared in the clean-state verification specification.

## Summary

You rebuilt the approved result from its recorded inputs and compared lineage before RMSE. The report shows which conditions agree and which changes in identifiers are expected.
