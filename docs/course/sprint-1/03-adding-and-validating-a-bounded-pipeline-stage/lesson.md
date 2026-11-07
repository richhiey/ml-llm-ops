📝
# Adding and validating a bounded pipeline stage

Threadline's first supplier trial includes thumbnails that have the right dimensions but almost no visible intensity variation. The existing boundary checks shape and dtype. The catalog team adds a specific intake rule so these low-information files reach a specialist for correction before category prediction.

For this supplier, each accepted thumbnail must have a brightest-minus-darkest pixel value of at least `20`. This is a declared exercise policy. It checks one kind of intake problem and needs its own evidence. You will add the check, connect it to inference and verify that valid predictions still work.

# 1. Locate the change boundary

Open [preprocessing.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/preprocessing.py) and find `validate_images()` and `preprocess()`. Trace `Predictor.predict()` in [inference.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/inference.py).

Both batch and HTTP consumers call the predictor's shared preparation. The appropriate insertion point is before normalization, while pixels still use their documented `0–255` scale. A **contract** states the inputs a function accepts, its output and how it signals failure.

| Input condition | Existing structural boundary | New supplier policy |
|---|---|---|
| Wrong shape or dtype | Reject | Preserve rejection |
| Constant grayscale image | Accept as structurally valid | Reject for insufficient range |
| Correct thumbnail with range `20` | Accept | Accept |
| Correct thumbnail with range `19` | Accept | Reject |

Expect to find one shared inference preparation function. Keep the model architecture, normalization and saved checkpoint fixed during this extension.

# 2. Write checks before the implementation

Create `tests/test_intake_quality.py` with these checks.

```python
import csv
import hashlib
import subprocess
import sys
from pathlib import Path
import numpy as np
import pytest
from PIL import Image

ACTIVE_MINIMUM_RANGE = 20

@pytest.mark.parametrize("base,pixel_range", [
    (0, 0),
    (86, 0),
    (0, ACTIVE_MINIMUM_RANGE - 1),
    (0, ACTIVE_MINIMUM_RANGE),
])
def test_intake_policy_through_batch(base, pixel_range, tmp_path):
    raw = np.full((28, 28), base, dtype=np.uint8)
    raw[:, 14:] = base + pixel_range
    image_path = tmp_path / "thumbnail.png"
    Image.fromarray(raw).save(image_path)
    original_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
    manifest_path = tmp_path / "manifest.csv"
    manifest_path.write_text("image_id,path\nexample,thumbnail.png\n")
    output = tmp_path / "delivery"
    result = subprocess.run([
        sys.executable, "-m", "catalog_mlops.cli", "batch",
        "--run", "work/runs/baseline",
        "--manifest", str(manifest_path), "--output", str(output),
    ], capture_output=True, text=True)
    if pixel_range >= ACTIVE_MINIMUM_RANGE:
        assert result.returncode == 0, result.stderr
        with (output / "predictions.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == 1 and rows[0]["image_id"] == "example"
    else:
        assert result.returncode != 0
        assert "contrast" in result.stderr
        assert not output.exists()
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == original_hash
```

```bash
uv run --frozen pytest -q tests/test_intake_quality.py
```

This first failure is intentional. The starter accepts these structurally valid thumbnails, so the rejection cases fail. Each test runs the actual public batch command in another Python process. The rejected-boundary case will also fail if a new validation function exists but is never connected to the pipeline.

`ACTIVE_MINIMUM_RANGE` records the policy expected by this integration test. When a partner requirement changes, update both the active source policy and the independently stated test expectation, then test the new boundary. Keep the earlier requirement and observed results in your source history.

# 3. Implement the bounded check

The structural function already in the source has this implementation. Its accepted output is the caller's original array.

```python
def validate_images(images: np.ndarray) -> np.ndarray:
    if not isinstance(images, np.ndarray):
        raise ValueError("Images must be a NumPy array")
    if images.dtype != np.uint8:
        raise ValueError("Raw image pixels must use uint8, representing values from 0 to 255")
    if images.ndim != 3 or images.shape[1:] != (28, 28) or len(images) == 0:
        raise ValueError("Expected a nonempty batch with shape (N, 28, 28)")
    return images
```

The source file already imports NumPy as `np`. Add the following function after `validate_images()`.

```python
def validate_contrast(images: np.ndarray, minimum_range: int = 20) -> np.ndarray:
    raw = validate_images(images)
    if not 0 <= minimum_range <= 255:
        raise ValueError("Minimum range must be between 0 and 255")
    ranges = np.ptp(raw, axis=(1, 2))
    failing_positions = np.flatnonzero(ranges < minimum_range)
    if failing_positions.size:
        raise ValueError(
            f"Insufficient contrast at batch positions {failing_positions.tolist()}"
        )
    return raw
```

`np.ptp()` computes the maximum minus minimum over the two image axes. The result has one range per image. `np.flatnonzero()` identifies the batch positions failing the declared threshold. The function returns the original accepted array without changing its pixels.

Now change the first line of `preprocess()` to call the new stage.

```python
def preprocess(images: np.ndarray) -> torch.Tensor:
    raw = validate_contrast(images, minimum_range=20)
    return normalize_pixels(torch.from_numpy(raw.copy()).unsqueeze(1))
```

The final numeric conversion has the following implementation in the same source file. It creates a float32 tensor on the declared scale.

```python
def normalize_pixels(raw: torch.Tensor) -> torch.Tensor:
    if raw.dtype != torch.uint8 or raw.ndim != 4 or tuple(raw.shape[1:]) != (1, 28, 28):
        raise ValueError("Expected uint8 grayscale tensors with shape (N, 1, 28, 28)")
    return raw.to(dtype=torch.float32).div(255.0)
```

`validate_contrast()` reuses the existing structural validation. Its parameter makes the policy explicit at the call site. Keep the function's default of `20` for the demonstrated supplier contract. A different partner can select another threshold at its inference boundary and test that policy separately. The channel conversion and division by `255` keep their prior behavior.

# 4. Verify the function and integration

```bash
uv run --frozen pytest -q tests/test_intake_quality.py
uv run --frozen pytest -q
git diff -- src/catalog_mlops/preprocessing.py
```

Expect four new quality checks to pass and the existing mechanics checks to remain passing. Inspect the diff and explain each changed statement, including how the failure positions relate to image order. Passing the contrast function's direct checks alone would miss an omitted call in `preprocess()`.

Do not rerun training to explain this change. The new intake rule decides which incoming images can reach the saved classifier. It does not change the saved weights.

# 5. Exercise the actual batch consumer

Create `work/check_quality_route.py` with the following code.

```python
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image

intake = Path("work/quality-intake")
intake.mkdir(exist_ok=True)
Image.fromarray(np.full((28, 28), 86, dtype=np.uint8)).save(intake / "flat.png")
(intake / "manifest.csv").write_text(
    "image_id,path\nflat-item,flat.png\n", encoding="utf-8"
)
output = Path("work/batches/quality-rejection")
result = subprocess.run([
    sys.executable, "-m", "catalog_mlops.cli", "batch",
    "--run", "work/runs/baseline",
    "--manifest", str(intake / "manifest.csv"), "--output", str(output),
], capture_output=True, text=True)
print(result.stderr)
assert result.returncode != 0 and "contrast" in result.stderr
assert not output.exists()
```

```bash
uv run --frozen python work/check_quality_route.py
uv run --frozen catalog-mlops batch --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/after-quality-stage
```

Expect the low-range intake to fail with its batch position and leave the requested output absent. Expect the valid `20`-image intake to produce a completed new batch. Compare its rows with `work/batches/baseline/predictions.csv`. Identifiers, classes and scores should agree because accepted images still use the same preparation and weights.

Inspect `batch.json`. The training source identity still refers to the baseline's archived code. The inference source identity records the edited code used by this consumer. This distinction lets another engineer see which part changed.

# 6. Verify the request boundary

Restart the service after editing source. In a second terminal, run the normal serving command with `work/runs/baseline` and port `8000`. In your first terminal, send the low-range file.

```bash
uv run --frozen catalog-mlops request --image work/quality-intake/flat.png --image-id flat-item --port 8000
```

Expect an HTTP `422` validation response. The command exits with an error because the server rejected the input. Now request a valid image from `work/intake` and verify that its prediction matches the retained batch row. Stop the service when finished.

# Watch out for

Check raw intensity range before normalization so threshold `20` has the intended units. Exercise the accepted boundary as well as rejected examples. Preserve the original image array. Restart imported code after changes. A high range can still occur in a poor photograph, so this bounded policy requires careful interpretation.

# Quick reference

| Check | Evidence |
|---|---|
| Policy boundary through the public consumer | Constants rejected, `19` rejected, `20` accepted, source image file unchanged |
| Shared preparation | Source trace and the public batch command establish that the new stage is called |
| Real batch route | Failed delivery remains unpublished and valid predictions agree |
| Real HTTP route | Rejected input returns `422`, valid response uses the retained model |

## Learning outcome

Follow an expert adding one preprocessing or validation stage to the provided pipeline, then verify its input/output contract and confirm that the unchanged stages still run.

## Summary

Threadline's supplier policy is now an implemented stage with a clear scale, failure condition and integration path. You have evidence that the new rejection works and that valid input still reaches the same saved classifier correctly. A proposed preparation change can be reviewed with the same combination of explanation and discriminating tests.
