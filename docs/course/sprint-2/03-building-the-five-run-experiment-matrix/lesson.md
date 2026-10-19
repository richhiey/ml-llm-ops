✂️
# Building the five-run experiment matrix

Linden Facilities wants five runs that answer one question: how does changing Ridge regularization affect validation error under a fixed setup? A **matrix** is a table declaring the configurations before execution.


## Work in the repository

Edit `configs/experiment.json` before executing anything. Declare your five positive distinct alphas, including the comparison anchor `1`, and retain the supplied metric/direction/partition fields. Keep your controls, spacing rationale and excluded example beside the config in a short local note or the optional matrix sheet. Register the plan with:

```sh
uv run linden-mlops plan --config configs/experiment.json
uv run linden-mlops status
```

Expect the five declared alphas and no new runs yet. [Experiment workflow](https://github.com/richhiey/ml-llm-ops/blob/main/docs/experiments.md) explains how the same plan is reused.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Starting point

Use the [contract and fixture](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), `Config`, and the fixed snapshot. `alpha` controls Ridge's regularization strength. The input guard rejects invalid measurements; it should be held constant across this model comparison.

| Matrix field | Decision to make |
|---|---|
| Factor / anchor | Name the changed setting and comparison reference |
| Controls | Pin data/split/features/solver/guard/evaluation |
| Metric / exclusion | Declare direction and label a changed evaluation question |

## Your task

Record your matrix in `configs/experiment.json`; optionally use the [blank matrix sheet](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/experiment-matrix-starter.csv) to create `experiment-matrix.csv` with five configuration labels, each alpha, the comparison anchor, varied factor, controls, primary metric and comparability status. Choose five positive alpha values spanning weak through stronger regularization, with `1` as your anchor. Justify the spacing and predict which comparisons might reveal underfitting. If you need a bounded reference range, use `0.01`, `0.1`, `1`, `10`, and `100`; the supplied config starts with those values. Your independently chosen matrix need not reproduce its winning alpha. State what is held fixed: snapshot/hash, feature order, split, scaler fitting, solver, guard and evaluation partition.

Choose the metric using the planning brief rather than whichever score later looks attractive. Add a clearly marked **excluded comparison example** that changes the evaluation partition; do not count it as one of the five controlled configurations. Explain what question that extra run could answer instead.

Prepare the five configurations without yet interpreting a result table. Keep the final holdout out of model selection.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need alpha's meaning | [Ridge API](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.Ridge.html) |
| You need the fixed controls | [Helper contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) |

## Hints

1. Write the comparison question before listing values.
2. Each comparison needs an anchor and one named changed factor.
3. A shared run name does not prove a shared data hash or partition.

## Checkpoints

A peer should be able to reconstruct all five `Config` values from your table without asking what you meant. Before running, point to the field that prevents an evaluation on `final` from entering the ranking. Save the table for the tracked experiment evidence.

## Learning outcome

Define a five-run experiment matrix for the provided training and inference pipeline starter that holds the dataset split and evaluation conditions constant, names the factor varied in each comparison, selects a primary metric tied to the inference brief, and labels any run that is not directly comparable.

## Summary

Your matrix gives each run a purpose before any score is seen. It also makes incompatible evaluations visible before they can influence selection.
