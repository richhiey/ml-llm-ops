"""Construct a supplier intake for independent acceptance work.

The exported products are real research images. The extra intake defects are
constructed course conditions, not observed supplier incidents.
"""

import argparse
import csv
from pathlib import Path
import shutil
import tempfile

import numpy as np
from PIL import Image

from catalog_mlops.data import load_arrays, verify_data


def prepare(data: Path, output: Path) -> None:
    if output.exists():
        raise FileExistsError(f"Retain the existing intake or select a new destination: {output}")
    manifest = verify_data(data)
    images, _ = load_arrays(data)
    source = np.asarray(manifest["partitions"]["current"]).reshape(10, 100).T.flatten()[20:40]
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(dir=output.parent, prefix=".supplier-intake-"))
    try:
        for position, image_id in enumerate(source, 1):
            Image.fromarray(images[image_id]).save(temporary / f"item-{position:03d}.png")
        special = [np.full((28, 28), 86, dtype=np.uint8),
                   np.tile(np.arange(24, dtype=np.uint8), (28, 2))[:, :28],
                   np.full((28, 28, 3), 180, dtype=np.uint8),
                   np.full((32, 32), 180, dtype=np.uint8)]
        for position, image in enumerate(special, 21):
            Image.fromarray(image).save(temporary / f"item-{position:03d}.png")
        with (temporary / "intake.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["image_id", "path"])
            for position in range(1, 25):
                writer.writerow([f"MM-{position:03d}", f"item-{position:03d}.png"])
        temporary.rename(output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--output", type=Path, default=Path("work/morrow-intake"))
    arguments = parser.parse_args()
    prepare(arguments.data, arguments.output)
    print(f"Created 24-record constructed supplier intake at {arguments.output}")
