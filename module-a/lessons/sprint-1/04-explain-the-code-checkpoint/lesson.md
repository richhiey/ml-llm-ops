✂️
# Explain-the-code checkpoint

Linden Facilities has received an assistant's proposed input check. It appears to fix invalid hours, but the planner cannot accept hidden edits to planned inputs.

**Continue here:** [Sprint 1 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=stage-work). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Starting point

Use the [candidate code](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/generated-stage-candidate.py) and the [snapshot card](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/data/README.md). The candidate is deliberately unsafe exercise material. It is not part of the installed helper. A **mutation** changes an existing object; an input contract must say whether that is allowed.

| Statement under review | Evidence to retain |
|---|---|
| Caller-owned frame | Values before and after the proposed call |
| Returned object | Whether it is the same object or an independent copy |
| Guard behavior | Accepted, rejected and silently changed examples |

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

## Learning outcome

Given an AI-generated addition to the pipeline, explain line by line what it does, test its input/output contract, and identify any part that needs correction before merging.

## Summary

You can distinguish code that rejects a contract violation from code that hides one. Your explained diff and failing-before/passing-after evidence are the basis for accepting the generated change.
