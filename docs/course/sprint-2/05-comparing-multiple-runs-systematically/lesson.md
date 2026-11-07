✂️
# Comparing multiple runs systematically

Threadline's six runs contain different gains and regressions. Your task is to select the best observed configuration by the declared rule and explain its tradeoffs to the catalog team.

Use your actual MLflow experiment, run ledger and fixed validation metric. Start the native MLflow UI using the README command if it is not running. Work from your own IDs and observations; the author reference is feedback, not a substitute for your comparison.

# Your task

Open **Experiments → threadline-cnn**. Select the baseline and five candidate rows, then choose **Compare**. Confirm the page says it is comparing six runs. Inspect parameter differences before ranking metrics: every candidate should change one declared factor against the same baseline.

Find `validation_macro_f1` in the comparison's Metrics section. Clicking that metric opens a comparison view with each run's recorded value. Use the final raw metric for the selection, rather than the highest intermediate-epoch observation or a rounded screenshot value.

Produce `work/selection.md` containing the six full IDs, eligibility checks, full-precision primary scores, selected configuration and baseline-to-candidate gain. Explain at least one category regression and the measured training-time tradeoff. Keep other cohorts or confounded recipes out of this ranking and explain any exclusion.

Retain a screenshot of your actual six-run comparison. Use the UI to make the decision first, then check it against the recorded predictions.

# Verify the comparison against raw evidence

The [comparison implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/comparison.py) reads native MLflow records, retrieves the recipe and recomputes scikit-learn metrics from each raw prediction CSV. It checks source/data/split/environment/initial weights and that the logged model belongs to the evaluated run. Inspect these operations before using the project verification file.

Replace the six capitalized ID tokens below with the full IDs from your ledger. These tokens identify your runs; they are not filenames or literal values to submit.

```bash
uv run --frozen python scripts/compare_runs.py --state work/mlflow --baseline BASELINE_ID --runs LONGER_ID LOWER_LR_ID WEIGHT_DECAY_ID DROPOUT_ID TRANSLATION_ID --output work/comparison.json
```

Expect five distinct eligible candidates and a selected run/model URI. Reconcile the output with your UI decision. If a control is mismatched, preserve the exclusion reason and repair the experiment before making a comparative claim. Do not overwrite an earlier comparison decision.

# Hints

<details><summary>Hint 1</summary>

The larger macro F1 wins among eligible configurations. A repeat ID does not add a configuration, and a larger accuracy cannot replace the primary metric.

</details>

<details><summary>Hint 2</summary>

Check the selected model's per-category recall alongside the baseline. A better average can conceal worse performance for a particular category. Runtime is an observation on a stated machine, not a production speed or cost guarantee.

</details>

# Checkpoints

Verify the same `3000` validation identities and class order, a shared source/environment, and one changed training field per candidate. Match the selected raw metric and model URI to the same run. Keep your written decision before opening the reference observations.

<details>
<summary>Reference feedback</summary>

**Result you should get**

The author's actual CPU study selected `longer-training` by validation macro F1. Different hardware may produce different observations; apply the declared rule to your own eligible results.

| Configuration | Macro F1 | Accuracy | Shirt recall |
|---|---:|---:|---:|
| Baseline | 0.8322 | 0.8380 | 0.3900 |
| Longer training | 0.8572 | 0.8570 | 0.7433 |
| Lower learning rate | 0.7955 | 0.8033 | 0.2967 |
| Weight decay | 0.8338 | 0.8400 | 0.3800 |
| Dropout | 0.8342 | 0.8383 | 0.4333 |
| Translation | 0.7841 | 0.7997 | 0.1767 |

**How**

The selected run `99ce416e13ee4eeba47f6adf05d4ed7c` improved raw macro F1 by `0.0250368652` over baseline `c538c971fdf44099b750af1d9513458b`. It also reduced T-shirt/top recall from `0.88` to `0.6467` and coat recall from `0.89` to `0.7133`. Training took about `14.21 s` versus `7.07 s` on the author's machine. Those tradeoffs belong in the handoff; they do not change the predeclared selection rule.

![Observed macro F1 across six configurations and category recall tradeoffs between baseline and eight epochs](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/sprint2-experiment-results__01__en.png)

The [actual reference evidence](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/evidence/sprint-2) includes full-precision scores, controls and raw validation predictions. Run IDs refer to the author store, not records preloaded into your local MLflow database. One-seed results identify a candidate for further validation, not a proven universal winner.

</details>

## Learning outcome

Use the MLflow UI to compare 5+ experiment runs against each other and identify the best-performing configuration for a given metric.

## Summary

Your selection is supported by a real six-run UI comparison and raw prediction evidence. The recommendation names both the observed improvement and the category/resource tradeoffs the next validation step must consider.
