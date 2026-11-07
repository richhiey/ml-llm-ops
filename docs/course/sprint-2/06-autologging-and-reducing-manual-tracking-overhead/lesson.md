✂️
# Autologging and reducing manual tracking overhead

At the end of an **epoch**, one pass through the training examples, Threadline's code has a **loss** value measuring disagreement with the known labels. That number needs to be recorded. Repeating that recording work for every measurement can become easy to overlook as the pipeline grows. The team wants the training tool and MLflow to handle more of it automatically, while keeping its final model-selection evidence complete.

You will repeat the baseline, the reference training recipe, using the same settings and unchanged Python code. The purpose of this repeat is to check how measurements are recorded. It adds evidence about logging without adding a new model-improvement configuration.

# What this autologging path can observe

**Autologging** means a tool integration automatically records supported information as the work happens. Here, **TensorBoard** is the training tool used to write messages containing measurements. A **scalar** is one number, such as the loss after an epoch. The project's callback, a function called after each epoch, sends these numbers through TensorBoard's `SummaryWriter`.

MLflow's integration listens for those messages and copies their values into the run's metric histories. This listening integration is called a **hook**. The history shows both the number and the epoch at which it was observed.

The project uses this configuration in its tracking source. [Tracking implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/tracking.py)

```python
mlflow.pytorch.autolog(log_every_n_step=1, log_models=False, checkpoint=False)
```

`log_every_n_step=1` enables capture at each declared step. In this pipeline, the step is the epoch number. The callback writes each observation with `SummaryWriter.add_scalar()`, and MLflow records it under `auto/`. This gives you a concrete check that automatic recording worked.

The code still explicitly records the final decision metric, which examples and source code were used, the recipe files and the saved model. TensorBoard's measurement messages do not identify every file this project needs. Automatic capture reduces repeated recording work, while explicit calls let the team choose the evidence required for its decision.

<details>
<summary>Optional implementation detail — supported capture and numeric precision</summary>

The CNN is a PyTorch `nn.Module`, the class used for the model definition. With this custom training loop, the installed MLflow `3.5.1` integration captures supported TensorBoard scalar and hyperparameter messages. Hyperparameters are training settings chosen before learning begins. The integration does not discover the whole training procedure or its dataset split.

A final `add_hparams()` call writes the proof parameter `autolog_hook=tensorboard` and causes queued scalar messages to be sent to MLflow before completion. A queue holds messages waiting to be recorded. Checking the final history immediately matters because closing the TensorBoard writer alone does not flush MLflow's separate queue.

TensorBoard's scalar messages use `float32`, a numeric representation with fewer decimal digits than the retained Python values. Tiny differences can therefore come from representation. Use the explicitly logged final metric to rank models, and compare captured history values with the documented representation.

For the broader supported integration, consult the installed-version guide. To inspect the exact TensorBoard capture behavior, follow the versioned hook implementation. [MLflow PyTorch guide](https://mlflow.org/docs/3.5.1/ml/deep-learning/pytorch/guide/) · [MLflow 3.5.1 hook source](https://github.com/mlflow/mlflow/blob/v3.5.1/mlflow/pytorch/__init__.py)

</details>

# Your task

Configure the project's autologging option for a baseline repeat. Choose a new output destination and retain its receipt, the saved record connecting that result to its MLflow run. Use this documented execution after tracing the option into the source configuration above.

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline-autolog --state work/mlflow --name baseline-autolog --autolog
```

Compare its MLflow record with the baseline whose measurements were logged directly. Verify `auto/train_loss`, `auto/validation_loss`, `auto/validation_accuracy` and `auto/validation_macro_f1` all contain steps `1–4`. Verify `autolog_hook=tensorboard`, the parameter captured through the integration. Distinguish automatically captured fields from explicitly logged fields.

Use the browser interface and inspect the stored values through `MlflowClient`, MLflow's Python interface for retrieving run records. In the optional [companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb), `MlflowClient.get_metric_history()` reads the values and their steps directly. Explain why the presence of only a final metric would not prove autologging worked.

In `work/autologging-check.md`, retain the configuration used, captured names and steps, one history inspection, the final-metric comparison, what remains explicit and a reason to keep or change this balance. Rank configurations using the explicit final validation macro F1, which averages the ten category F1 scores equally.

# Hints

<details><summary>Hint 1</summary>

The successful repeat should have the same configuration, image split and final macro F1 as its baseline in the same recorded environment. Each run creates a new model, and the fixed seed repeats its starting weights. The automatic measurement names begin with `auto/`, while the direct-logging baseline uses `manual/`.

</details>

<details><summary>Hint 2</summary>

Inspect what creates the data identity, saves the checkpoint and logs the final metric. Those project responsibilities do not become automatic because a scalar hook is enabled.

</details>

# Checkpoints

Check every expected metric and step, not only training loss. Make sure the run is finished and its model reload was verified. Preserve the two actual run IDs. Do not count a repeated configuration as another improvement experiment.

<details>
<summary>Reference feedback</summary>

**Result you should get**

The author's autologging repeat `5673c459ef284ea4904a9d42d38d8e7e` captured all four automatic histories at steps `1–4`, recorded `autolog_hook=tensorboard` and retained the same final macro F1 `0.8322013435739599` as the manual baseline. Explicit source/data/artifact logging remained present.

**How**

Follow the enabled PyTorch hook into TensorBoard scalar emission and inspect the client histories. Compare fields against the manual baseline, then identify what is still recorded explicitly. Fewer manual calls are useful only if the evidence required for your decision remains visible and complete.

</details>

## Learning outcome

Configure autologging for the pipeline and explain the tradeoff between autologging convenience and control over what gets logged.

## Summary

Threadline has evidence that autologging captures the intended learning observations. Your configuration keeps the final decision metric, saved model and retrievable recipe under explicit control, while the integration records the emitted epoch measurements.
