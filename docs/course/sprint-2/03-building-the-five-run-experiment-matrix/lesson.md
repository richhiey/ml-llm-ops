✂️
# Building the five-run experiment matrix

Threadline wants to reduce the clothing-category corrections its catalog specialists make. It has budget for five small CPU training investigations. Your job is to decide which suspected limitation each change addresses before seeing candidate scores.

Use your completed local pipeline, its baseline configuration and the [training configuration](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py). This activity produces a plan and configuration files; MLflow execution follows in the guided work. Keep your saved baseline and intake changes.

# Your task

An **experiment matrix** is a table of planned comparisons. Create yours in `work/experiment-plan.md` alongside five candidate JSON configuration files. JSON stores each recipe as named settings and values. For each candidate, state the suspected limitation, one changed setting, the baseline and candidate values, an expected benefit and a diagnostic measurement that could reveal a drawback.

Use settings the existing pipeline supports. You can vary training passes, update size, weight decay, dropout or small image shifts. Weight decay restrains learned weights. Dropout temporarily switches off some hidden responses during training. Image shifts create positional variation while preserving the category label. Connect your chosen setting to a reason it might help this classifier, and consider what it might make worse. Validation images remain unchanged.

Your five candidates must be distinct from each other and from the baseline, the reference recipe. Keep the same image groups, evaluation procedure, CNN structure, code, package versions, seed and CPU threads. A fixed seed repeats the starting weight values within the declared environment, while each new model learns from scratch. Declare validation macro F1, the average of the ten category F1 scores, as the decision metric and explain its connection to the equal-category brief. Name the saved prediction and recipe files that will let you check the comparison.

Include a separate row for one deliberately non-comparable proposal and explain why it is excluded. It does not count toward the five candidates. Do not open the test split or invent results for your plan.

# Working with documentation

| Question | Inspect |
|---|---|
| Which settings and bounds exist? | [TrainingConfig](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py) |
| Where do update size, weight restraint and image shifts affect learning? | [Training implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/training.py) |
| Which hidden responses does dropout affect? | [CNN definition](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py) |

# Hints

<details><summary>Hint 1</summary>

Compare every candidate to the same baseline, rather than accumulating changes from one candidate to the next. Keep unsupported changes out of this first bounded study.

</details>

<details><summary>Hint 2</summary>

A useful hypothesis connects a setting to a visible weakness. More training might refine similar-category features; image shifts might reduce position sensitivity. Neither is guaranteed to improve this validation set.

</details>

# Checkpoints

Read the five files side by side with `configs/baseline.json`. Each should differ in exactly one supported training field. Check that no candidate silently changes seed, thread count or validation preparation. Confirm your hypotheses do not claim success before execution.

Keep your attempt before opening the reference matrix.

<details>
<summary>Reference feedback</summary>

**Result you should get**

One feasible five-candidate matrix is below. The repository contains these [reference configurations](https://github.com/richhiey/ml-llm-ops/tree/main/configs/experiments); compare them with your own files after making your plan.

| Candidate | Single change from baseline | Question |
|---|---|---|
| Longer training | Epochs `4 → 8` | Does more learning improve the fixed validation result? |
| Lower learning rate | `0.001 → 0.0003` | Do smaller updates help within four epochs? |
| Weight decay | `0 → 0.001` | Does restraining weights help on separate validation images? |
| Dropout | `0 → 0.2` | Does switching off some training responses help this small model? |
| Translation | Pixels `0 → 2` | Does learning from small shifts help unchanged validation images? |

**How**

Copy the baseline separately for each row, edit its named field and compare every other value. Record all controls and retain raw validation predictions as support for the metrics. A proposed “eight epochs plus dropout” row needs a combined-recipe label and cannot replace one of these one-factor candidates.

</details>

## Learning outcome

Define a five-run experiment matrix for the provided training and inference pipeline starter that holds the dataset split and evaluation conditions constant, names the factor varied in each comparison, selects a primary metric tied to the inference brief, and labels any run that is not directly comparable.

## Summary

Your matrix states what will change, why it might help and which evidence could contradict the hypothesis. The configurations are ready for tracked execution without changing the question after seeing the scores.
