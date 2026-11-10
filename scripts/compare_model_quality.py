"""Compare two loaded models on the exact same delivered images and known labels."""

import argparse
import json
from pathlib import Path
from src.artifacts import read_json, write_json
from src.monitoring import compare_model_quality

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = compare_model_quality(read_json(args.first), read_json(args.second))
    write_json(args.output, report, overwrite=False)
    print(json.dumps(report, indent=2, allow_nan=False))
