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
    print(json.dumps(report, indent=2, allow_nan=False))
