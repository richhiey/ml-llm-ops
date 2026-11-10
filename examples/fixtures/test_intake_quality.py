"""Copy into tests/ to check the intake policy through the actual batch process."""
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
        assert "contrast" in result.stderr
        assert not output.exists()
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == original_hash
