"""Check the intake function directly and through the batch entry point."""

import csv
import hashlib
import re
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from src.preprocessing import validate_intake

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
        sys.executable, "scripts/predict_batch.py",
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
        assert "contrast" in result.stderr.lower()
        assert not output.exists()
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == original_hash


def test_accepted_pixels_are_preserved():
    images = np.full((1, 28, 28), 60, dtype=np.uint8)
    images[:, :, 14:] = 80
    expected = images.copy()

    result = validate_intake(images)

    np.testing.assert_array_equal(result, expected, strict=True)
    np.testing.assert_array_equal(images, expected, strict=True)


def test_mixed_batch_reports_every_rejected_position():
    images = np.full((3, 28, 28), 86, dtype=np.uint8)
    images[0].fill(60)
    images[0, :, 14:] = 80
    images[1].fill(82)
    images[1, :, 14:] = 101

    with pytest.raises(ValueError, match="(?i)contrast") as error:
        validate_intake(images)

    message = str(error.value)
    # Accept lists and ordinary messages such as "contrast failed at 1 and 2".
    number_groups = re.findall(r"\b\d+(?:\s*,\s*(?:and\s+)?\d+|\s+(?:and\s+)?\d+)*\b", message)
    assert any(re.findall(r"\d+", group) == ["1", "2"] for group in number_groups), message


def test_invalid_shape_type_and_empty_batch_are_rejected():
    image = np.zeros((28, 28), dtype=np.uint8)
    image[:, 14:] = 20
    invalid_inputs = (
        image[None, :, :].tolist(),
        image,
        image[None, :-1, :],
        image[None, :, :].astype(np.float32),
        np.empty((0, 28, 28), dtype=np.uint8),
    )
    for images in invalid_inputs:
        with pytest.raises(ValueError):
            validate_intake(images)
