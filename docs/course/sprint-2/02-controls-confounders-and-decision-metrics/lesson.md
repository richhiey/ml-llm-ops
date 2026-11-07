🏷
# Controls, confounders, and decision metrics

Threadline's catalog specialists need more reliable category suggestions, particularly for similar-looking tops. A colleague suggests training longer and adding shifted training images at the same time. If the result improves, the team would still not know which change helped. That makes its next engineering decision harder to justify.

A controlled comparison makes a limited claim: under the stated conditions, changing one factor produced a different observed result.

# Keep the question small enough to answer

A **control** is a condition held fixed so runs can be compared. A **factor** is the setting deliberately varied. A **confounder** is another change that offers a competing explanation for the result.

The **baseline** is the reference recipe and result. Each **candidate** changes one setting against that baseline. Group the fixed conditions by the question they protect.

| Question | Keep fixed | Why it matters |
|---|---|---|
| Did the models learn from the same examples? | Original images and recorded training/validation split | Different examples could explain the change in score |
| Did learning begin from the same point? | CNN structure and initial weight values | A different starting model introduces another difference |
| Was each candidate measured in the same way? | Validation images, pixel preparation, category order and metric | The score must answer the same question every time |
| Did the execution conditions change? | Python code, installed packages and CPU thread count | Another code or numerical change could affect the result |

A **seed** is a recorded number used to repeat random choices. Here, keeping seed `426` creates a new CNN with the same initial weight values for every run in the declared environment. Each CNN then learns from scratch using its own recipe. The eight-epoch candidate begins with those initial values, independently of the trained four-epoch model. The pipeline also records the starting weights so this condition can be checked.

# Understand what each training change might do

A **hypothesis** is a proposed explanation to test. These five settings offer different hypotheses about the catalog model's limitations. Their possible benefits are questions for the experiment.

| Setting | What changes | Why Threadline might try it | Possible drawback |
|---|---|---|---|
| Epochs | Number of passes through the training examples | Four passes may leave useful clothing patterns incompletely learned | More time, or fitting training examples too closely |
| Learning rate | Size of each update to the model's learned weights | Smaller updates may refine a useful pattern more carefully | Learning may progress too slowly within four epochs |
| Weight decay | A restraint that discourages large learned weights | It may reduce reliance on patterns specific to the training examples | Too much restraint can prevent useful learning |
| Dropout | Randomly switch off some hidden responses during training | It may help the classifier use several useful clues instead of depending heavily on one | Learning can become harder, especially in a small model |
| Translation augmentation | Create slightly shifted training images with the same labels | Product thumbnails may place the same clothing shape a little differently | Shifts may add difficulty without helping the unchanged validation images |

Dropout is switched off when evaluating or making predictions. Translation changes training examples only. This keeps measurement on the original validation images. The source shows where each setting affects the CNN's learning. [Training implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/training.py)

| Comparison | What you can conclude |
|---|---|
| Four versus eight epochs, everything else fixed | An observed effect of more training under this recipe |
| Lower learning rate plus more epochs | An effect of the combined recipe; the individual cause is unresolved |
| Same settings, new validation images | Performance on different evaluation data; not a direct improvement comparison |
| Same settings, automatic recording enabled | A repeat checking how measurements are recorded |

A combined recipe can be useful later. Label it honestly and give it its own question. Here, five separate one-factor candidates make the first study easier to interpret.

# Choose the decision metric before seeing results

**Recall** asks how many actual items of a category were found. **Precision** asks how many suggestions for that category were correct. In the author's baseline, the CNN finds `117` of `300` actual shirts, giving recall `0.39`. It suggests “Shirt” for `158` images, of which `117` are correct, giving precision about `0.741`. Finding more shirts and making fewer wrong shirt suggestions are related but different goals.

**F1** combines precision and recall, becoming smaller when either is poor. **Macro F1** averages the ten category F1 scores equally. Values run from `0` to `1`, with larger values better. Threadline gives each category equal importance, so validation macro F1 is its **primary metric**, the measure declared in advance for choosing between comparable configurations. Compute it on the same `3000` validation images.

**Diagnostic metrics** help explain the choice. Accuracy reports the fraction of all images classified correctly. Category precision and recall expose mistakes hidden by an average. Training and validation loss measure disagreement with known labels on each group. Runtime records elapsed time on the measured machine. These measurements can support a recommendation without replacing the primary rule. The scikit-learn reference explains the different ways F1 can be averaged. [F1 score and averaging](https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.f1_score.html)

A candidate can improve macro F1 while making one category worse. Report that regression. Do not quietly replace the declared primary metric with whichever diagnostic favors a preferred candidate.

A client may also declare a minimum acceptable recall before comparing runs. **Eligibility** then means meeting that client's requirements. First exclude invalid comparisons, then apply the requirements, then choose the largest primary metric among the remaining configurations. A controlled run can fail a business requirement and still provide valid experimental evidence. Threadline's current study has no additional category threshold.

# Distinguish observation from a durable improvement claim

These CPU runs use one recorded seed to keep the first comparison manageable. The largest observed macro F1 selects a candidate for further validation. It does not prove that the recipe will always win across random seeds, other product images or live suppliers.

Keep full-precision values for ranking and round only for display. If values tie exactly, retain the earlier declared eligible run, with the baseline first. Preserve the official test split until configuration selection is recorded; repeatedly selecting against it would turn it into tuning data.

# Check for Understanding

Your experiment plan contains a longer-training candidate, a candidate changing both dropout and learning rate, and a candidate evaluated on a new group of supplier images. Classify each comparison and write the repair needed before it can support this study's model-selection decision. State the primary metric and one diagnostic you would inspect for the catalog team.

<details>
<summary>Solution</summary>

**Result you should get**

Only the longer-training row is directly comparable if all controls match. Split the two-factor change into separate candidates, or label it a combined-recipe study. Keep the new supplier-image result separate from the fixed-validation ranking. Use validation macro F1 for selection and, for example, shirt recall plus precision to explain category tradeoffs.

**How**

List every changed condition before looking at scores. A numerical gain cannot repair an invalid comparison. Keep observations from other image groups because they may matter operationally, while clearly stating the different question they answer.

</details>

## Learning outcome

Explain why a run comparison is invalid when dataset split, evaluation conditions, or multiple uncontrolled factors change, and distinguish a primary decision metric from diagnostic metrics.

## Summary

Threadline has a selection rule and a set of controls it can check before comparing scores. The planned matrix will turn those rules into five focused investigations.
