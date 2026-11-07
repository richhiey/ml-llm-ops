"""Small application commands that expose the reusable pipeline operations."""

import argparse
import json
from pathlib import Path
import urllib.request

from catalog_mlops.artifacts import read_json
from catalog_mlops.data import load_arrays, prepare_data, verify_data
from catalog_mlops.evaluation import evaluate
from catalog_mlops.inference import export_samples, predict_batch, read_thumbnail
from catalog_mlops.model import TrainingConfig
from catalog_mlops.training import configure_cpu, load_model, make_loader, runtime_source_sha256, train, verify_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="catalog-mlops")
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="Download and verify the dataset and fixed splits")
    prepare.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    training = commands.add_parser("train", help="Train one fresh CNN from a declared configuration")
    training.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    training.add_argument("--config", type=Path, required=True)
    training.add_argument("--output", type=Path, required=True)
    score = commands.add_parser("evaluate", help="Evaluate a saved checkpoint on its fixed validation data")
    score.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    score.add_argument("--run", type=Path, required=True)
    samples = commands.add_parser("samples", help="Export prepared thumbnails and an inference manifest")
    samples.add_argument("--data", type=Path, default=Path("data/fashion-mnist"))
    samples.add_argument("--partition", default="current")
    samples.add_argument("--count", type=int, default=20)
    samples.add_argument("--output", type=Path, required=True)
    batch = commands.add_parser("batch", help="Predict labels for all images named in a CSV manifest")
    batch.add_argument("--run", type=Path, required=True)
    batch.add_argument("--manifest", type=Path, required=True)
    batch.add_argument("--output", type=Path, required=True)
    serving = commands.add_parser("serve", help="Start a local HTTP consumer pinned to one model")
    serving.add_argument("--run", type=Path, required=True)
    serving.add_argument("--port", type=int, default=8000)
    request = commands.add_parser("request", help="Send one thumbnail to the running HTTP consumer")
    request.add_argument("--image", type=Path, required=True)
    request.add_argument("--image-id", required=True)
    request.add_argument("--port", type=int, default=8000)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "prepare":
        result = prepare_data(args.data)
        result = {"name": result["name"], "split_sha256": result["split_sha256"],
                  "counts": {name: len(ids) for name, ids in result["partitions"].items()}}
    elif args.command == "train":
        result = train(args.data, args.output, TrainingConfig(**read_json(args.config)))
    elif args.command == "evaluate":
        record = verify_run(args.run)
        manifest = verify_data(args.data)
        if record["split_sha256"] != manifest["split_sha256"]:
            raise ValueError("Evaluation split differs from the training run")
        images, labels = load_arrays(args.data)
        model, checkpoint = load_model(args.run / "model.pt")
        config = TrainingConfig(**checkpoint["config"])
        configure_cpu(config)
        result, _, _ = evaluate(model, make_loader(images, labels, manifest["partitions"]["validation"], config))
        result["evaluation_evidence"] = {
            "model_sha256": record["model_sha256"],
            "training_source_sha256": record["source"]["source_sha256"],
            "evaluation_source_sha256": runtime_source_sha256(),
            "split_sha256": manifest["split_sha256"],
        }
    elif args.command == "samples":
        result = export_samples(args.data, args.partition, args.count, args.output)
    elif args.command == "batch":
        result = predict_batch(args.run, args.manifest, args.output)
    elif args.command == "serve":
        import uvicorn
        from catalog_mlops.service import create_app
        uvicorn.run(create_app(args.run), host="127.0.0.1", port=args.port)
        return
    else:
        payload = {"image_id": args.image_id, "pixels": read_thumbnail(args.image).tolist()}
        request = urllib.request.Request(f"http://127.0.0.1:{args.port}/predict",
                                         data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.load(response)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
