✂️
# Experiment tracking deliverable

Morrow Market asks for an independent review of the catalog classifier before a supplier trial. It gives categories equal importance, but its catalog team has two additional acceptance requirements: T-shirt/top recall must be at least `0.80`, and sneaker recall at least `0.90` on the fixed validation set.

The partner wants the strongest macro F1 among configurations meeting those requirements. This is a new decision brief applied to the tracked pipeline you have built. The thresholds are constructed assessment policy, not claimed research or production standards.

# What you will work with

Use your completed local pipeline, the fixed Fashion-MNIST splits, at least five distinct candidate configurations plus baseline, the autologging repeat, and the actual artifacts in your MLflow store. Keep the official test split closed. Do not change the evaluation data to make a candidate pass the new policy.

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

Audit the runs you have already created. Complete any missing configuration or logging evidence through the actual pipeline. Retain excluded/confounded rows with their reasons; duplicates and instrumentation repeats do not count as distinct candidates. Keep source fixed across any runs you add to this study.

Show a real MLflow UI comparison of at least five configurations. Retrieve raw parameters, metrics and predictions to verify the comparison. Explain the changed factor and hypothesis for each candidate.

## Apply the partner's acceptance conditions

Create `work/morrow-selection.md` listing each run's full ID, comparability, two policy checks and primary metric. Distinguish a controlled run that fails the partner's policy from a run that is not scientifically comparable. Apply the policy before choosing the highest macro F1. Explain any difference from the original Threadline recommendation.

The project's comparison file ranks controlled experimental results; it does not know Morrow's new business policy. Keep its original result intact and document the partner decision separately. Do not alter observed metrics or the primary metric to obtain a preferred winner.

## Verify autologging and assistant advice

Retain the autologging configuration and raw histories showing what was automatically captured. Explain which project evidence remains explicit and why.

Direct your approved assistant to recommend a configuration under Morrow's brief. Include actual run evidence and the two policy thresholds. Retain the exact request and response. Validate every recommendation against raw MLflow values and the declared selection rule. Flag any wrong ID, omitted policy failure, unsupported performance claim or invalid comparison, and preserve the correction alongside the original response.

# Final check

Your handoff should let a colleague retrieve each configuration, metric history, evaluated model and supporting prediction file. It must include the actual UI comparison, partner eligibility table, selection or no-eligible-result decision, autologging evidence, original assistant response and claim-by-claim validation.

No registry alias is changed in this assessment. The output is a justified candidate for lifecycle validation, with all unresolved tradeoffs visible.

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

Morrow receives a tracked, policy-aware recommendation supported by real runs, genuine autologging and checked assistant advice. The selected artifact and its evidence are ready for registry validation and connected reproducibility work.
