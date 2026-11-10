"""Read an image manifest and publish a complete prediction CSV."""
import argparse
import json
from pathlib import Path
from src.inference import predict_batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report-errors", action="store_true",
                        help="Write results.csv with a prediction or input error for every manifest row.")
    args = parser.parse_args()
    report = predict_batch(args.run, args.manifest, args.output, report_errors=args.report_errors)
    print(json.dumps(report, indent=2, allow_nan=False))
