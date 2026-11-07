# Pipeline contracts

## Dataset and preprocessing

Original compressed IDX files must match the SHA256 values in `data.py`. The split manifest records exact official-training indices. Training uses only `train`. Validation uses only `validation`. Other partitions support later operational work and the official test split is reserved until selection.

`validate_images()` accepts a nonempty NumPy array of uint8 grayscale images with shape `(N, 28, 28)`. It preserves the caller's array. `preprocess()` produces float32 tensors with shape `(N, 1, 28, 28)`, with pixel `255` mapped to `1.0` and pixel `0` to `0.0`. Evaluation and training use the same `normalize_pixels()` implementation. Neither inference route rescales each image by its own maximum.

An image-quality policy is a separate bounded extension. The guided supplier policy requires pixel range of at least `20` within each accepted thumbnail. This checks for low-information intake under the exercise brief. It does not detect every photographic defect or establish category correctness. The starter intentionally has only its structural boundary. Learners add and test the new policy through the ordinary application route.

## Saved run

The model artifact declares architecture, class order and preprocessing version. `verify_run()` checks the retained recipe, model, metrics, predictions, learning history, environment and source archive identities before a consumer loads it. A new run uses a new output directory. Incomplete jobs do not publish a complete run directory.

`training_source_sha256` identifies the archived training code. `inference_source_sha256` identifies the source present when the consumer starts. These can differ after an intake extension. Restart a Python process after editing source so the imported functions correspond to that source revision.

## Batch input and output

A UTF-8 CSV contains exactly `image_id,path` in that order. Identifiers are nonempty and unique. Relative image paths are resolved against the manifest's directory. PNG images must use mode `L` and size `28×28`.

Successful delivery publishes a new directory with `predictions.csv` and `batch.json`. Prediction rows preserve input order and identifiers. Fields are `image_id`, `class_id`, `class_name` and `top_score`. The record identifies the model, consumed manifest/image hashes, count, output hash and elapsed seconds. A failed job leaves its requested output directory absent.

## HTTP request and response

`POST /predict` receives JSON containing `image_id` and `pixels`, a list of 28 rows of 28 integer pixels in `[0,255]`. Floats and out-of-range values are rejected before conversion to uint8. Success returns the prediction, model identity and service-side `inference_seconds`. Invalid input returns HTTP `422`. `GET /health` reports the loaded model identity.

The process pins one saved model at startup. In this starting route, selecting another run requires a new process. Later registry work will make the resolution/reload boundary explicit. Batch and single-request top scores can differ by small floating-point roundoff, so compare class equality and score difference at most `1e-6`.
