"""Generate a flat thumbnail with a batch manifest and an HTTP request."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

intake = Path("work/quality-intake")
intake.mkdir(parents=True, exist_ok=False)
pixels = np.full((28, 28), 86, dtype=np.uint8)
Image.fromarray(pixels).save(intake / "flat.png")
(intake / "manifest.csv").write_text("image_id,path\nflat-item,flat.png\n")
(intake / "request.json").write_text(json.dumps({"image_id": "flat-item", "pixels": pixels.tolist()}) + "\n")
print("Created a constant-intensity PNG, one-row manifest and HTTP request body in", intake)
