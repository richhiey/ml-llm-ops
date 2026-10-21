✂️
# Proving the selected serving path uses the active version

Linden Facilities is ready to hand a batch CSV to the planner. Good model metrics do not prove which artifact served those rows or whether the complete file arrived in time.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb) in your local project environment. Find the section for **Proving the selected serving path uses the active version** using its Campus activity ID **A-S4-03**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Use `uv run linden-mlops batch --output-name serving-check` once, or inspect a retained batch if it already proves the same unchanged selection and input. Compare `work/tracking/serving-check.csv` and `.json` with the source input and saved registry identity. Create an invalid input copy under `work/`, then run `batch --input work/invalid-batch.csv --output-name rejected-input`. Expect rejection and no successful output; retain the valid file separately. Use the API lookup for input-copy and lineage checks.


## Starting point

Use your active registered model and `batch-v1.csv`. A **resolved version** is the fixed version returned by the alias lookup at the start of this job. It may differ from the current alias if someone changes the alias after the job starts.

| Acceptance dimension | Observable field |
|---|---|
| Correct rows | Input/output row_id lists and finite predictions |
| Correct model | Resolved version and source run |
| Timely completion | elapsed_seconds and complete_within_60s |

## Your task

Exercise the selected batch path with the representative `24` rows. Capture the input hash, output CSV, resolved version/source run, row count, finite predictions, elapsed seconds and throughput. Check complete output within `60` seconds as required by the [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md).

Compare output `row_id` values and ordering with the input. Confirm the registered version maps to the intended source run. Then use a copy containing an invalid hour to prove the validated input boundary rejects it. Preserve the valid output separately; a failed job is not evidence of complete serving.

Write a short evidence statement explaining what the observed timing establishes on this machine. Do not infer HTTP latency or universal cost savings from a batch timing record. Also diagnose this proposed shortcut without rerunning: an engineer checks only `rows=24` and the current alias, then calls an old CSV proof of the latest deployment. Name the evidence needed to accept or reject that claim.

## Working with documentation

Inspect `batch_predict` in `src/linden_mlops/lifecycle.py` and the [contract](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md). It resolves once, pins the model version, predicts and writes completion evidence.

## Hints

1. A row count alone cannot detect reordered or mismatched identifiers.
2. Use the version recorded for the job; a later alias lookup describes a later moment.
3. Keep measurements and predictions together so a fast failed request cannot look like success.

## Checkpoints

Your evidence names the actual version and raw output file. All `24` input identifiers have one finite prediction each. The completion deadline passes, or you diagnose the bottleneck and rerun. The invalid-input test rejects before producing a successful batch result.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** the `24` input identifiers occur once each in the original order with finite `prediction_kwh`; job metadata identifies the intended resolved version/source run, input hash and whole-batch completion no greater than `60` seconds. Your invalid-hour copy fails before a new successful output is written. An old CSV plus today's alias lookup cannot prove which version generated that file.

**How to check:** compare input/output identifier lists and finiteness, then connect the job's recorded version to its registry source run. Use job metadata from the same invocation as the CSV; an alias can change afterwards. Use a fresh invalid-output name so a stale success file cannot be mistaken for a failed job's result. If row identity, lineage or timing is missing, repair that specific check; one fast successful call alone does not establish every acceptance dimension.

</details>

## Learning outcome

Exercise the selected batch or real-time inference path with a representative input, verify that it resolves to the intended active model version, and capture the output plus the latency, throughput, or completion evidence named in the inference decision brief.

## Summary

Your batch proof identifies the model used, checks row alignment and records whole-job completion. The invalid-input test shows where the serving contract stops bad data.
