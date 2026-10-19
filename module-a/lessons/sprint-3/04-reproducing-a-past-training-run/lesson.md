✂️
# Reproducing a past training run

Linden Facilities asks you to rebuild a previously approved result rather than train something that happens to score similarly. **Reproduction** requires matching the recorded lineage before checking the numeric result.

## Your route through this lesson

Choose and rebuild a past result, checking lineage before numerical agreement. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Original/new IDs, recoverable inputs, comparison and diagnosed scope of proof.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=registry-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use a real past run in your tracking store. If you need a standalone starting state, run `uv run python exercises/prepare-practice.py past-run --state state-past` and read its returned run ID. Use its reproduction artifacts, the registry version linked to that run and the [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md). Use the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md) as an API reference, then choose a past run yourself.

| Recorded input | Recovery evidence |
|---|---|
| Source/data/config | Archive bytes and original manifest |
| Environment | Python, installed distributions, platform and lock |
| Registered artifact | Version source run and logged model URI |

## Select the old result before starting a new one

Choose a past run whose artifacts and registered source-run relationship are available. Save its full ID immediately. The new training run you create later is the reproduction, not a replacement for the evidence you chose. If you use the prepared starting state, read `case.json` and inspect the returned run rather than assuming its ID or version counter.

Use the manifest to form a recovery inventory. For each identity, locate actual bytes or an executable setting. A source hash with no source archive leaves recovery incomplete; a model URI with no accessible artifact directory does too. Check availability before spending time fitting another model.

## Read the reproduction interface as a contract

The guided registry notebook demonstrates `reproduce(workspace, run_id, destination)`: it loads the recorded manifest, checks current source/data/environment identity, reruns the recorded configuration into a new store and writes a comparison. It does not repair mismatched source for you, change the original run or register a replacement version.

Your independent work is to choose the past execution, recover the corresponding content, use the interface correctly and justify the comparison. Consult the worked notebook if the return structure is unfamiliar; then return to the unsolved workspace and your chosen record. A saved demonstration result is not your reproduction.

## Use two checkpoints instead of one final score

| Checkpoint | Question to answer before proceeding |
|---|---|
| Recovery readiness | Do source, snapshot, config, partition, environment and model/source-run links identify the chosen execution? |
| Result agreement | Did a new execution preserve those conditions and meet the absolute RMSE tolerance? |

For the first checkpoint, inspect the downloaded manifest and registered version's source run. For the second, retain the returned original/new IDs and the actual delta. Compute or verify `abs(new_rmse - old_rmse)` against `1e-6`. A tiny delta with a different snapshot does not pass the first checkpoint.

## Investigate a refusal before forcing a rerun

“Restore recorded source and data” means the loaded package or snapshot differs. Locate the original source archive and restore it into a new folder; do not change the recorded hash. An environment refusal means Python, distributions, platform or lock differ; compare the recorded/current fields to identify the difference. A destination-exists refusal protects earlier evidence; choose a new destination instead of overwriting it.

In Colab, reproducing within the same hosted environment is a new-store replay. It is useful, but it does not establish that a minimal local environment matches the hosted package set. Label that scope in the report. The stronger clean-source/new-environment handoff uses the declared local setup and remains a separate proof.

Finish by explaining why changed run IDs are expected, why identical lineage is required, and why the registry source-run link belongs in the inventory even though this reproduction function creates only a training run.

## Your task

Create a lineage inventory with source revision, data hash, exact config, evaluation partition, Python/package/lock versions, model URI and registered version/source run. Recover the corresponding content. If your source differs, restore the archived source into a new folder and rebuild its environment; do not edit the original evidence.

Rerun the recorded configuration into a new state directory. Compare the same evaluation partition using absolute RMSE difference <= `1e-6` kWh. Write `reproduction-report.md` with original and new run IDs, lineage comparison, numeric difference, pass/fail and diagnosis of any mismatch.

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

## Decide what each result proves

A new-state replay proves the training recipe does not depend on the old registry or notebook variables. It does not prove a fresh environment can be built. Mark that distinction in your report and retain the original model version's source-run link even though `reproduce` itself creates a training run, not a registered replacement. To prove the stronger clean starting state, restore the source bundle and locked environment using the specification.

## Learning outcome

Given a past experiment logged in MLflow, use its recorded code, data, configuration, environment, and registry lineage to reproduce the evaluation result within the tolerance declared in the clean-state verification specification.

## Summary

You rebuilt the approved result from its recorded inputs and compared lineage before RMSE. The report shows which conditions agree and which changes in identifiers are expected.
