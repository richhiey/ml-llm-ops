✂️
# Pipeline extension deliverable

Morrow Market is a fictional catalog partner trying Threadline's image-classification pipeline. Its staff need category suggestions ready before their morning product review. They have sent a new set of thumbnails and a rule specifying which images they will accept for prediction.

Use your existing saved CNN, whose learned weights turn prepared thumbnails into category scores, and the same local project. Your task is to check the incoming files, adapt the taught image-validation step and demonstrate a complete prediction delivery. Explain your code change and recommend how the partner should receive predictions.

# What you will work with

Create the constructed acceptance intake from the repository root.

```bash
python docs/course/exercises/prepare_intake.py --output work/morrow-intake
```

The script exports `24` identified records to `work/morrow-intake/intake.csv`. This **intake** is the group of files received for the job. Its CSV manifest pairs each image's identifier with a filename. Product examples come from the separate research-image pool. Additional format and quality conditions are deliberately constructed for this exercise. The resulting files are ready for you to inspect.

| Partner requirement | Acceptance condition |
|---|---|
| Image format | Prepared `28×28` grayscale thumbnails using raw uint8 pixels |
| Minimum brightness range | Brightest minus darkest raw pixel is at least `24` on the `0–255` scale |
| Input identity | Every original record retained in your intake decision |
| Accepted delivery | One prediction per accepted identifier, in accepted-manifest order |
| Rejected delivery | Separate record of rejected identifiers and observed reasons |
| Prediction source | The existing saved CNN, with actual loaded model identity |

The partner receives a completed manifest each evening. Its review starts the next morning, and it does not need to keep a user waiting for each individual result. Your delivery recommendation must address that primary workflow. [Application contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md)

# Your task

## Inspect and decide

Inspect each file's metadata, including its image mode and dimensions, and the actual pixel values. Use the same Pillow and NumPy inspection you have practiced. Produce an intake decision record identifying which inputs meet the partner's contract and which require correction. Preserve the original manifest and files. Do not silently resize, recolor or rescale rejected inputs into apparently valid thumbnails.

Before changing code, identify a boundary case that distinguishes this partner's policy from the previously demonstrated supplier rule. State the expected behavior on both sides of the new boundary.

## Extend and explain

Implement or adapt one bounded validation stage, a function checking the incoming images against the agreed rule, in the ordinary application source. Connect it to the preparation used for prediction. Keep the demonstrated function's default supplier rule available, and explicitly select the partner's threshold where preparation calls that function. Retain the source diff, the changed lines shown by Git, and record which rule is now applied. Explain each changed line, the accepted inputs and the return or rejection it produces.

Create executable checks for an accepted boundary, a rejected boundary, source preservation and the connection to the real prediction route. Show evidence of a failed check or rejected delivery before the relevant correction, then retain the passing evidence. Exercise the stage through a batch or request so the observation includes its connection to the application.

## Deliver and verify

Create an accepted manifest from your intake decisions, keeping the `image_id,path` columns. Run the real batch route using your saved CNN and a new output directory. Match output counts, identifiers and order against that manifest. Compare the reported model hash, its content fingerprint, with the hash of your saved model file, or checkpoint. Explain why retraining was unnecessary for this intake change.

Exercise a rejected case through an actual prediction script or HTTP request. Verify the documented failure behavior and the absence of an apparently complete batch result. Also demonstrate that the valid route continues to work. Use the same learned weights when comparing behavior.

Recommend batch or real-time delivery for the partner. Explain latency, throughput and cost drivers using the brief and your measurements, with the timer boundaries stated.

# Final check

Your retained evidence should let another engineer inspect the original files, your accepted/rejected decisions, the source change, the rule currently applied, a line-by-line explanation, boundary tests, actual predictions and delivery recommendation. Label which supplier rule each test checks, and update the prediction-route test's expected threshold to match the partner brief. Keep your first attempt and any repair so another engineer can follow what changed.

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

Morrow's handoff contains the checked incoming files, explained source, accepted predictions and a delivery recommendation tied to its review process. Keep the original CNN and evaluation as historical baseline evidence. Before comparing model improvements, retain the completed pipeline's code and confirm the same baseline training recipe with that code so later runs have a comparable starting point.
