✂️
# Integrating pipeline, tracking, and registry

Linden Facilities has training, registry and operational-response records. Another engineer needs a release that identifies the model actually intended for service and the recipe behind it. A plausible run ID or collection of successful files is insufficient.

## Start with an evidence inventory

Continue the same clone and cumulative workspace. Begin `work/HANDOFF.md` with criterion, existing record, observed or missing state, dependency and next check. Reuse the explained extension, distinguishing tests and original experiment comparison. Keep the historical five-run choice distinct from the operationally active model: a justified response can select a feedback-trained version without rewriting that experiment.

| Criterion | Question your evidence must answer |
|---|---|
| Connected execution | Which run trained the intended registered artifact? |
| Explained extension | What application behavior did you add and how do its tests distinguish correct from incomplete behavior? |
| Response | Which signal, labels and candidate comparison justified the action? |
| Delivery | Which intended version produced a complete, ordered planner file within the brief? |
| Reproducibility | Can the exact selected recipe be replayed, then received from fresh source/environment/state? |

Order the remaining checks by dependency. Keep missing evidence visible; a planned command is not a completed result.

## Your task — declare a usable release

Create `work/release.json` as the application's release descriptor. This file will be consumed by export; it is not a worksheet invented for this lesson. Use the actual intended active artifact and the job that served it.

| Required field | Value to establish from the application |
|---|---|
| `model_name` | Registered model name, here `dev.linden-demand` |
| `version` | Actual intended active version as a string |
| `run_id` | That registered artifact's actual source run |
| `batch_name` | Existing job name without the extension, such as `response-batch` |

Inspect the registry and raw run/job records before writing values. Do not substitute the matrix winner by habit. A source run and batch from different models do not become consistent merely because their predictions look similar.

Use `verify_release(workspace, path)` from the [release source](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/release.py) to check your descriptor against approved/current model state, source lineage and the actual batch CSV/JSON. Read the failure and repair your declared selection or genuinely missing evidence. Do not edit raw model, run or job records to make a descriptor pass. Preserve an unsuccessful attempt when it reveals a mismatch.

The release also requires the training run, serving job and current application source to agree. If you change application code after fitting, deliberately revalidate the intended recipe in a new run/version and produce a fresh named batch before export. Preserve the earlier records; do not relabel an old run as current or rerun a parameter search merely to repair lineage.

The application can record/check additional `config`, `data_sha256`, `code_revision` and `batch_input_sha256` fields. Inspect those actual values; a field copied from another release must be rejected. `write_release` provides an application-generated descriptor when you later automate the same operation, but your first task is to establish the correct identities yourself.

## Replay the release's actual source

Resolve the intended version using the [registry/API interfaces](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md). Predict which recipe invariants should match before invoking `reproduce(workspace, release_run_id, new_destination)` from the [lifecycle source](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/lifecycle.py). The source ID must be the one in your validated release descriptor.

A feedback-trained run retains `training-data.csv` among its reproduction artifacts. Replay consumes those bytes. It refuses changed source/environment and never tunes from final rows. If a retained run belongs to older application code, restore its exported source separately; do not edit a manifest to claim the current checkout is identical.

Open `reproduction-check.json`, inspect the new raw validation run and independently calculate the absolute RMSE difference. It must be at most `0.000001` kWh on the same validation population. Record the new run ID. This replay uses a new store in the current source/environment. A fresh-source/fresh-environment receiving proof remains a separate boundary.

## Working with documentation

The [release source](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/release.py) defines descriptor fields and checks. The [recovery runbook](https://github.com/richhiey/ml-llm-ops/blob/main/docs/recovery.md) explains replay versus clean receiving. Use those contracts to choose arguments; do not ask an assistant to invent a missing interface.

## Hints

<details><summary>Hint 1 — Follow the artifact backward</summary>

Start with the current intended registered version, then its raw source run, training snapshot and configuration. Keep the old experiment decision as historical evidence.

</details>
<details><summary>Hint 2 — Follow the job forward</summary>

The descriptor must name a real job whose version and source agree with the release. If you have only stale output, run a distinctly named new batch from the intended version; do not alter an old job's metadata.

</details>

## Checkpoints

Your inventory has evidence or a bounded next action for every criterion. `release.json` describes one approved/current artifact and its actual output. The selected snapshot/configuration/source/environment support replay within tolerance. Export will read this same descriptor, so the work carries forward into the actual handoff.

<details><summary>Check after creating the release and inspecting your replay</summary>

**Result you should get:** a valid application release descriptor, a dependency-ordered handoff inventory and a new-store replay of its exact recorded recipe. The original experiment decision may differ from the operational release without either record being rewritten.

**How:** join version → source run → data/configuration → actual job and inspect every supplied descriptor field against those records. Calculate the repeated validation-score delta independently. An equal score cannot compensate for different data or code. If verification refuses a mismatched field or stale job, preserve that failure and repair the actual declaration/evidence before export.

</details>

## Learning outcome

Scope the remaining handoff work, connect pipeline, tracking, registry and operational-response evidence, then replay the selected run from its recorded source, data, configuration and environment within the declared result tolerance.

## Summary

Your remaining work is scoped around a real release. Its model, run, data and serving record form one inspectable chain, and its recorded recipe has a replay result while the broader clean receiving proof remains to be established.
