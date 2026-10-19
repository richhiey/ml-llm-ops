✂️
# Proving the selected serving path uses the active version

Linden Facilities is ready to hand a batch CSV to the planner. Good model metrics do not prove which artifact served those rows or whether the complete file arrived in time.

**Continue here:** [Sprint 4 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/04-cumulative-handoff.ipynb#scrollTo=handoff-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use your active registered model and `batch-v1.csv`. A **resolved version** is the fixed version returned by the alias lookup at the start of this job. It may differ from the current alias if someone changes the alias after the job starts.

| Acceptance dimension | Observable field |
|---|---|
| Correct rows | Input/output row_id lists and finite predictions |
| Correct model | Resolved version and source run |
| Timely completion | elapsed_seconds and complete_within_60s |

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

## Learning outcome

Exercise the selected batch or real-time inference path with a representative input, verify that it resolves to the intended active model version, and capture the output plus the latency, throughput, or completion evidence named in the inference decision brief.

## Summary

Your batch proof identifies the model used, checks row alignment and records whole-job completion. The invalid-input test shows where the serving contract stops bad data.
