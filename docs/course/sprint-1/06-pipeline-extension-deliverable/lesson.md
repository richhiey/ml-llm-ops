✂️
# Pipeline extension deliverable

Harbor Facilities sends a new supplier intake file with boundary values and several different contract violations. Your cumulative project must distinguish usable rows from invalid inputs, explain the responsible rules and preserve valid predictions.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) in your local project environment. Find the section for **Pipeline extension deliverable** using its Campus activity ID **A-S1-06**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Read `docs/course/exercises/harbor-intake.csv` with pandas in a local script. Import `validate_ranges` from `linden_mlops.pipeline`. Use the existing source and your earlier checks to investigate the new intake; do not train another model or rebuild the project. Run probes with `uv run python your_script.py` and keep the raw intake unchanged.


## What you will work with

Open the [Harbor supplier intake](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/harbor-intake.csv), also available at `docs/course/exercises/harbor-intake.csv` in the repository. Inspect it before applying the guard.

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md). The supplier file has exactly `row_id`, `temperature_c`, `hour` and `occupancy`; it has no historical target or partition. Keep its values and identifiers unchanged. Apply the feature guard directly rather than passing it to historical `ingest()` or training on it. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

| Intake field | Contract to apply |
|---|---|
| `temperature_c` | Inclusive `-30..50` |
| `hour` | Integer in `0..23` |
| `occupancy` | Inclusive `0..100` |

## As you work, keep these questions in mind

Which supplier rows should be rejected before training or inference? Can you explain the exact line responsible? Why does the original planning deadline favor your chosen inference pattern?

## Quick diagnosis

Before executing the supplier file, record a row-by-row prediction: accept/reject, responsible condition and expected effect on the whole mixed intake. Harbor asks, “Can we clip the invalid values and still describe this as the supplied input?” Give an acceptance decision you can test.

## Making improvements

### Task A — Validate an extension

Reuse your actual edited project, source diff and observed boundary/integration checks. Before running the guard on the new supplier input, classify each row as acceptable or rejected and name the rule. Test individual rows and the whole mixed intake with the saved `validate_ranges` function, preserving the raw data. A rejected intake must not be silently clipped or have bad rows dropped. Do not change the source snapshot or split.

### Task B — Explain the code

Reuse your explanation of each changed line, including reads, conditions, exception behavior, copies and returns. Include the existing diff and failing-before/passing-after record, plus your candidate review. You do not need a second code rewrite or a second explanation of the same lines.

### Task C — Choose inference

Recommend batch or real-time from the supplied 24-row/60-second brief. Address latency, throughput and resource cost, and name the observable completion evidence.

## Final check

Check your existing working notes and keep the same local project/output folder. Point to your existing contract-test result and edited batch CSV/metadata; do not rerun them merely to generate new IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before relying on them. No new notebook, separate evidence report, registry setup, endpoint build or fresh-environment recovery is required for this checkpoint.

## Check your decision after the attempt

<details>
<summary>Solution — supplier intake and acceptance evidence</summary>

**Result you should get:** `H-201` and `H-203` pass. `H-202` fails because `22.5` is not an integer hour; `H-204` fails because `51` exceeds the temperature maximum; `H-205` fails because `-0.5` is negative occupancy. The complete five-row intake raises an error rather than returning three filtered rows. `H-201` and `H-203` retain their original values and index when checked individually. Clipping would change the supplied values and conceal a contract failure.

**How:** compare each prediction with an individual guard probe, then probe the complete intake. This compact check captures the verdicts without altering the file:

```python
import pandas as pd
from linden_mlops.pipeline import validate_ranges

intake = pd.read_csv("docs/course/exercises/harbor-intake.csv")
for index in intake.index:
    row = intake.loc[[index]]
    try:
        checked = validate_ranges(row)
        pd.testing.assert_frame_equal(checked, row)
        print(row.iloc[0]["row_id"], "accepted; values/index preserved")
    except ValueError as error:
        print(row.iloc[0]["row_id"], "rejected", str(error))
try:
    validate_ranges(intake)
except ValueError as error:
    print("mixed intake rejected", str(error))
else:
    raise AssertionError("Mixed invalid intake must reject")
```

If a verdict differs, inspect the actual changed guard before editing it. Acceptance of `H-202` suggests the integer condition is missing; rejection of `H-201` or `H-203` suggests an inclusive boundary became exclusive. Correct the responsible condition, rerun the focused failed probe and relevant contract tests, and retain the original failure alongside the repair.

For the inference decision, a passing answer connects all `24` inputs arriving together and the `60`-second completion deadline to batch processing. The existing batch CSV/metadata demonstrates completion and preserved row identity. Resource cost remains a qualitative tradeoff unless measured price or consumption evidence exists; validation error says nothing about serving price.

</details>

## Learning outcome

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## Summary

Harbor’s supplier change has been tested through an explained pipeline extension. The deliverable connects the code decision to observed contract and inference evidence.
