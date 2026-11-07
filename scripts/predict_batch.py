"""Read an image manifest and publish a complete prediction CSV."""
import argparse
import json
from pathlib import Path
from catalog_mlops.inference import predict_batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(predict_batch(args.run, args.manifest, args.output), indent=2, allow_nan=False))
