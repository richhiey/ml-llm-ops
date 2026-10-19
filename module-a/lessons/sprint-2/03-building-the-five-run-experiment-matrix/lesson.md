✂️
# Building the five-run experiment matrix

Linden Facilities wants five runs that answer one question: how does changing Ridge regularization affect validation error under a fixed setup? A **matrix** is a table declaring the configurations before execution.

## Your route through this lesson

Design the five configurations before execution and label an incompatible comparison. Start in your project or a fresh unsolved workspace. Read the mission, choose an investigation, and use hints only when needed. Keep predictions, source changes and observed results; the guided reference is support rather than your submission.

**Finish with:** A reconstructable five-row matrix, controls, metric, predictions and exclusion rationale.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=experiment-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Starting point

Use the [contract and fixture](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md), `Config`, and the fixed snapshot. `alpha` controls Ridge's regularization strength. The input guard rejects invalid measurements; it should be held constant across this model comparison.

| Matrix field | Decision to make |
|---|---|
| Factor / anchor | Name the changed setting and comparison reference |
| Controls | Pin data/split/features/solver/guard/evaluation |
| Metric / exclusion | Declare direction and label a changed evaluation question |

## Plan the comparison before you own any scores

This is a design task. You do not need to run five models to finish it. You need a plan precise enough that another person could execute the intended comparison without choosing missing settings for you. Start with one sentence: “With this snapshot and evaluation fixed, I want to test the effect of ___ on ___.”

Ridge's `alpha` is the penalty strength, not the learning rate. A larger penalty generally shrinks fitted coefficients more strongly; whether that helps held-out error is an empirical question. Choosing values spaced across a range can reveal more than five nearly identical settings, but the spacing should follow your stated question rather than an expectation that one particular value must win.

## Separate the configuration from the execution

A configuration declares settings. A run is an execution of those settings. Running the same configuration five times gives repeatability information, but it does not produce five distinct configurations. Give your planned rows stable labels such as `candidate-a`; leave run-ID fields empty until execution supplies actual IDs.

Use the anchor alpha `1` as a reference when describing each planned comparison. Record the factor that changes relative to that anchor and all settings that must stay fixed. At minimum, someone should be able to reconstruct each `Config(alpha=..., range_guard=True, autolog=...)` and know to evaluate `validation`.

## Make the matrix executable as a specification

| Field in your plan | A precise entry | An entry to repair |
|---|---|---|
| Evaluation | `validation` on the fixed snapshot | “test data” with no row identity |
| Primary metric | `rmse_kwh`, lower is better | “best score” |
| Guard | Enabled for all five | “same as before” |
| Source/data | Named revision/hash or a location to capture before execution | “latest” |
| Exclusion | Hypothetical changed partition, not in ranking | A sixth row silently sorted with the five |

The exclusion example is a planning counterexample; do not open the reserved final holdout to produce its number now. Explain why its changed evaluation would measure a different question. That explanation is useful even without running it.

## Review before executing anything

Ask whether your table would expose an accidental split change, duplicate alpha, missing guard or switch to a training metric. If a peer could only discover those mistakes by asking you what you meant, improve the table. Record one prediction that the results could overturn, such as stronger regularization worsening validation error beyond some point. Keep the prediction unchanged when you later inspect results.

Finish with the five-row plan, the excluded-comparison explanation and a rationale for the metric/spacing. Carry these into tracking; do not retrospectively choose controls that make a favorable score look intentional.

## Your task

Use the [blank matrix sheet](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/experiment-matrix-starter.csv) to create `experiment-matrix.csv` with five configuration labels, each alpha, the comparison anchor, varied factor, controls, primary metric and comparability status. Choose five positive alpha values spanning weak through stronger regularization, with `1` as your anchor. Justify the spacing and predict which comparisons might reveal underfitting. If you need a bounded reference range, use `0.01`, `0.1`, `1`, `10`, and `100`; the supplied CLI fixture uses exactly those values. Your independently chosen matrix need not reproduce its winning alpha. State what is held fixed: snapshot/hash, feature order, split, scaler fitting, solver, guard and evaluation partition.

Choose the metric using the planning brief rather than whichever score later looks attractive. Add a clearly marked **excluded comparison example** that changes the evaluation partition; do not count it as one of the five controlled configurations. Explain what question that extra run could answer instead.

Prepare the five configurations without yet interpreting a result table. Keep the final holdout out of model selection.

## Working with documentation

| Use it when… | Reference |
|---|---|
| You need alpha's meaning | [Ridge API](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.Ridge.html) |
| You need the fixed controls | [Helper contracts](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/contracts.md) |

## Hints

1. Write the comparison question before listing values.
2. Each comparison needs an anchor and one named changed factor.
3. A shared run name does not prove a shared data hash or partition.

## Checkpoints

A peer should be able to reconstruct all five `Config` values from your table without asking what you meant. Before running, point to the field that prevents an evaluation on `final` from entering the ranking. Save the table for the tracked experiment evidence.

## Make a testable pre-run prediction

For each comparison, write one prediction about the model's behavior and one observation that would challenge it. For example, increasing a penalty might reduce coefficient size but still worsen held-out error. Retain the prediction even when the result disagrees; do not rewrite the matrix after seeing scores. Label the changed-partition example with the different question it measures.

## Learning outcome

Define a five-run experiment matrix for the provided training and inference pipeline starter that holds the dataset split and evaluation conditions constant, names the factor varied in each comparison, selects a primary metric tied to the inference brief, and labels any run that is not directly comparable.

## Summary

Your matrix gives each run a purpose before any score is seen. It also makes incompatible evaluations visible before they can influence selection.
