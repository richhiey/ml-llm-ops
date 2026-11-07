✂️
# Pipeline extension deliverable

Morrow Market is a new catalog partner evaluating Threadline's thumbnail-classification pipeline. Its intake resembles the supplier workflow you have practiced, but its acceptance policy and files need an independent check. The partner wants a complete set of category suggestions before its morning catalog review.

Use your existing saved CNN and the same local helper repository. Your task is to demonstrate an explained, tested pipeline extension and recommend a delivery pattern for this partner.

# What you will work with

Create the constructed acceptance intake from the repository root.

```bash
uv run --frozen python docs/course/exercises/prepare_intake.py --output work/morrow-intake
```

The script exports `24` identified records to `work/morrow-intake/intake.csv`. Product examples come from the independent research-image pool. Additional format/quality conditions are deliberately constructed for this exercise. Creating the intake does not verify or repair it.

| Partner requirement | Acceptance condition |
|---|---|
| Image format | Prepared `28×28` grayscale thumbnails using raw uint8 pixels |
| Minimum intensity range | At least `24` on the raw `0–255` scale |
| Input identity | Every original record retained in your intake decision |
| Accepted delivery | One prediction per accepted identifier, in accepted-manifest order |
| Rejected delivery | Separate record of rejected identifiers and observed reasons |
| Prediction source | The existing saved CNN, with actual loaded model identity |

The partner receives a completed manifest each evening. Its review starts the next morning, and it does not need to keep a user waiting for each individual result. Your delivery recommendation must address that primary workflow. [Application contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md)

# Your task

## Inspect and decide

Inspect the input metadata and image values. Produce an intake decision record identifying which inputs meet the partner's contract and which require correction. Preserve the original manifest and files. Do not silently resize, recolor or rescale rejected inputs into apparently valid thumbnails.

Before changing code, identify a boundary case that distinguishes this partner's policy from the previously demonstrated supplier rule. State the expected behavior on both sides of the new boundary.

## Extend and explain

Implement or adapt one bounded validation stage in the ordinary application source and connect it to shared inference preparation. Keep the demonstrated function's default supplier policy available, and select this partner's threshold explicitly at the preparation boundary. Retain the source diff and record the active policy. Explain each changed line, the input/output contract and why the insertion point is appropriate.

Create executable checks for an accepted boundary, a rejected boundary, source preservation and integration. Show evidence of a failed check or rejected route before the relevant correction, then retain the passing evidence. A direct helper-function call alone does not establish that the batch or request route uses your stage.

## Deliver and verify

Create an accepted manifest from your intake decisions. Run the real batch route using your saved CNN and a new output directory. Reconcile output counts, identifiers and order against that manifest. Verify the checkpoint identity and explain why retraining was unnecessary for this intake change.

Exercise a rejected case through an actual consumer. Verify the documented failure behavior and the absence of an apparently complete batch result. Also demonstrate that the valid route continues to work. Use the same learned weights when comparing behavior.

Recommend batch or real-time delivery for the partner. Explain latency, throughput and cost drivers using the brief and your measurements, with the timer boundaries stated.

# Final check

Your retained evidence should let another engineer inspect the original intake, your accepted/rejected decision, the implemented source change, active partner policy, line-by-line explanation, discriminating tests, actual delivery and inference recommendation. Label which supplier policy each boundary test exercises, and update the active integration-test expectation to match the partner brief. Keep your first attempt and any repair rather than replacing its evidence with a summary claim.

<details>
<summary>Reference feedback</summary>

**Result you should get**

The constructed intake has `20` acceptable product thumbnails and `4` records requiring correction under the partner's policy. Your checks must distinguish raw range `23` from `24`. Using a threshold of `20` unchanged would accept a supplied thumbnail that fails this partner's requirement. The completed delivery has exactly the accepted identifiers in their declared order and records the saved model used.

**How**

Inspect mode, dimensions, dtype and raw maximum-minus-minimum values. Keep structural failures separate from quality-policy failures. Match every decision to its original identifier. Verify that the validation stage is called by shared inference, then run the accepted subset through the normal consumer. An evening manifest supports a batch recommendation, while another client's interactive review can justify a request service. Explain the measured work rather than inferring hosting costs from one local call.

</details>

## Learning outcome

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## Summary

Morrow's handoff contains a validated intake boundary, explained source, actual accepted predictions and a delivery recommendation tied to its review process. Keep the original CNN and evaluation as historical baseline evidence. Before controlled model comparisons, freeze the audited source and confirm the same baseline recipe under that source so later runs have a comparable starting point.
