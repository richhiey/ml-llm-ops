✂️
# Explain-the-code checkpoint

Threadline receives an AI-authored proposal claiming to prepare supplier thumbnails on the saved CNN's expected scale. It produces the right-looking shape for an ordinary image. Your job is to decide whether the claim survives examples chosen to distinguish it from the documented preparation.

The [review candidate](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/generated_preprocessing.py) is a deliberately flawed, inactive course proposal. It is outside application source. Keep it separate while you investigate.

The full proposed implementation is visible here. Copy it into your probe script and investigate the behavior before connecting any proposal to application source.

```python
import numpy as np

def prepare_candidate(images):
    raw = np.asarray(images, dtype=np.float32)
    maximum = raw.max(axis=(1, 2), keepdims=True)
    normalized = raw / maximum
    return normalized[:, None, :, :]
```

# Your task

Review every executable line in `prepare_candidate()` and explain the input, intermediate shape, scaling rule and returned shape. Create `work/review_candidate.py` with your own probes and retain the output.

Your evidence must address all three questions.

- Does the candidate preserve the saved model's intensity scale across different thumbnails?
- Does it always produce finite numeric values for structurally valid raw arrays?
- What belongs at the intake boundary when an image fails Threadline's quality policy?

Use the [pipeline contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md) as the acceptance basis. Include at least one plausible input on which the proposal appears to work and two counterexamples that test different assumptions. Compare its output with the shared preparation where the input is accepted. State your expected result before running each probe.

Finish with a merge recommendation, a precise correction and a check that would prevent this failure from returning. If an assistant helps you review, validate its claims against the actual arrays and code.

# Working with documentation

| Investigate | Documentation |
|---|---|
| Which axes are reduced and kept | [NumPy maximum](https://numpy.org/doc/stable/reference/generated/numpy.max.html) |
| Whether every output is a usable finite value | [NumPy isfinite](https://numpy.org/doc/stable/reference/generated/numpy.isfinite.html) |
| How raw pixels enter the real model | [Shared preprocessing source](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/preprocessing.py) |

# Hints

<details>
<summary>Hint 1</summary>

The proposal chooses a scale from each input. Consider what happens when two files have different brightest pixels but their numbers use the same documented raw scale.

</details>

<details>
<summary>Hint 2</summary>

Check the value used as the divisor. A shape test can pass while a division produces unusable values.

</details>

# Checkpoints

Record the original input values and whether they changed. Inspect shape and dtype, but also inspect numeric values and finiteness. Explain how a passing example could conceal the error. Keep your attempt and recommendation before opening the feedback.

<details>
<summary>Reference feedback</summary>

**Result you should get**

A thumbnail containing pixel `128` as its maximum becomes `1.0` in the candidate, whereas the saved scale maps that value to approximately `0.502`. An all-zero raw image causes division by zero and non-finite values. A thumbnail whose maximum is `255` can make the proposal appear correct. The proposed replacement should be rejected until its preparation matches the declared model contract.

**How**

The conversion creates a float32 array. `max(axis=(1, 2), keepdims=True)` produces one divisor per image with shape `(N, 1, 1)`. Division therefore rescales each image differently. The final slice adds a channel dimension and can conceal that numeric mismatch behind a correct `(N, 1, 28, 28)` shape.

Use fixed scaling by `255` through the shared preparation. Keep intake-quality rejection before model input. The all-zero probe tests the proposal directly, while the operational policy should reject such a file before prediction. Test a valid lower-maximum thumbnail with sufficient range to separate scaling correctness from intake rejection.

</details>

## Learning outcome

Given an AI-generated addition to the pipeline, explain line by line what it does, test its input/output contract, and identify any part that needs correction before merging.

## Summary

Threadline's merge decision is supported by input values, executable counterexamples and a correction tied to the saved model contract. Your review explains what the code actually does and why an ordinary passing example is insufficient evidence for deployment.
