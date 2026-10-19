🏷️
# Controls, confounders, and decision metrics

Linden Facilities sees a smaller error after a teammate changed both regularization and evaluation rows. The team wants to attribute the improvement to the model change, but two explanations now fit the evidence.

## Your route through this lesson

Reason through confounded results and calculate what the decision metrics measure. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** A justified comparison boundary and metric rule that preserves the final holdout.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb#scrollTo=metric-reasoning). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Hold the question steady

A **control** is a condition held fixed across a comparison. A **factor** is the setting deliberately varied. A **confounder** is another changed condition that could explain the observed difference. To compare `alpha`, hold the data snapshot, split, features, scaling, solver, guard and evaluation metric fixed.

| Run change | What you can conclude |
|---|---|
| Alpha only; identical validation rows | Difference under those controlled conditions |
| Alpha and split changed | Cannot isolate alpha's effect |
| Same alpha, final instead of validation rows | Different evaluation, not a new alpha comparison |
| Added input guard; valid rows unchanged | Validate operational contract separately from model improvement |

## Ask what caused the difference

Suppose configuration A uses `alpha=1` on the fixed validation rows, while B uses `alpha=10` on a different set of rows. B's error is lower. Two things changed: the model's penalty and the difficulty of the evaluation examples. The result does not isolate the effect of alpha. The problem is an ambiguous explanation, even if both executions are technically valid.

A controlled comparison fixes the evaluation question and varies the intended factor. It does not prove that the result generalizes to every dataset. It gives a narrower conclusion: under these recorded conditions, this change produced this observed difference. That narrower conclusion is useful because another engineer can inspect and repeat it.

## Primary and diagnostic metrics have different jobs

A **primary decision metric** is the measure chosen in advance to rank candidates. Here it is validation RMSE, in kWh, lower is better. Squaring errors before averaging makes larger errors count more. A **diagnostic metric** helps explain behavior without silently replacing the selection rule; here MAE measures average absolute error.

A teammate cannot choose RMSE when it favors one run and switch to training score when it favors another. Training metrics describe fit to known rows; they do not measure the same held-out question. The inference brief also has a completion budget: good RMSE and acceptable batch completion are separate requirements.

## Connect an error measure to a decision

For a prediction, the error is the predicted demand minus the observed demand. **MAE** averages the absolute errors: signs cannot cancel, and each extra kWh contributes equally. **RMSE** squares each error, averages the squares, then takes the square root. Squaring gives a large miss more influence; the square root brings the final result back to kWh.

For the illustrative error lists `A=[2,2,8]` and `B=[4,4,4]`, both MAEs are `(2+2+8)/3 = 4` kWh. A's RMSE is `sqrt((4+4+64)/3) = sqrt(24)`, about `4.899` kWh. B's RMSE is `4` kWh. The distinction matters when the brief wants larger misses to count more heavily. It does not make RMSE the right metric for every business problem.

Linden declares validation RMSE as the primary model-selection metric. MAE helps interpret the result, and batch completion checks whether the output is delivered in time. Those measures answer different questions; the report should preserve each instead of letting the most favorable number decide.

## Decide which comparisons belong together

| Pair of observations | Decision before ranking |
|---|---|
| Different alpha; same source, features, snapshot and validation partition | Include in the declared alpha comparison |
| Same alpha run twice | Useful repeat check; not two distinct configurations |
| Training RMSE versus validation RMSE | Keep separate: fitting rows and held-out rows answer different questions |
| Model change plus changed feature set | A different experiment; cannot attribute the difference to alpha alone |
| Final holdout after configuration selection | Report separately; do not feed it back into tuning |

The `partition` column makes roles explicit in this snapshot. The 168 training rows fit the scaler and estimator; 48 validation rows support selection; 24 final rows provide a later check once selection is finished. These counts describe the teaching snapshot, not a recommendation for real time-series validation.


The synthetic interleaved split is fixed to teach infrastructure; it is not a recommended temporal validation design for real forecasting.

## Interpret a tiny winning margin carefully

A deterministic ranking can distinguish two raw values that round to the same display value. That tells you which row wins the declared metric rule. It does not quantify uncertainty about unseen facility demand. Nor does the `1e-6` reproduction tolerance do that: it checks whether a repeated execution agrees with its original result.

Keep three statements separate in your explanation: which candidate ranks first, what operational checks it still needs, and what the synthetic evaluation cannot establish. This prevents a correctly sorted table from becoming an unsupported deployment recommendation.

## Check for Understanding

A run on `final` scores better than all five validation runs. Linden's assistant recommends it as the winner. Identify the invalid comparison and specify the evidence needed to rank the five configurations.

▶️ **Solution** *(toggle)*

> **Result you should get:** exclude the final-partition score from the validation ranking. Require the same snapshot, partition, source, features, solver and guard, then sort validation RMSE ascending.
>
> **How:** inspect `evaluation_partition`, `data_sha256` and the declared matrix, not just the score column. Keep the final result as a separate post-selection report.

![Controls, confounders, and decision metrics: evidence path](assets/controls-confounders-and-decision-metrics__01__en.png)

## Learning outcome

Explain why a run comparison is invalid when dataset split, evaluation conditions, or multiple uncontrolled factors change, and distinguish a primary decision metric from diagnostic metrics.

## Summary

You can separate an alpha comparison from a changed evaluation question. The declared primary metric and fixed controls now determine how the result table should be read.
