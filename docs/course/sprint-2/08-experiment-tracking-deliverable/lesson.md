✂️
# Experiment tracking deliverable

Morrow Market, another fictional clothing retailer, is considering the classifier for a supplier trial with its own catalog requirements. Its specialists want stronger category suggestions overall, while protecting two categories they have explicitly chosen for this trial. T-shirt/top recall must be at least `0.80`, and sneaker recall at least `0.90` on the fixed validation set.

Recall measures the fraction of actual members of a category found. With `300` validation examples per category, these requirements mean finding at least `240` actual T-shirts/tops and `270` sneakers. Morrow wants the largest macro F1, the equally weighted average of the ten category F1 scores, among configurations meeting both requirements. A higher average alone cannot settle this partner's choice. The thresholds are constructed assessment policy, not claimed research or production standards.

# What you will work with

Use your completed local pipeline and fixed Fashion-MNIST training/validation groups. Bring five distinct changed candidate recipes plus the reference baseline, the baseline repeat checking automatic logging, and the saved files in your MLflow store. Keep the official test split closed. Preserve the validation examples when applying the new policy.

| Requirement | Evidence to retain |
|---|---|
| Comparable study | Fixed data/split, evaluation, source, environment and initial weights |
| At least five distinct candidates | Actual configurations and completed full run IDs |
| Genuine autologging | Enabled configuration and all expected raw metric histories |
| Partner eligibility | Raw T-shirt/top and sneaker recall for every candidate |
| Selection | Highest raw macro F1 among eligible configurations, or an explicit no-eligible-result finding |
| Assistant use | Actual request/response and validation of every recommendation |

# Your task

## Review and complete the tracked study

Audit the training executions you have already recorded. Complete any missing configuration or logging evidence through the actual pipeline. Retain excluded comparisons and their reasons. Repeating an ID or recording the same recipe with automatic logging does not create a distinct improvement candidate. Keep the Python code fixed across any runs you add to this study, and keep the same seed and starting model weights.

Show a real MLflow UI comparison of at least five configurations. Retrieve raw parameters, metrics and predictions to verify the comparison. Explain the changed factor and hypothesis for each candidate.

## Apply the partner's acceptance conditions

Create `work/morrow-selection.md` listing each run's full ID, whether it shares the required comparison conditions, the two policy checks and the primary metric. **Eligibility** means meeting Morrow's requirements. A properly controlled run can fail this policy, while a run on different evaluation images fails the comparison conditions. Apply both kinds of checks before choosing the highest macro F1. Explain any difference from the original Threadline recommendation.

The project's comparison file ranks controlled experimental results; it does not know Morrow's new business policy. Keep its original result intact and document the partner decision separately. Do not alter observed metrics or the primary metric to obtain a preferred winner.

## Verify autologging and assistant advice

Retain the autologging configuration and raw histories showing what was automatically captured. Explain which project evidence remains explicit and why.

Direct your approved assistant to recommend a configuration under Morrow's brief. Include actual run evidence and the two policy thresholds. Retain the exact request and response. Validate every recommendation against raw MLflow values and the declared selection rule. Flag any wrong ID, omitted policy failure, unsupported performance claim or invalid comparison, and preserve the correction alongside the original response.

# Final check

Your handoff should let a colleague retrieve each configuration, metric history, evaluated model and supporting prediction file. It must include the actual UI comparison, partner eligibility table, selection or no-eligible-result decision, autologging evidence, original assistant response and claim-by-claim validation.

The output recommends a saved model for the engineers' next validation step. Explain the remaining category and runtime tradeoffs so Morrow can see what the recommendation establishes.

<details>
<summary>Reference feedback</summary>

**Result you should get**

Applied to the author's six controlled configurations, Morrow's policy selects `weight-decay`, run `cfc92f3749474862bcc32a9269b797d5`: macro F1 `0.8337648911681302`, T-shirt/top recall `0.90` and sneaker recall `0.92`. The original eight-epoch winner fails the new T-shirt/top requirement. Dropout fails the sneaker requirement. Use your own eligible values if your observations differ.

**How**

Preserve the original experimental ranking, add the two explicit policy checks, then maximize macro F1 among rows that are both comparable and policy-eligible. Baseline and translation also pass those two thresholds in the author study, but have lower macro F1 than weight decay. A one-seed outcome remains evidence for further validation, not permission to claim deployment readiness. Validate the assistant against the partner brief rather than accepting a repeated earlier recommendation.

</details>

## Learning outcome

Deliverable: at least 5 experiment configurations logged and compared in MLflow, an autologging setup, and an AI-assisted summary recommending which configuration to promote - with the summary validated against raw data.

## Summary

Morrow receives a recommendation supported by real runs, checked automatic logging and validated assistant advice. It meets the partner's stated conditions, or explains why no observed configuration does. The selected saved model remains connected to the recipe and measurements needed for its next review.
