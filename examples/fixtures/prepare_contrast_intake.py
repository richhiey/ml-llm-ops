"""Generate synthetic thumbnails on either side of a contrast threshold."""

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    output = parser.parse_args().output
    output.mkdir(parents=True, exist_ok=False)

    for brightness_range in (19, 20):
        pixels = np.full((28, 28), 86, dtype=np.uint8)
        pixels[:, 14:] = 86 + brightness_range
        Image.fromarray(pixels).save(output / f"range-{brightness_range}.png")

    for filename, ranges in (("boundary.csv", (20,)), ("mixed.csv", (20, 19))):
        with (output / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["image_id", "path"])
            writer.writerows((f"range-{value}", f"range-{value}.png") for value in ranges)


if __name__ == "__main__":
    main()
