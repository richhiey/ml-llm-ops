✂️
# Integrating pipeline, tracking, and registry

Linden Facilities can demonstrate each component, but a handoff needs a connected execution. Your task is to integrate existing behavior and prove that the same run reaches registration and inference.


## Work in the repository

Inspect `src/linden_mlops/cli.py` and `lifecycle.py`. Connect your existing selected run, registered version and batch IDs first. The selected recipe is in `work/selected-config.json`; use it for any genuinely missing execution. The existing `handoff` entry point shows the API sequence, so a second implementation is optional.

For a negative check, use a separate local candidate run with `range_guard=False`, register it, attempt approval, and verify the prior active version stayed unchanged. Keep its ID and rejection; do not activate it. Complete only missing links, then add their actual identities to your existing handoff note. The fresh receiving run later supplies the complete new execution; there is no need for an extra full reference pipeline now.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Starting point

Use your chosen validation configuration, validated extension and the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md). An **end-to-end run** connects the stages so its output artifact can be traced through the lifecycle.

| Boundary | Identity to carry |
|---|---|
| Training to registration | Actual run ID and model URI |
| Registration to selection | Returned version and validation tags |
| Selection to inference | Resolved version and matching source run |

## Your task

Trace the provided entry point, or adapt it only where your scope shows a missing connection. It trains, evaluates, logs parameters/metrics/artifacts, registers the resulting model, records validation evidence, assigns `active` and exercises the batch path. You may call the existing public helper API; keep reusable behavior in the helper rather than duplicate it in a notebook.

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

All links resolve to actual records in the new store. A rejected candidate remains inspectable and does not become active. The success path uses the selected configuration, not whichever baseline happened to be easiest to run.

## Learning outcome

Integrate the existing pipeline stages, MLflow tracking, registry aliases/tags, and inference-mode decision into one end-to-end run that trains, evaluates, logs, and registers a model version.

## Summary

The project now links one execution through tracking, registration, validated selection and inference. A failed gate has an observable stopping point instead of an unexplained partial handoff.
