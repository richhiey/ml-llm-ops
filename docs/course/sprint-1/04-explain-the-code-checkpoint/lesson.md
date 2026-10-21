✂️
# Explain-the-code checkpoint

Linden Facilities has received an assistant's proposed input check. It appears to fix invalid hours, but the planner cannot accept hidden edits to planned inputs.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) in your local project environment. Find the section for **Explain-the-code checkpoint** using its Campus activity ID **A-S1-04**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Open `docs/course/exercises/generated-stage-candidate.py`. Load the candidate in your own local probe script using `runpy.run_path(path)['proposed_guard']`; import the correct guard with `from linden_mlops.pipeline import validate_ranges`. Use pandas tables and fresh `.copy(deep=True)` inputs to investigate the mission below. Run your script with `uv run python your_script.py`. Keep the unsafe candidate separate from `src/`.


## Starting point

Use the [candidate code](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/generated-stage-candidate.py) and the [snapshot card](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/data/README.md). The candidate is deliberately unsafe exercise material. It is not part of the installed helper. A **mutation** changes an existing object; an input contract must say whether that is allowed.

| Statement under review | Evidence to retain |
|---|---|
| Caller-owned frame | Values before and after the proposed call |
| Returned object | Whether it is the same object or an independent copy |
| Guard behavior | Accepted, rejected and silently changed examples |

## Your task

Read the candidate source in the exercise file and produce a line-by-line review. Your project already contains the validated expert addition: keep it. Identify the corrections this proposal needs before merging; do not overwrite your working guard with unsafe code or rebuild the project. Identify each read, write, condition, return and side effect. State which invalid cases the candidate accepts and whether valid values or caller-owned objects change. Keep all original feature values, indexes, targets and partition labels intact for accepted data.

Probe one valid input plus `hour=24`, a negative hour and a fractional hour, using a fresh copy for each case. Record expected versus observed behavior, including caller mutation and returned-object identity. Show at least one failed contract assertion against the candidate, then contrast the same input with the saved `validate_ranges` function. Reuse the broader boundary tests and passing batch from the walkthrough. Rerun them only if you change the actual project source. You may consult the range-validation reference, but explain the correction yourself.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need elementwise range behavior | [pandas Series.between](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html) |
| You need to distinguish a view from a copy | [pandas DataFrame.copy](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.copy.html) |
| You need the scaffold contract | [Contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) |

## Hints

1. Compare a copy of the input before and after the candidate call. Which assignment changes an existing table?
2. A maximum check does not validate the minimum or integer requirement.
3. Explain what an exception should mean for the caller. Silent repair and explicit rejection have different contracts.

## Checkpoints

Before accepting the proposal, demonstrate one failure that would be invisible if you tested only `hour=12`. Point to the existing guard line that addresses each required correction. Keep the observed candidate failure and correct-guard contrast beside your review; no second implementation or separate report is required.

## Check your work after attempting the task

<details>
<summary>Open the self-check after recording your own result</summary>

**Result you should get:** `hour=24` becomes `23` without an exception, while a negative or fractional hour is accepted unchanged. For accepted inputs the proposal returns the caller's very same frame; a valid hour alone therefore misses the copy-contract failure. The existing `validate_ranges` rejects all three invalid hours and returns a separate deep copy for a valid frame. No candidate code belongs in `src/`.

**How to check:** the empty check only covers zero rows. The assignment writes into `frame`, `clip(upper=23)` repairs upper violations, and `return frame` exposes the same object. Compare both values and `returned is input_frame`; one cannot replace the other. If your review says “all valid values are mutated”, narrow that claim: the assignment targets the caller's object, but values already in range can remain equal. If you missed a failure, add that fresh-input probe and correct the corresponding line explanation before proposing a merge.

</details>

## Learning outcome

Given an AI-generated addition to the pipeline, explain line by line what it does, test its input/output contract, and identify any part that needs correction before merging.

## Summary

You can distinguish code that rejects a contract violation from code that hides one. Your line-by-line review and contrasting probes establish what must change before the proposal is safe to merge.
