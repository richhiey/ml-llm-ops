📝
# Reading the provided pipeline scaffold

Threadline's catalog team wants a first working classifier and a clear account of its mistakes. You will train a small CNN, inspect where it struggles and use its saved weights to suggest categories for incoming thumbnails.

Work in one local clone in VS Code. Your end result is a trained baseline, evaluation evidence, a batch CSV and an HTTP prediction from the same model. The [README](https://github.com/richhiey/ml-llm-ops/blob/main/README.md) repeats this exact command sequence, including the two-terminal service step. The [setup guide](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md) covers installation and recovery.

Run the commands below. Short Python excerpts explain the ML operations inside the supplied files; you do not need to copy those excerpts into a second implementation. The [companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) provides the complete native-package implementation for closer inspection.

# 1. What images are we learning from?

Get the repository and install its locked environment.

```bash
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --frozen
source .venv/bin/activate
python scripts/prepare_data.py
python scripts/inspect_dataset.py
```

`uv sync --frozen` installs the locked environment once. Activate `.venv` once in each terminal, then run the tools directly. On Windows, use the activation command in the [setup guide](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md). `python` executes the named file, which you can open in your editor. Preparation downloads and verifies Fashion-MNIST, then records fixed image indices. Inspection reads the image arrays with NumPy and plots examples with Matplotlib.

Expect the original array to have shape `(60000, 28, 28)` and dtype `uint8`. The bounded CPU profile uses `12,000` training images and `3,000` separate validation images: `1200` and `300` per category respectively. The official test split stays reserved for reporting after model selection.

Open `work/training-examples.png`. Choose two categories you expect the model to confuse and explain what makes their silhouettes similar.

![One actual training example from each category, with its original image identifier](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/fashion-mnist-examples__01__en.png)

The script's [visible data-reading implementation](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/inspect_dataset.py) is available if you want to inspect the file format. Understanding binary headers is not required for this task.

# 2. What does the CNN receive?

A raw thumbnail contains integer brightness values from `0` to `255`. PyTorch needs a floating-point tensor, with a channel dimension for grayscale. Inside the supplied preprocessing, the key conversion is:

```python
inputs = raw_images.to(dtype=torch.float32) / 255.0
```

Here, `raw_images` is an existing batch shaped `(N, 1, 28, 28)`. A raw pixel of `128` becomes approximately `0.502`. Training and inference must use that same scale. Scaling each image by its own brightest pixel would change what its numbers mean.

The CNN learns small filters that respond to image patterns. Two convolution-and-pooling blocks turn local patterns into features, and a classifier produces ten raw category scores, called **logits**.

| Point in the CNN | Shape for one image |
|---|---|
| Prepared input | `1 × 28 × 28` |
| First convolution and pooling | `16 × 14 × 14` |
| Second convolution and pooling | `32 × 7 × 7` |
| Flattened features | `1568` values |
| Hidden classifier layer | `32` values |
| Output | `10` category scores |

Open [model.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/model.py). Locate `nn.Conv2d`, `nn.MaxPool2d` and the final `nn.Linear`. Match them to this table. You are tracing the supplied architecture; you do not need to rewrite it.

# 3. How does the model learn?

Inspect `configs/baseline.json`. It specifies four **epochs**—four passes through the training examples—a batch size of `64`, learning rate `0.001` and seed `426`. The learning rate controls the size of weight updates.

```bash
python scripts/train.py --config configs/baseline.json --output work/runs/baseline
```

The script starts with fresh CNN weights. It uses PyTorch's Adam optimizer. The essential update, inside the existing batch loop, is:

```python
optimizer.zero_grad(set_to_none=True)
logits = model(inputs)
loss = nn.functional.cross_entropy(logits, known_labels)
loss.backward()
optimizer.step()
```

The loss measures disagreement with the known labels. `backward()` computes how weights contributed to that loss; `step()` updates them. Clearing gradients prevents an earlier batch's gradients from accumulating accidentally. Validation makes predictions without updating weights.

Expect four epoch observations and a completed `work/runs/baseline` directory. Keep that directory. An existing output is protected; inspect it rather than deleting it to rerun the same command.

# 4. Where does the baseline struggle?

Reload the saved model, evaluate it on the fixed validation images and inspect its results.

```bash
python scripts/evaluate.py --run work/runs/baseline
python scripts/inspect_results.py --run work/runs/baseline
```

The first script evaluates the saved weights. The second recomputes metrics from the retained prediction CSV and draws your own plots. Expect `3000` predictions. The author's reference run reached accuracy `0.8380` and macro F1 `0.8322`; inspect your own result rather than treating those numbers as a guarantee across computers.

**Accuracy** is the fraction classified correctly. **Recall** asks how many actual examples of a category were found; **precision** asks how many predictions of that category were correct. F1 combines precision and recall. **Macro F1** averages the ten category F1 scores equally, matching Threadline's equal-category priority.

![Observed training and validation loss over four epochs in the author's baseline](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/baseline-learning-history__01__en.png)

Open `work/learning-history.png`. Training loss comes from images used to update weights. Validation loss comes from separate images. Describe how both change; four epochs alone cannot establish what a longer run would achieve.

![Actual categories on rows and predicted categories on columns for the author's validation results](https://raw.githubusercontent.com/richhiey/ml-llm-ops/main/docs/course/figures/baseline-confusion-matrix__01__en.png)

Open `work/confusion-matrix.png`. Follow the actual-shirt row across the predictions. The reference found `117` of `300` shirts: recall `0.39`. It called `73` shirts coats and `70` T-shirts/tops. This is a concrete weakness that overall accuracy conceals. Identify the largest error in your own matrix.

# 5. What connects the score to a usable model?

Inspect these files in `work/runs/baseline`.

| Artifact | What it lets you check |
|---|---|
| `config.json`, `history.json` | Training settings and learning observations |
| `dataset.json` | Data identities, class order and fixed split indices |
| `model.pt` | Saved learned weights |
| `metrics.json`, `validation-predictions.csv` | Scores and the predictions behind them |
| `source.zip`, `environment.json`, `run.json` | Code, environment and connected artifact identities |

A **hash** is a content fingerprint used here to detect mismatched files. The run record contains the saved model's fingerprint; the consumers below report that same model identity. Retain the files as well as their hashes so another engineer can retrieve the recipe.

This is a useful stopping point. You can close your editor and resume from the saved model without training again.

# 6. Can the saved model process an incoming batch?

Export a small unlabeled intake from the separate incoming-image pool and run prediction.

```bash
python scripts/export_samples.py --count 20 --output work/intake
python scripts/predict_batch.py --run work/runs/baseline --manifest work/intake/manifest.csv --output work/batches/baseline
```

Expect `20` rows in `work/batches/baseline/predictions.csv`, plus `batch.json`. Match identifiers and order to the intake manifest. Each result contains a category and a top softmax score. **Softmax** turns logits into normalized scores; its largest value is not a calibrated guarantee of correctness.

Open [inference.py](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/inference.py). Trace the image read, shared preprocessing, saved-model call and output row. Incoming images supply no category label.

# 7. Can a client request one prediction?

In a **second terminal**, at the repository root, start the actual web server.

```bash
source .venv/bin/activate
uvicorn scripts.api:app --host 127.0.0.1 --port 8000
```

Uvicorn loads the FastAPI application declared in [scripts/api.py](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/api.py). That file explicitly selects `work/runs/baseline`. Wait for startup to complete and keep the terminal running.

Back in the **first terminal**, prepare the request body and send it using `curl`.

```bash
python scripts/prepare_request.py --image work/intake/56368.png --image-id train:56368 --output work/intake/request.json
curl --fail-with-body -sS -H "Content-Type: application/json" --data-binary @work/intake/request.json http://127.0.0.1:8000/predict
```

The [request preparation file](https://github.com/richhiey/ml-llm-ops/blob/main/scripts/prepare_request.py) reads the PNG with Pillow and writes its identifier and pixel array as JSON. Open `request.json`: these are the values the client sends. `curl` performs the HTTP request directly. In Windows PowerShell, use `curl.exe` for this command.

Expect a prediction, loaded model identity and service-side processing time. Match the class to `train:56368` in your batch CSV. The model hashes must agree; top scores should agree within `1e-6` for floating-point roundoff. Stop Uvicorn with `Ctrl+C` in the second terminal.

# Quick reference

Complete an annotated route from raw image to served suggestion. For each of the five stages, name its purpose, input, output, actual source function and one observed artifact. Trace one training identifier and one incoming identifier; mark where the saved weights connect the routes.

| Underlying package operation | Project code that assembles it |
|---|---|
| NumPy reads and selects image arrays | `data.py` verifies files and records splits |
| PyTorch converts tensors, learns weights and predicts | `preprocessing.py`, `model.py` and `training.py` connect those operations |
| scikit-learn calculates evaluation metrics | `evaluation.py` reports fixed-split results |
| FastAPI receives a request; Uvicorn runs the server | `service.py` connects validated input to the saved classifier |

Project functions save repeated assembly work. The package operations above explain what those functions do. Use the linked source and notebook when you need implementation detail.

# Watch out for

Wait for preparation before training. Keep validation labels outside weight updates. Use the same pixel scale in training and inference. Restart the server after source changes. Keep completed outputs and choose a new destination for a deliberately new run.

## Learning outcome

Trace how data moves through the provided training/inference pipeline scaffold from raw input to served prediction, and label each stage's purpose.

## Summary

Threadline has a baseline with visible weaknesses and saved weights that work through batch and HTTP delivery. Your stage trace connects the images, preparation, learning, evaluation and category suggestion. You can now add a supplier intake rule at a specific boundary and check its effect.
