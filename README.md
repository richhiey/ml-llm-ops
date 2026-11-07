# Catalog MLOps

Train, evaluate and operate a small Fashion-MNIST CNN on a local CPU. The running case follows Threadline Retail as its catalog team investigates category suggestions, controlled improvements and reproducible operation.

Start with the [local setup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md), then read the [project story](https://github.com/richhiey/ml-llm-ops/blob/main/docs/project-story.md) and [Campus lessons](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/README.md).

```bash
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --frozen
uv run --frozen catalog-mlops prepare
uv run --frozen catalog-mlops train --config configs/baseline.json --output work/runs/baseline
uv run --frozen catalog-mlops evaluate --run work/runs/baseline
```

The two-convolution CNN has 55,338 parameters. Its CPU profile uses 12,000 training and 3,000 validation images with recorded indices. The official test split is reserved for reporting after selection. Every run retains weights, configuration, data/split identities, code snapshot, environment, validation predictions and metrics.

## Application layout

| Location | Purpose |
|---|---|
| `src/catalog_mlops/` | Reusable ingestion, preprocessing, training, evaluation and inference operations |
| `configs/` | Explicit training recipes |
| `tests/` | Contract and artifact-integrity regression checks |
| `notebooks/` | Local companion notebooks importing the reusable core |
| `docs/course/` | Campus lessons and clearly labeled exercise material |
| `work/` | Your ignored run artifacts, intake files and observations |
| `data/` | Your ignored verified dataset cache |

Use [the inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) to compare batch and HTTP delivery. Read [the dataset card](https://github.com/richhiey/ml-llm-ops/blob/main/docs/dataset-card.md) for task limits and attribution.

Development proceeds sequentially through the three sprints. Published revision evidence will identify which project stages have been verified.
