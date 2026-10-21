✂️
# Integrating pipeline, tracking, and registry

Linden Facilities can demonstrate each component, but a handoff needs a connected execution. Your task is to integrate existing behavior and prove that the same run reaches registration and inference.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Integrating pipeline, tracking, and registry** using its Campus activity ID **A-S4-02**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Prepare a draft evidence index from your existing cumulative project:

```sh
uv run python docs/course/exercises/prepare-evidence.py integration --destination work/integration-review
```

The exercise copies actual matrix IDs, active registry identity and retained batch metadata into review material, with one deliberately mismatched identity link. It does not change runtime state. Open `work/integration-review/handoff-index.json`. Locate and repair the inconsistent identity using the raw registry and the files named by `batch_evidence_path` and `batch_predictions_path`, then complete your own handoff index. Preserve the original raw evidence. The selected recipe is in `work/selected-config.json`; use it for any genuinely missing execution.

For a negative check, plan a separate local candidate run with `range_guard=False`. Before executing, predict which gate should fail, what should remain pending, and which existing identity must stay active. Choose and connect the public interfaces yourself, then retain the actual rejection and before/after evidence. Do not activate the rejected candidate. Complete only missing links, then add their actual identities to your existing handoff note. The fresh receiving run later supplies the complete new execution; there is no need for an extra full reference pipeline now.


## Starting point

Use your chosen validation configuration, validated extension and the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md). An **end-to-end run** connects the stages so its output artifact can be traced through the lifecycle.

| Boundary | Identity to carry |
|---|---|
| Training to registration | Actual run ID and model URI |
| Registration to selection | Returned version and validation tags |
| Selection to inference | Resolved version and matching source run |

## Your task

Begin with the deliberately inconsistent draft. Identify the exact link that conflicts with the raw registry and batch evidence. Write your diagnosis before editing it: name the two conflicting IDs, the authoritative records and why a similar score or shared display name cannot repair the chain. Correct the draft, then build a connected index for train → evaluate/log → register → validated active alias → batch. Use existing successful execution records where they meet the same contracts; implement or run only a genuinely missing connection. You may call the public helper API; keep reusable behavior in the helper rather than duplicate it in a notebook.

Reuse the existing cumulative store. Capture a single evidence index naming the training run ID, model URI, registered version, validation tags, alias event and batch-resolved version/source run. Include your extension and chosen alpha. Keep pending registration separate from validated activation; a failed gate must stop selection.

Explain which function owns each stage and what happens if validation fails. Demonstrate a negative case without activating a rejected model, then inspect the successful path already recorded. Preserve evidence of both outcomes.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need the public sequence | [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) |
| You need exact setup/flags | [Helper README](https://github.com/richhiey/ml-llm-ops/blob/main/README.md) |

## Hints

1. Carry the returned run ID into registration; do not select a run by display name.
2. Carry the returned version into approval and activation; do not assume the counter.
3. Compare the batch source run with the registered version's source run.

## Checkpoints

All corrected links resolve to actual records in the cumulative store. A rejected candidate remains inspectable and does not become active. The success path uses the selected configuration, not whichever baseline happened to be easiest to run.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** your corrected index connects the registered model's actual source run to its model URI, validation tags, alias event and batch-resolved version/source run. The deliberately substituted training ID may be a real matrix run, but it is not the run that produced that registered artifact. The negative candidate remains `pending`, approval raises an error for the missing range guard, and the previously active version stays selected.

**How to check:** obtain the registered version with `ws.client.get_model_version` and compare its `run_id` with the raw run, the job metadata and your draft. Follow identities rather than choosing whichever matrix row has a plausible score. For the negative case, use `Workspace.run`, `register` and `approve`; inspect the alias before and after the failed approval without invoking `activate`. A successful training call does not establish a passed release gate. If your records disagree, fix the index or missing boundary and retain the rejection evidence; rerunning a finished wrapper would hide the reasoning this task asks you to supply.

</details>

## Learning outcome

Integrate the existing pipeline stages, MLflow tracking, registry aliases/tags, and inference-mode decision into one end-to-end run that trains, evaluates, logs, and registers a model version.

## Summary

The project now links one execution through tracking, registration, validated selection and inference. A failed gate has an observable stopping point instead of an unexplained partial handoff.
