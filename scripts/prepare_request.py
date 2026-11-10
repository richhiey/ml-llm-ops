"""Convert one grayscale PNG to the JSON body sent by curl. No HTTP is hidden here."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--image-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with Image.open(args.image) as image:
        if image.mode != "L" or image.size != (28, 28):
            raise ValueError("Expected an existing 28x28 grayscale PNG; no conversion is applied")
        pixels = np.asarray(image).tolist()
    payload = {"image_id": args.image_id, "pixels": pixels}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream)
        stream.write("\n")
    print(f"Wrote {args.output}; inspect it before sending with curl")
