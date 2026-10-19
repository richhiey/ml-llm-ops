✂️
# Integrating pipeline, tracking, and registry

Linden Facilities can demonstrate each component, but a handoff needs a connected execution. Your task is to integrate existing behavior and prove that the same run reaches registration and inference.

## Your route through this lesson

Connect one chosen configuration through the lifecycle and make a failed gate observable. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Successful identity chain plus rejected-candidate evidence preserving active selection.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=handoff-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use your chosen validation configuration, validated extension and the [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md). An **end-to-end run** connects the stages so its output artifact can be traced through the lifecycle.

| Boundary | Identity to carry |
|---|---|
| Training to registration | Actual run ID and model URI |
| Registration to selection | Returned version and validation tags |
| Selection to inference | Resolved version and matching source run |

## Draw one chain before writing an entry point

Choose the actual validation configuration you intend to hand over. Write a chain showing what each operation returns and which next operation consumes it. The run returns a model URI and run ID; registration consumes the source run and returns a version; validation/activation act on that version; inference records the version and source run it resolved. These are the seams where separate working examples can accidentally become an unconnected project.

Do not discover a run by sorting every historical execution and taking the last row. Carry its returned identity. Do not hard-code version `1`. Use the value registration returns in this store. If your selected alpha differs from the reference fixture's winner, explain the controlled evidence that selected it and use it consistently.

## Make failure part of the design

Your entry point should stop activation when approval fails. Logging and registration may have succeeded, so retain those records as partial completion. A broad exception handler that prints “done” after an approval error can make a rejected candidate appear active in the report.

Write a predicted failure path before running it. Start with a suitable approved active version, introduce a candidate that fails the numeric gate, and identify which record should still be current afterward. A negative case in an empty store cannot establish that an existing active selection survived, so plan the starting state deliberately.

## Use an integration ledger

| Operation | Identity or evidence to retain | Question for the next boundary |
|---|---|---|
| Train/evaluate/log | Actual run ID, config, metrics, model URI | Is this the chosen configuration? |
| Register | Returned version and source run | Does it reference that execution? |
| Validate | Tags and real test/metric rationale | Is activation allowed? |
| Select | Alias event and current lookup | Which version will a new job resolve? |
| Infer | CSV plus resolved version/source run | Is it the selected artifact with aligned output? |

Keep one ledger for the successful path and a short failure record for the rejected candidate. The important result is the connected chain, not the number of commands that exit successfully.

## Validate from the same project code you will submit

Use the editable project's CLI or a script importing its public API. A notebook may orchestrate the investigation, but reusable pipeline/lifecycle logic should remain in the project package. In Colab use a new subprocess for changed source; a reference module already in memory is not evidence that your edit executed.

After success, inspect the registered version's source run and compare it to both the training record and inference evidence. After failure, inspect `active` again. Retain the output and explain the stopping point. If any identity differs, trace backward to the first boundary where an assumed value replaced a returned one.

## Your task

Build an entry point in your project copy that trains, evaluates, logs parameters/metrics/artifacts, registers the resulting model, records validation evidence, assigns `active` and exercises the batch path. You may call the existing public helper API; keep reusable behavior in the helper rather than duplicate it in a notebook.

Use a new state directory. Capture a single evidence index naming the training run ID, model URI, registered version, validation tags, alias event and batch-resolved version/source run. Include your extension and chosen alpha. Keep pending registration separate from validated activation; a failed gate must stop selection.

Explain which function owns each stage and what happens if validation fails. Demonstrate a negative case without activating a rejected model, then run the successful path. Preserve evidence of both outcomes.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need the public sequence | [API lookup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/api-reference.md) |
| You need exact setup/flags | [Helper README](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/README.md) |

## Hints

1. Carry the returned run ID into registration; do not select a run by display name.
2. Carry the returned version into approval and activation; do not assume the counter.
3. Compare the batch source run with the registered version's source run.

## Checkpoints

All links resolve to actual records in the new store. A rejected candidate remains inspectable and does not become active. The success path uses the selected configuration, not whichever baseline happened to be easiest to run.

## Make partial completion visible

Write an evidence table with `operation`, `returned identity`, `next operation's input` and `observed result`. Test a candidate whose RMSE fails approval while a valid version is active. Prove the failed attempt leaves `active` unchanged. The success path must connect your selected training run to the registered artifact and batch source run; producing independent successful examples in different stores does not satisfy that link.

## Learning outcome

Integrate the existing pipeline stages, MLflow tracking, registry aliases/tags, and inference-mode decision into one end-to-end run that trains, evaluates, logs, and registers a model version.

## Summary

The project now links one execution through tracking, registration, validated selection and inference. A failed gate has an observable stopping point instead of an unexplained partial handoff.
