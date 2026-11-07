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

The process pins one saved model at startup. In this starting route, selecting another run requires a new process. The registry consumer below resolves its selected version once at startup too. Batch and single-request top scores can differ by small floating-point roundoff, so compare class equality and score difference at most `1e-6`.

## Registry selection and replay

A numbered version connects the native logged model to its source run. Registration begins pending. The reviewed validation operation recomputes the declared replay checks, retains the report on that run and records its evidence address and fingerprint as version tags. `validation_scope=clean-cpu-replay-v1` establishes replay consistency; the applicable business brief determines suitability separately.

The reviewed alias operation requires passed retained evidence and the expected current version. It reads the result back and records actor, reason, time and operation status. Native MLflow changes can bypass this local path. The journal is mutable local evidence, not a complete immutable history of outside actions.

A registry batch or service resolves the alias once and loads that exact native version. Existing processes remain pinned after an alias reassignment; a newly started consumer must report the restored version, run and model identity. [Declared replay checks](https://github.com/richhiey/ml-llm-ops/blob/main/docs/reproducibility.md)

## Incoming-image observations

Batch delivery retains each consumed PNG fingerprint and mean brightness from the same bytes used for prediction. Monitoring reads each published batch/prediction file once and verifies those captured bytes. It summarizes mean brightness per thumbnail in ten `0–1` ranges and counts predicted categories.

Without known labels, no accuracy or macro F1 is reported. Supplied labels must cover exactly the delivered identifiers. A same-model cohort comparison keeps model and inference source fixed; a paired model-quality comparison instead requires identical ordered input bytes and labels, with fixed inference source.

Brightness total variation `0.20` and macro-F1 drop `0.05` are declared exercise investigation thresholds. They do not detect every input change or replace category-specific business requirements. The public reference CSVs are compact exports from actual observations, not substitutes for a learner's own store and execution evidence.
