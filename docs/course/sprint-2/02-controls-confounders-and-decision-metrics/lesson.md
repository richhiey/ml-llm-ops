🏷
# Controls, confounders, and decision metrics

Threadline wants fewer category mistakes, particularly among similar-looking tops. A colleague suggests training longer and adding image shifts at the same time. If the result improves, the team would still not know which change was responsible.

A controlled comparison makes a limited claim: under the stated conditions, changing one factor produced a different observed result.

# Keep the question small enough to answer

A **control** is a condition held fixed so runs can be compared. A **factor** is the setting deliberately varied. A **confounder** is another change that offers a competing explanation for the result.

For this study, keep the original image files, training and validation indices, validation preparation, class order, CNN structure, code snapshot, environment, seed and CPU thread count fixed. The model starts from fresh weights each time. Candidate configuration changes must preserve the same initial weight values and evaluation route.

| Comparison | What you can conclude |
|---|---|
| Four versus eight epochs, everything else fixed | An observed effect of more training under this recipe |
| Lower learning rate plus more epochs | An effect of the combined recipe; the individual cause is unresolved |
| Same settings, new validation images | Performance on different evaluation data; not a direct improvement comparison |
| Same settings, autologging enabled | A repeat checking instrumentation; not a new model-improvement configuration |

A combined recipe can be useful later. Label it honestly and give it its own question. Here, five separate one-factor candidates make the first study easier to interpret.

# Choose the decision metric before seeing results

Threadline gives each of the ten catalog categories equal importance. **Validation macro F1** is the primary metric: average the F1 score of each category equally, then prefer the larger value among eligible configurations. Compute it on the same `3000` validation images.

**Diagnostic metrics** explain the result and its tradeoffs. Accuracy reports overall correctness. Shirt recall shows whether more actual shirts are found. Per-category precision reveals whether that comes with more incorrect shirt suggestions. Training and validation loss help inspect learning behavior. Runtime describes resource use on the measured machine.

A candidate can improve macro F1 while making one category worse. Report that regression. Do not quietly replace the declared primary metric with whichever diagnostic favors a preferred candidate.

A client may also declare a minimum acceptable recall for a category before comparing runs. Treat such a requirement as an eligibility check, then maximize the primary metric among candidates that pass. A controlled run that fails a business requirement remains valid experimental evidence. Keep that distinction separate from a confounded comparison. Threadline's current study has no additional category threshold; a new partner can supply a different brief.

# Distinguish observation from a durable improvement claim

These CPU runs use one recorded seed to keep the first comparison manageable. The largest observed macro F1 selects a candidate for further validation. It does not prove that the recipe will always win across random seeds, other product images or live suppliers.

Keep full-precision values for ranking and round only for display. If values tie exactly, retain the earlier declared eligible run, with the baseline first. Preserve the official test split until configuration selection is recorded; repeatedly selecting against it would turn it into tuning data.

# Check for Understanding

Your experiment plan contains a longer-training candidate, a candidate changing both dropout and learning rate, and a candidate evaluated on a new supplier cohort. Classify each comparison and write the repair needed before it can support this study's model-selection decision. State the primary metric and one diagnostic you would inspect for the catalog team.

<details>
<summary>Solution</summary>

**Result you should get**

Only the longer-training row is directly comparable if all controls match. Split the two-factor change into separate candidates, or label it a combined-recipe study. Keep the supplier-cohort result separate from the fixed-validation ranking. Use validation macro F1 for selection and, for example, shirt recall plus precision to explain category tradeoffs.

**How**

List every changed condition before looking at scores. A numerical gain cannot repair an invalid comparison. Keep observations from other cohorts because they may matter operationally, while clearly stating the different question they answer.

</details>

## Learning outcome

Explain why a run comparison is invalid when dataset split, evaluation conditions, or multiple uncontrolled factors change, and distinguish a primary decision metric from diagnostic metrics.

## Summary

Threadline has a selection rule and a set of controls it can check before comparing scores. The planned matrix will turn those rules into five focused investigations.
