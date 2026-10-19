✂️
# Explain-the-code checkpoint

Linden Facilities has received an assistant's proposed input check. It appears to fix invalid hours, but the planner cannot accept hidden edits to planned inputs.

## Your route through this lesson

Predict and probe a proposed function, then justify a correction. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** Statement-level explanation, mutation/rejection probes and corrected project logic.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=stage-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use the [candidate code](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/generated-stage-candidate.py) and the [snapshot card](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/data/README.md). The candidate is deliberately unsafe exercise material. It is not part of the installed helper. A **mutation** changes an existing object; an input contract must say whether that is allowed.

| Statement under review | Evidence to retain |
|---|---|
| Caller-owned frame | Values before and after the proposed call |
| Returned object | Whether it is the same object or an independent copy |
| Guard behavior | Accepted, rejected and silently changed examples |

## Prepare an investigation that can prove you wrong

Work in your editable project or the unsolved learner workspace. Load the candidate from the supplied file; do not install it as the reference helper's validation function. Before executing it, read the whole function and mark which statements inspect a value, change a value, call another function or return an object. An assignment through `.loc` can change the caller's DataFrame even when the function's name sounds like a harmless check.

Create small, separate input tables for each probe. Reusing one table after a mutating call can contaminate the next test. Keep an untouched deep copy and compare it afterward. Your task is to decide whether the candidate meets the contract, not to prove that any numeric output is acceptable.

## Build the explanation from observations

Use one row of this structure per statement:

| Statement | My prediction before execution | Observation | Consequence for merging |
|---|---|---|---|
| Select a column | Which values are read? | Actual field/value | Required or unrelated input? |
| Assign a value | Which object changes? | Original versus saved copy | Allowed by the contract? |
| Return | Same object or a new object? | Object identity and values | Can the caller trust unchanged input? |

Do not fill the observation column from the code alone. Run a distinguishing probe. A useful test should fail if your explanation is wrong. Testing `hour=12` alone cannot distinguish a correct range guard from a function that never checks hours. Testing a value above the maximum cannot establish that negative or fractional values are rejected.

## Organize the work into three passes

First, predict behavior for ordinary, boundary and invalid rows. Second, execute the candidate and record returned values, raised exceptions and mutations. Third, correct only the bounded validation logic in your project and rerun the same probes. Keep your initial predictions visible, even when they were wrong; explain what changed your interpretation.

Then reconnect the corrected function through the guarded preprocessing branch. Your integration evidence should show the guard is reached, accepted features retain order/index/values and ordinary validation metrics agree with the unchanged baseline. A corrected function that is never called is not an integrated extension.

## Know when to stop and diagnose

| Observation | Next investigation |
|---|---|
| No exception, but input values changed | Inspect writes to the caller's table |
| One invalid field rejected, another accepted | Check loop control and return placement |
| Valid rows change | Distinguish validation from silent transformation |
| Correct local function, unchanged project behavior | Check imported file, interpreter and guarded branch |

Keep the final decision concrete: accepted as written, accepted after a named correction, or not ready. Support it with the explained diff and the probes that distinguish the corrected behavior. In Colab, execute edited-project probes in a new process through `project_python`; the notebook's already imported reference module must not stand in for your changed file.

## Your task

Produce a line-by-line explanation of the candidate, then a corrected addition in your project copy. Identify each read, write, condition, return and side effect. State which invalid cases the candidate accepts and which valid rows it changes. Keep all original feature values, indexes, targets and partition labels intact for accepted data.

Create evidence for a valid row, both hour boundaries, a negative hour, `24`, a fractional hour, missing data and a non-finite value. Show a failing test against the candidate before showing the corrected behavior. Confirm ingestion, training, evaluation and batch inference still work. You may consult the range-validation reference, but explain the correction yourself.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need elementwise range behavior | [pandas Series.between](https://pandas.pydata.org/docs/reference/api/pandas.Series.between.html) |
| You need to distinguish a view from a copy | [pandas DataFrame.copy](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.copy.html) |
| You need the scaffold contract | [Contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md) |

## Hints

1. Compare a copy of the input before and after the candidate call. Which assignment changes an existing table?
2. A maximum check does not validate the minimum or integer requirement.
3. Explain what an exception should mean for the caller. Silent repair and explicit rejection have different contracts.

## Checkpoints

Before integration, demonstrate one failure that would be invisible if you tested only `hour=12`. After correction, compare valid features and metrics with the baseline. Finish with an explained diff and observed checks, not a claim that the assistant said it was safe.

## Explain a consequence before running

For each changed statement, fill `statement → value read or written → effect on caller → test that could refute my explanation`. Predict the result for `hour=24`, `hour=-1` and a valid row before executing the candidate. A correct explanation must account for the original table after the call, not just the returned object. Use your editable project from the stage exercise; do not remove the reference notebook's pin check to accommodate edits.

## Learning outcome

Given an AI-generated addition to the pipeline, explain line by line what it does, test its input/output contract, and identify any part that needs correction before merging.

## Summary

You can distinguish code that rejects a contract violation from code that hides one. Your explained diff and failing-before/passing-after evidence are the basis for accepting the generated change.
