"""Prepare labeled research cohorts and one explicitly constructed brightness shift.

Course fixture only: prediction applications never read these known labels.
"""

import argparse
import csv
from pathlib import Path
import shutil
import tempfile

import numpy as np
from PIL import Image

from catalog_mlops.artifacts import write_json
from catalog_mlops.data import load_arrays, verify_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    parser.add_argument("--output", type=Path, default=Path("work/cohorts"))
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    manifest = verify_data(args.data)
    images, labels = load_arrays(args.data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".cohorts-", dir=args.output.parent))
    try:
        for name, partition, factor in [
            ("reference", "reference", 1),
            ("current", "current", 1),
            ("shifted-current", "current", 0.45),
        ]:
            cohort = temporary / name
            cohort.mkdir()
            with (
                (cohort / "manifest.csv").open("w", newline="") as stream,
                (cohort / "labels.csv").open("w", newline="") as label_stream,
            ):
                inputs = csv.writer(stream)
                inputs.writerow(["image_id", "path"])
                known = csv.writer(label_stream)
                known.writerow(["image_id", "label"])
                for image_id in manifest["partitions"][partition]:
                    raw = images[image_id]
                    pixels = (
                        raw
                        if factor == 1
                        else np.rint(raw.astype(float) * factor).astype(np.uint8)
                    )
                    Image.fromarray(pixels).save(cohort / f"{image_id}.png")
                    inputs.writerow([f"train:{image_id}", f"{image_id}.png"])
                    known.writerow([f"train:{image_id}", int(labels[image_id])])
            write_json(
                cohort / "fixture.json",
                {
                    "kind": "unmodified research cohort"
                    if factor == 1
                    else "constructed brightness-shift exercise",
                    "partition": partition,
                    "image_ids": manifest["partitions"][partition],
                    "transformation": {
                        "multiply_brightness_by": factor,
                        "rounding": "numpy.rint",
                        "dtype": "uint8",
                    },
                    "data_sha256": manifest["raw_sha256"],
                    "split_sha256": manifest["split_sha256"],
                    "labels_policy": "Known labels are separate evaluation evidence; never prediction input.",
                },
            )
        lock = args.output.parent / f".{args.output.name}.lock"
        lock.mkdir()
        try:
            if args.output.exists():
                raise FileExistsError(args.output)
            temporary.rename(args.output)
        finally:
            lock.rmdir()
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    print(
        "Created reference, current and explicitly shifted-current cohorts in",
        args.output,
    )
