✂️
# Proving the selected serving path uses the active version

Linden Facilities is ready to hand a batch CSV to the planner. Good model metrics do not prove which artifact served those rows or whether the complete file arrived in time.

## Your route through this lesson

Test row integrity, artifact identity, completion and invalid-input rejection separately. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** New CSV/timing/version records and a distinct failed probe without stale success files.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=handoff-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use your active registered model and `batch-v1.csv`. A **resolved version** is the fixed version returned by the alias lookup at the start of this job. It may differ from the current alias if someone changes the alias after the job starts.

| Acceptance dimension | Observable field |
|---|---|
| Correct rows | Input/output row_id lists and finite predictions |
| Correct model | Resolved version and source run |
| Timely completion | elapsed_seconds and complete_within_60s |

## State the intended model before measuring time

Record the current active version and its source run before starting the new job. This is the intended selection, not a prediction about every later alias lookup. `batch_predict` resolves the alias once at job start and loads that fixed version. Its returned `resolved_version` is the appropriate identity for the job, even if the alias changes afterward.

Use the representative planned input, not a training table with known targets. The input has 24 unique identifiers and three features; output should preserve those identifiers and add one finite prediction per row. A count of 24 alone cannot detect duplicated, reordered or mismatched records.

## Plan three checks that answer different questions

| Check | Passing evidence | A misleading substitute |
|---|---|---|
| Row integrity | Ordered input/output identifiers agree; predictions finite | Only printing the first five rows |
| Artifact identity | Job version maps to intended source run | A filename containing `final` |
| Delivery | Complete CSV plus whole-job elapsed time <=60s | Time to construct a model object or a fast exception |

Write your predicted checks before invoking the job. Keep the new output name distinct from an earlier successful file. Read both the CSV and its evidence record after completion. That guards against inspecting a stale file while assuming the most recent command produced it.

## Design the invalid-input probe as a separate job

Copy the input rather than modifying the bundled snapshot. Change one field to an invalid hour while preserving the identifiers and other values. Decide what should happen before running it: rejection at the validated feature boundary, with no new successful output under that probe's unique name.

A process raising an exception quickly has not met the serving deadline. Keep its failure separate from the valid job's successful timing. If a file already exists under the probe name, choose another new name or preserve the old file and explain its origin; do not let it masquerade as newly produced output.

## Interpret the measurement's scope

The helper's timer begins before alias lookup and ends after writing the CSV. It includes model loading and prediction. It does not measure network requests to an HTTP service because none is implemented. Record the observed seconds and throughput, but accept against the brief's whole-job deadline rather than matching an instructor's exact elapsed time.

If the deadline fails, inspect which work dominates and rerun after a documented correction. If the row or identity check fails, do not treat a fast completion as a partial pass for the planner. Finish with the valid output, timing/version evidence, invalid-probe result and a statement of what this machine's observation establishes.

## Your task

Exercise the selected batch path with the representative `24` rows. Capture the input hash, output CSV, resolved version/source run, row count, finite predictions, elapsed seconds and throughput. Check complete output within `60` seconds as required by the [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md).

Compare output `row_id` values and ordering with the input. Confirm the registered version maps to the intended source run. Then use a copy containing an invalid hour to prove the validated input boundary rejects it. Preserve the valid output separately; a failed job is not evidence of complete serving.

Write a short evidence statement explaining what the observed timing establishes on this machine. Do not infer HTTP latency or universal cost savings from a batch timing record.

## Working with documentation

Inspect `batch_predict` in `src/campus_mlops/lifecycle.py` and the [contract](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md). It resolves once, pins the model version, predicts and writes completion evidence.

## Hints

1. A row count alone cannot detect reordered or mismatched identifiers.
2. Use the version recorded for the job; a later alias lookup describes a later moment.
3. Keep measurements and predictions together so a fast failed request cannot look like success.

## Checkpoints

Your evidence names the actual version and raw output file. All `24` input identifiers have one finite prediction each. The completion deadline passes, or you diagnose the bottleneck and rerun. The invalid-input test rejects before producing a successful batch result.

## Specify the job boundary

State which operations your timer covers: alias resolution, model loading, prediction and output writing. Verify that exact boundary against the helper. Store valid and intentionally invalid requests under distinct output names; a previous successful CSV left on disk cannot prove that a later failed request completed. Compare identifier lists as well as row counts before accepting an output.

## Learning outcome

Exercise the selected batch or real-time inference path with a representative input, verify that it resolves to the intended active model version, and capture the output plus the latency, throughput, or completion evidence named in the inference decision brief.

## Summary

Your batch proof identifies the model used, checks row alignment and records whole-job completion. The invalid-input test shows where the serving contract stops bad data.
