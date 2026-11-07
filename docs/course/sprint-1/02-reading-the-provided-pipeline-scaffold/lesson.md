📝
# Reading the provided pipeline scaffold

Threadline's catalog team wants a first working classifier and an honest account of its mistakes. You will follow the supplied pipeline from verified thumbnails to a trained CNN, then reload that CNN and use both delivery routes.

Use one local clone in VS Code. Finish with a retained baseline run, validation evidence, a batch CSV and a real HTTP prediction from the same saved model. The [setup guide](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md) supplies installation and recovery steps. The [local companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) shows the same data loading, model definition and evaluation directly with standard libraries.

This walkthrough has two stopping points. First retain the trained/evaluated baseline. Then run the inference routes. Keep completed artifacts when you resume.

# 1. Verify your starting point

Run these commands from the repository root.

```bash
uv sync --frozen
uv run --frozen catalog-mlops prepare
```

The environment is installed from the committed lock. Dataset preparation verifies the original files before creating its split manifest. Wait until preparation finishes.

Expect `fashion-mnist-cpu-v1`, a split hash, `train=12000` and `validation=3000`. There are also separate operational pools for later investigations. Keep the official test images reserved.

# 2. Inspect the actual images and labels

Create `work/inspect_dataset.py` with the following code, then run it.

```python
from pathlib import Path
import gzip
import json
import struct
import numpy as np
import matplotlib.pyplot as plt

data = Path("data/fashion-mnist")
manifest = json.loads((data / "manifest.json").read_text())
with gzip.open(data / "train-images-idx3-ubyte.gz", "rb") as stream:
    magic, count, height, width = struct.unpack(">IIII", stream.read(16))
    images = np.frombuffer(stream.read(), dtype=np.uint8).reshape(count, height, width)
with gzip.open(data / "train-labels-idx1-ubyte.gz", "rb") as stream:
    label_magic, label_count = struct.unpack(">II", stream.read(8))
    labels = np.frombuffer(stream.read(), dtype=np.uint8)
assert (magic, height, width) == (2051, 28, 28)
assert label_magic == 2049 and label_count == count

class_names = ("T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot")
train_ids = manifest["partitions"]["train"]
validation_ids = manifest["partitions"]["validation"]
print(images.shape, images.dtype, labels.shape)
print("Training counts", np.bincount(labels[train_ids], minlength=10))
print("Validation counts", np.bincount(labels[validation_ids], minlength=10))
assert set(train_ids).isdisjoint(validation_ids)

figure, axes = plt.subplots(2, 5, figsize=(11, 4.5), layout="constrained")
for label, axis in enumerate(axes.flat):
    image_id = next(index for index in train_ids if labels[index] == label)
    axis.imshow(images[image_id], cmap="gray", vmin=0, vmax=255)
    axis.set_title(class_names[label])
    axis.set_xlabel(f"train:{image_id}")
    axis.set_xticks([])
    axis.set_yticks([])
figure.savefig("work/training-examples.png", dpi=150)
```

```bash
uv run --frozen python work/inspect_dataset.py
```

The compressed files use the IDX binary format. `struct.unpack()` reads their headers, and `np.frombuffer()` interprets the remaining bytes as raw integer pixels or labels. The JSON manifest contains the exact indices selected by the pipeline, which you can inspect directly.

Expect image shape `(60000, 28, 28)`, dtype `uint8` and label shape `(60000,)`. Each training class has `1200` examples and each validation class has `300`. Open `work/training-examples.png` in VS Code. The plot loop selects and draws one actual training example for each label. The raw file contains more images than the bounded CPU training profile uses.

![One actual training example from each of the ten categories, with its original sample identifier](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/fashion-mnist-examples__01__en.png)

Each research thumbnail presents one prepared front-view product image. Shirts, pullovers and coats share visual structure at this resolution. The model has to learn distinctions that can be difficult even to inspect in a small image.

# 3. Trace preparation and the model

Open the source functions shown below. Follow their callers in the editor rather than starting a separate implementation.

| Source | What to trace |
|---|---|
| [data.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/data.py) | Download hashes, original arrays and fixed indices |
| [preprocessing.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/preprocessing.py) | Structural checks, channel dimension and one division by `255` |
| [model.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py) | The complete `CatalogCNN` definition |
| [training.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/training.py) | Fresh initialization, weight updates, validation and checkpoint save/reload |

The CNN has two convolutional layers. A **convolution** applies a learned small filter across the image. A **ReLU** activation keeps positive responses and maps negative responses to zero. **Pooling** reduces the spatial resolution by taking the strongest response in a small region.

| Point in the CNN | Shape for one image |
|---|---|
| Prepared input | `1 × 28 × 28` |
| First convolution and pooling | `16 × 14 × 14` |
| Second convolution and pooling | `32 × 7 × 7` |
| Flattened features | `1568` values |
| Hidden classifier layer | `32` values |
| Output | `10` category scores |

The complete model uses ordinary PyTorch layers. Read this definition alongside `model.py`. Append it to `work/inspect_dataset.py` so it is available for the direct checkpoint inspection below.

```python
import torch
from torch import nn

class CatalogCNN(nn.Module):
    def __init__(self, dropout=0.0):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 10),
        )

    def forward(self, inputs):
        return self.classifier(self.features(inputs))
```

Those final raw scores are **logits**. The training loss compares logits with the known category and the optimizer adjusts weights to reduce that loss. The small model has `55,338` trainable parameters. An **epoch** is one pass through the training examples.

# 4. Train the baseline from fresh weights

Inspect `configs/baseline.json`. It declares four epochs, batch size `64`, learning rate `0.001` and seed `426`. The **learning rate** controls the size of optimizer updates. The seed controls recorded sources of randomness within the declared environment.

```bash
uv run --frozen catalog-mlops train --config configs/baseline.json --output work/runs/baseline
```

The weight-update loop inside the supplied pipeline follows these operations. Read the excerpt alongside `training.py`. Here, `model` is the CNN above, `training` yields raw image/label batches, and `optimizer` is Adam configured from `baseline.json`.

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
model.train()
for raw_images, known_labels in training:
    inputs = raw_images.to(dtype=torch.float32) / 255.0
    optimizer.zero_grad(set_to_none=True)
    logits = model(inputs)
    loss = nn.functional.cross_entropy(logits, known_labels)
    loss.backward()
    optimizer.step()
```

This is an excerpt to inspect inside its existing training context. Division prepares the input scale. Clearing gradients prevents accidental accumulation. `backward()` computes gradients and `step()` updates weights. Validation omits these updates. The application command executes the full pipeline and retains its artifacts.

Expect four epoch observations and a completed `work/runs/baseline` directory. `train()` constructs a new CNN before learning. It does not start from a supplied pretrained checkpoint. Validation runs between epochs without updating weights.

If this directory already holds a completed run, inspect and reuse it. Choose a new directory only when deliberately making another run. A fresh command in the same environment should repeat the declared recipe, while results across platforms can differ.

# 5. Read the retained learning and evaluation evidence

Run evaluation through the saved checkpoint.

```bash
uv run --frozen catalog-mlops evaluate --run work/runs/baseline
```

Expect `count=3000`, overall accuracy, macro F1, per-class metrics and a confusion matrix. `model.eval()` selects evaluation behavior, and inference mode avoids tracking gradients. The report uses the same fixed validation IDs as training's validation observations.

The author's observed reference run reached accuracy `0.8380` and macro F1 `0.8322`. These numbers describe one CPU run under the recorded recipe. Inspect your own retained predictions to explain your result.

Append the following code to `work/inspect_dataset.py`. It loads the declared architecture and saved weights, performs validation with PyTorch directly, computes metrics with scikit-learn and draws both plots with Matplotlib.

```python
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from torch.utils.data import DataLoader, TensorDataset

run = Path("work/runs/baseline")
checkpoint = torch.load(run / "model.pt", map_location="cpu", weights_only=True)
model = CatalogCNN(dropout=checkpoint["config"]["dropout"])
model.load_state_dict(checkpoint["state_dict"])
model.eval()
torch.set_num_threads(checkpoint["config"]["cpu_threads"])
validation = TensorDataset(
    torch.from_numpy(images[validation_ids].copy()).unsqueeze(1),
    torch.from_numpy(labels[validation_ids].astype(np.int64)),
)
loader = DataLoader(validation, batch_size=64, shuffle=False)
truth, predictions = [], []
with torch.inference_mode():
    for raw_images, known_labels in loader:
        logits = model(raw_images.to(dtype=torch.float32) / 255.0)
        predictions.extend(logits.argmax(dim=1).tolist())
        truth.extend(known_labels.tolist())
print("Accuracy", accuracy_score(truth, predictions))
print("Macro F1", f1_score(truth, predictions, average="macro"))
print(classification_report(truth, predictions, labels=range(10),
                            target_names=class_names, zero_division=0))

history = json.loads((run / "history.json").read_text())
epochs = [row["epoch"] for row in history]
figure, axis = plt.subplots(figsize=(8, 4), layout="constrained")
axis.plot(epochs, [row["train_loss"] for row in history], "o-", label="Training")
axis.plot(epochs, [row["validation_loss"] for row in history], "s--", label="Validation")
axis.set(xlabel="Epoch", ylabel="Cross-entropy loss (unitless)", xticks=epochs)
axis.legend()
figure.savefig("work/learning-history.png", dpi=150)

matrix = confusion_matrix(truth, predictions, labels=range(10))
figure, axis = plt.subplots(figsize=(9, 7), layout="constrained")
image = axis.imshow(matrix, cmap="Greens", vmin=0)
axis.set_xticks(range(10), class_names, rotation=40, ha="right")
axis.set_yticks(range(10), class_names)
axis.set_xlabel("Predicted category")
axis.set_ylabel("Actual category")
figure.colorbar(image, ax=axis, label="Images")
figure.savefig("work/confusion-matrix.png", dpi=150)
```

```bash
uv run --frozen python work/inspect_dataset.py
```

Expect two figures derived from your own observations. **Cross-entropy loss** measures disagreement with the known labels. Smaller loss is better under the same evaluation conditions. Training loss comes from examples used for updates, while validation loss comes from separate examples. These four observations alone do not prove what a longer run would achieve.

![Observed training and validation loss over four epochs of the author's baseline](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/baseline-learning-history__01__en.png)

**Recall** for a category is the fraction of its actual examples classified correctly. **Precision** is the fraction of predictions for that category that are correct. F1 combines precision and recall. **Macro F1** averages F1 equally across the ten categories, matching the catalog brief's equal-category priority.

![Actual categories on rows and predictions on columns for 3,000 validation images in the author's baseline](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/baseline-confusion-matrix__01__en.png)

The reference found `117` of `300` shirts, giving shirt recall `0.39`. It classified `73` shirts as coats and `70` as T-shirts/tops. That is a specific weakness to investigate, even though overall accuracy is much higher. In your matrix, follow one actual category across its row and explain the largest error.

# 6. Identify what was saved

Inspect the files in the completed run.

| Artifact | What it establishes |
|---|---|
| `config.json` and `history.json` | Recipe and observed learning curve |
| `dataset.json` | Original file identities, class order and split indices |
| `model.pt` | Learned weights and model/preprocessing declaration |
| `metrics.json` and `validation-predictions.csv` | Evaluation summary and the predictions supporting it |
| `source.zip`, `environment.json` and `run.json` | Code/environment record and connected artifact hashes |

A **hash** is a content fingerprint. Changing a byte changes the expected fingerprint. Here, hashes help detect mismatched artifacts. They also need retrievable files to support later reproduction.

The underlying file operation uses Python's `hashlib` directly.

```python
import hashlib
model_hash = hashlib.sha256(Path("work/runs/baseline/model.pt").read_bytes()).hexdigest()
print(model_hash)
```

Expect this value to match the model fingerprint in the saved run record.

This is the first stopping point. Keep these artifacts when you close the editor.

# 7. Run a batch with the saved CNN

Export a small unlabeled intake from the independent incoming pool, then invoke the normal batch route.

```bash
uv run --frozen catalog-mlops samples --count 20 --output work/intake
uv run --frozen catalog-mlops batch --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/baseline
```

Expect `20` rows in `work/batches/baseline/predictions.csv`, plus `batch.json`. Compare image identifiers and order with `work/intake/manifest.csv`. The model supplies a `class_id`, `class_name` and `top_score` for each image. **Softmax** converts the ten logits into normalized scores. The largest score is not a calibrated guarantee of correctness.

Open [inference.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/inference.py). Trace manifest → `read_thumbnail()` → `Predictor.predict()` → `preprocess()` → saved CNN → identified predictions. The input manifest has `image_id,path` and supplies no label.

# 8. Call the real-time route

In a second terminal at the repository root, start the local service.

```bash
uv run --frozen catalog-mlops serve --run work/runs/baseline --port 8000
```

Expect a message that the service is listening on port `8000`. It loads and pins that saved model at startup. Keep this terminal running.

In your first terminal, use the first image from the generated intake.

```bash
uv run --frozen catalog-mlops request --image work/intake/56368.png --image-id train:56368 --port 8000
```

The fixed manifest's first image is `train:56368`. Expect an HTTP response containing its prediction, model identity and service-side processing time. Compare its class with the matching batch row. Class IDs must agree, and top-score difference should be at most `1e-6` to allow floating-point roundoff. The model hash must match the batch record.

Stop the service with `Ctrl+C` in its terminal when finished. The [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) explains the two clients and what the timers include.

Finish your annotated stage trace. For each of the five stages, record its actual function name, purpose, input, output and one observed artifact. Trace one training image identifier and one incoming identifier, and show where the saved CNN connects their two routes. Use your retained files as the labels on that trace.

# Project assembly

The implementations above establish how the packages work. For project construction, the repository packages those operations into reusable functions and adds file validation, identity records and complete-output delivery.

| Operation you inspected | Repository entry point | Project responsibility |
|---|---|---|
| IDX headers, NumPy arrays and recorded indices | `prepare_data()` and `load_arrays()` | Verified dataset access |
| PyTorch layers, Adam, loss, backward pass and updates | `train()` | One configured learning run and retained artifacts |
| `torch.load()`, `load_state_dict()` and `eval()` | `load_model()` | Restore the declared CNN and validate its metadata |
| Raw pixels divided by `255`, forward pass and category selection | `Predictor.predict()` | Consistent preparation and identified suggestions |
| CSV/image reading, prediction and complete output | `predict_batch()` | Deliver a complete batch with model/input evidence |

After tracing these operations in source, you can use the project function to assemble another delivery without rewriting its packaging logic. This code is a project integration example using the already-trained model.

```python
# Project assembly
from pathlib import Path
from catalog_mlops.inference import predict_batch

report = predict_batch(
    run_directory=Path("work/runs/baseline"),
    manifest_path=Path("work/intake/manifest.csv"),
    output=Path("work/batches/project-assembly"),
)
print(report["count"], report["model"])
```

Expect `20` delivered predictions and the same model hash as the earlier batch. Use a new output directory for this actual execution. Be able to point from the function to its preparation, model call and output-writing code. The helper assembles operations whose behavior you have already inspected.

# Watch out for

Wait for data preparation before training. Keep validation labels outside weight updates. Avoid dividing by `255` twice or treating a softmax score as established reliability. Restart a service or notebook kernel after editing imported source. An existing output path preserves evidence and requires inspection or a deliberately new destination.

# Quick reference

| Operation | Entry point | Evidence |
|---|---|---|
| Verify data | `catalog-mlops prepare` | File identities and split counts |
| Learn weights | `catalog-mlops train` | Completed baseline run |
| Reload/evaluate | `catalog-mlops evaluate` | Metrics on fixed validation IDs |
| Deliver many predictions | `catalog-mlops batch` | CSV and batch identity record |
| Deliver one response | `catalog-mlops serve` and `request` | Actual HTTP prediction and loaded model identity |

## Learning outcome

Trace how data moves through the provided training/inference pipeline scaffold from raw input to served prediction, and label each stage's purpose.

## Summary

Threadline now has a baseline whose mistakes can be inspected and whose saved weights work through both inference routes. Your stage trace connects the image files, preprocessing, learning, evaluation and delivered prediction. A supplier requirement can now be added at a specific boundary and tested against that working route.
