"""Describe delivered images, adding measured classification quality only when labels are supplied."""

import argparse
import json
from pathlib import Path
from catalog_mlops.artifacts import write_json
from catalog_mlops.monitoring import observe_delivery

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--labels", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = observe_delivery(args.batch, args.labels)
    write_json(args.output, report, overwrite=False)
    summary = {
        key: report[key]
        for key in (
            "count",
            "model",
            "quality_available",
            "mean_brightness_counts",
            "predicted_category_counts",
        )
    }
    summary["output"] = str(args.output)
    if report["quality_available"]:
        summary["quality"] = {
            key: report["quality"][key] for key in ("accuracy", "macro_f1")
        }
    print(json.dumps(summary, indent=2, allow_nan=False))
