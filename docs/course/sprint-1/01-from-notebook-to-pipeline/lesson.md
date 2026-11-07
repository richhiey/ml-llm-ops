🏷
# From notebook to pipeline

Threadline Retail's fashion specialists review product categories before items enter the catalog. They have labeled examples of ten kinds of clothing, footwear and bags. The engineering team wants to investigate whether images can support useful category suggestions.

A notebook experiment might show that a model recognizes a shirt. The catalog team needs to know where that image came from, how it was prepared, which learned model produced the answer and whether the same process works for the next supplier batch. A pipeline makes those operations explicit and connects their inputs and outputs.

# Follow one product through five stages

Fashion-MNIST supplies small front-view product thumbnails with reviewed category labels. A **label** is the known category used to teach and evaluate the classifier. The course uses those research images in a fictional catalog operation. The images are already prepared as `28×28` grayscale thumbnails. [Dataset card](https://github.com/richhiey/ml-llm-ops/blob/main/docs/dataset-card.md)

| Stage | What happens at Threadline | Evidence to inspect |
|---|---|---|
| Ingestion | Load verified image and label files, then select recorded sample indices. | Original file hashes and the split manifest |
| Preprocessing | Convert raw integer pixels into the numeric shape and scale expected by the CNN. | Input/output shapes, dtype and pixel values |
| Training | Use labeled training images to adjust the CNN's weights. | Configuration, learning history and saved weights |
| Evaluation | Compare predictions with known labels on separate validation images. | Predictions, metrics and confusion matrix |
| Inference | Load the saved model and suggest categories for incoming thumbnails. | Identified predictions and the model actually loaded |

A **CNN**, or convolutional neural network, learns image patterns using small filters that move across the image. Early filters can respond to local edges. Later layers combine those responses to produce a score for each category. Training adjusts the filters and classification weights using examples.

At ingestion, an image might be identified as `train:56368`. That identifier means an index in the original research training file. Its known label can be used during training or evaluation. Incoming catalog images have their own identifiers and need predictions without supplying a category to the model.

# Two routes share the same preparation

The training route contains labeled examples and updates model weights. The inference route loads the resulting weights and produces predictions. New catalog images pass through ingestion and preprocessing, then go to the saved model. They do not need to pass through training again.

**Preprocessing** changes the representation of the input. Here, raw pixels use unsigned 8-bit integers, `uint8`, with values from `0` to `255`. The shared function creates a channel dimension and produces `float32` tensors with values from `0.0` to `1.0`. A **tensor** is the multidimensional numeric array used by the neural network.

The CNN was trained to interpret that scale. If a supplier image is scaled differently during inference, the weights receive a different kind of input. Giving each image its own maximum value of `1.0` would change the contrast relationship the model learned.

# A metric needs a result it can be traced to

A **validation set** contains labeled images kept separate from training. It helps the engineers see whether the learned patterns work on other examples. The CPU profile has `12,000` training images and `3,000` validation images with recorded, disjoint indices. The official test split is reserved for reporting after model selection.

Accuracy is the fraction classified correctly. Per-category recall asks how many examples of a category were found. A **confusion matrix** shows the actual category against the predicted category, exposing mistakes such as shirts classified as coats. These observations help the catalog team decide what to investigate next.

The team retains more than a score. A saved run connects the model to its configuration, dataset, split, source code, environment and predictions. Another engineer can inspect that record without depending on the original notebook's hidden variables.

A **reproducible run** provides retrievable code, data, split, configuration and environment so another engineer can repeat its evaluation within a declared tolerance. Hidden notebook state prevents that engineer from knowing which steps and values produced the result. Recording the recipe begins here, while later operational work will verify a clean replay.

# Check for Understanding

A colleague has a screenshot showing `84%` accuracy and a file named `best-model.pt`. They now want to run tomorrow's supplier thumbnails through the classifier. Draw the route from those images to identified predictions. Mark the information that must be retrieved or verified before the screenshot can support using that model.

<details>
<summary>Solution</summary>

**Result you should get**

Your route should include incoming image identities, the expected image contract, shared preprocessing, a known saved model and identified output predictions. Your evidence list should connect the screenshot's metric to a dataset/split, evaluation procedure and the exact model artifact.

**How**

Trace ingestion → preprocessing → inference for the new images. Trace the saved artifact backward to training and evaluation records. A plausible filename cannot establish that the file is the model that achieved the displayed score. Re-running training would create a new observation requiring its own evidence.

</details>

## Learning outcome

Explain why a reproducible training/inference pipeline replaces a one-off notebook workflow, and identify the 5 stages a production ML pipeline must cover - ingestion, preprocessing, training, evaluation, inference.

## Summary

Threadline's prototype has a traceable route from labeled product images to a learned model and from incoming images to category suggestions. The scaffold will make each stage visible so you can inspect its actual data, code and outputs.
