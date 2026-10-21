🏷️
# Controls, confounders, and decision metrics

Linden Facilities sees a smaller error after a teammate changed both regularization and evaluation rows. The team wants to attribute the improvement to the model change, but two explanations now fit the evidence.


Read this explanation alongside the [repository setup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md). Use your existing project evidence for the checks; no new model execution is needed.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) in your local project environment. Find the section for **Controls, confounders, and decision metrics** using its Campus activity ID **A-S2-02**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Hold the question steady

A **control** is a condition held fixed across a comparison. A **factor** is the setting deliberately varied. A **confounder** is another changed condition that could explain the observed difference. To compare `alpha`, hold the data snapshot, split, features, scaling, solver, guard and evaluation metric fixed.

| Run change | What you can conclude |
|---|---|
| Alpha only; identical validation rows | Difference under those controlled conditions |
| Alpha and split changed | Cannot isolate alpha's effect |
| Same alpha, final instead of validation rows | Different evaluation, not a new alpha comparison |
| Added input guard; valid rows unchanged | Validate operational contract separately from model improvement |

## Primary and diagnostic metrics have different jobs

A **primary decision metric** is the measure chosen in advance to rank candidates. Here it is validation RMSE, in kWh, lower is better. Squaring errors before averaging makes larger errors count more. A **diagnostic metric** helps explain behavior without silently replacing the selection rule; here MAE measures average absolute error.

A teammate cannot choose RMSE when it favors one run and switch to training score when it favors another. Training metrics describe fit to known rows; they do not measure the same held-out question. The inference brief also has a completion budget: good RMSE and acceptable batch completion are separate requirements.

## Connect an error measure to a decision

For a prediction, the error is the predicted demand minus the observed demand. **MAE** averages the absolute errors: signs cannot cancel, and each extra kWh contributes equally. **RMSE** squares each error, averages the squares, then takes the square root. Squaring gives a large miss more influence; the square root brings the final result back to kWh.

For the illustrative error lists `A=[2,2,8]` and `B=[4,4,4]`, both MAEs are `(2+2+8)/3 = 4` kWh. A's RMSE is `sqrt((4+4+64)/3) = sqrt(24)`, about `4.899` kWh. B's RMSE is `4` kWh. The distinction matters when the brief wants larger misses to count more heavily. It does not make RMSE the right metric for every business problem.

Linden declares validation RMSE as the primary model-selection metric. MAE helps interpret the result, and batch completion checks whether the output is delivered in time. Those measures answer different questions; the report should preserve each instead of letting the most favorable number decide.

## Interpret a tiny winning margin carefully

A deterministic ranking can distinguish two raw values that round to the same display value. That tells you which row wins the declared metric rule. It does not quantify uncertainty about unseen facility demand. Nor does the `1e-6` reproduction tolerance do that: it checks whether a repeated execution agrees with its original result.

Keep three statements separate in your explanation: which candidate ranks first, what operational checks it still needs, and what the synthetic evaluation cannot establish. This prevents a correctly sorted table from becoming an unsupported deployment recommendation.

## Check for Understanding

These are explicitly illustrative comparison cards, not new executions on the reserved final rows. Candidate C has validation errors `[0, 0, 9]` kWh; D has `[3, 3, 3]` kWh under identical controls. Another card reports final-partition RMSE `2` kWh. Produce the MAE and RMSE for C and D, rank the comparable candidates under Linden's declared rule, and explain which card must stay out of that ranking.

<details>
<summary>Check the numbers after committing to a ranking</summary>

**Result you should get:** C and D both have MAE `3` kWh. C has RMSE `sqrt(27) ≈ 5.196` kWh; D has RMSE `3` kWh. D wins the comparable validation ranking. The final-partition card is excluded, even though its number is lower.

**How:**

```python
import numpy as np
for name, errors in {"C": [0, 0, 9], "D": [3, 3, 3]}.items():
    errors = np.asarray(errors, dtype=float)
    print(name, "MAE", np.abs(errors).mean(),
          "RMSE", np.sqrt(np.square(errors).mean()))
```

Equal average absolute error does not imply equal squared-error penalty. If you chose the final card, inspect evaluation basis before sorting: it answers a different question. These cards do not authorize opening the actual final holdout.

</details>

## Learning outcome

Explain why a run comparison is invalid when dataset split, evaluation conditions, or multiple uncontrolled factors change, and distinguish a primary decision metric from diagnostic metrics.

## Summary

You can separate an alpha comparison from a changed evaluation question. The declared primary metric and fixed controls now determine how the result table should be read.
