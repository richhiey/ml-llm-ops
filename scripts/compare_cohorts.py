"""Compare incoming-image distributions under the same loaded model and preparation."""

import argparse
import json
from pathlib import Path
from catalog_mlops.artifacts import read_json, write_json
from catalog_mlops.monitoring import compare_cohorts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = compare_cohorts(read_json(args.reference), read_json(args.current))
    write_json(args.output, report, overwrite=False)
    print(json.dumps(report, indent=2, allow_nan=False))
