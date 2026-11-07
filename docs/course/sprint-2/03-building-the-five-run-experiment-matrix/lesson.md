✂️
# Building the five-run experiment matrix

Threadline has budget for five small CPU investigations of its classifier. Your job is to decide what each investigation asks before the team sees any candidate results.

Use your completed local pipeline, its baseline configuration and the [training configuration](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py). This activity produces a plan and configuration files; MLflow execution follows in the guided work. Keep your saved baseline and intake changes.

# Your task

Create `work/experiment-plan.md` and five candidate JSON configurations. For each candidate, state the suspected limitation, one changed setting, the baseline and candidate values, an expected benefit and a diagnostic that could reveal a drawback.

Use settings the existing pipeline supports. Training duration, learning rate, weight decay, dropout and translation augmentation are available. **Weight decay** discourages large weights; **dropout** randomly suppresses hidden activations during training; **translation augmentation** shifts training images slightly to expose positional variation. Validation images remain unchanged.

Your five candidates must be distinct from each other and from the baseline. Hold the data/split, evaluation, architecture, code, environment, seed and CPU threads fixed. Declare validation macro F1 as the decision metric and explain its connection to the equal-category brief. Name which raw artifacts will let you check the comparison.

Include a separate row for one deliberately non-comparable proposal and explain why it is excluded. It does not count toward the five candidates. Do not open the test split or invent results for your plan.

# Working with documentation

| Question | Inspect |
|---|---|
| Which settings and bounds exist? | [TrainingConfig](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py) |
| Where is the learning-rate/weight-decay update applied? | [Training implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/training.py) |
| Where does dropout change behavior? | [CNN definition](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py) |

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
| Weight decay | `0 → 0.001` | Does constraining weights improve generalization? |
| Dropout | `0 → 0.2` | Does hidden-layer regularization help this small model? |
| Translation | Pixels `0 → 2` | Does learning from small shifts help unchanged validation images? |

**How**

Copy the baseline separately for each row, edit its named field and compare every other value. Record all controls and retain raw validation predictions as support for the metrics. A proposed “eight epochs plus dropout” row needs a combined-recipe label and cannot replace one of these one-factor candidates.

</details>

## Learning outcome

Define a five-run experiment matrix for the provided training and inference pipeline starter that holds the dataset split and evaluation conditions constant, names the factor varied in each comparison, selects a primary metric tied to the inference brief, and labels any run that is not directly comparable.

## Summary

Your matrix states what will change, why it might help and which evidence could contradict the hypothesis. The configurations are ready for tracked execution without changing the question after seeing the scores.
