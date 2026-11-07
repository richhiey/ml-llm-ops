✂️
# Autologging and reducing manual tracking overhead

Threadline's pipeline currently records each learning observation explicitly. The team wants less repeated instrumentation, while retaining the evidence needed to trust a comparison. You will configure real autologging and check exactly what it captures.

Use the same baseline training recipe and frozen source. This is an instrumentation repeat, not a sixth improvement candidate.

# What this autologging path can observe

The CNN is a plain PyTorch `nn.Module`. In pinned MLflow `3.5.1`, its PyTorch autologging hook can capture scalar events written through TensorBoard. It does not discover this custom training loop's data split or automatically infer every project artifact.

The relevant configuration in the [tracking source](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/tracking.py) is:

```python
mlflow.pytorch.autolog(log_every_n_step=1, log_models=False, checkpoint=False)
```

`log_every_n_step=1` enables scalar capture for the declared steps. The adapter writes each epoch observation with `SummaryWriter.add_scalar()`, and the MLflow hook records it under `auto/`. A final `add_hparams()` event captures the `autolog_hook=tensorboard` proof parameter and flushes the scalar queue before completion. The training algorithm stays the same.

Final decision metrics, data/source identities, recipe artifacts and the verified native model are still logged explicitly. Autologging reduces repeated scalar plumbing; explicit logging keeps control over project-specific evidence. The [installed-version documentation](https://mlflow.org/docs/3.5.1/ml/deep-learning/pytorch/guide/) provides broader PyTorch integration context; the [versioned hook source](https://github.com/mlflow/mlflow/blob/v3.5.1/mlflow/pytorch/__init__.py) documents TensorBoard scalar/hyperparameter capture. This is narrower than automatically instrumenting a complete vanilla-PyTorch training loop.

# Your task

Configure the project's autologging option for a baseline repeat. Choose a new output destination and retain its receipt. Use this documented execution after tracing the option into the source configuration above.

```bash
python scripts/track_experiment.py --config configs/baseline.json --output work/experiments/baseline-autolog --state work/mlflow --name baseline-autolog --autolog
```

Compare its native MLflow record with the manually instrumented baseline. Verify `auto/train_loss`, `auto/validation_loss`, `auto/validation_accuracy` and `auto/validation_macro_f1` all contain steps `1–4`. Verify the proof parameter and distinguish automatically captured fields from explicitly logged fields.

Use the UI and a raw client inspection. In the optional [companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb), `MlflowClient.get_metric_history()` reads the events directly. Explain why the presence of only a final metric would not prove autologging worked.

Retain `work/autologging-check.md`: configuration used, captured keys/steps, one native history inspection, final-metric comparison, what remains explicit and a reason to keep or change this balance. TensorBoard scalar events use float32 values, so tiny differences from retained full-precision epoch values can be representation differences. Rank configurations using the explicit final decision metric.

# Hints

<details><summary>Hint 1</summary>

The successful repeat should have the same configuration, split and final macro F1 as its baseline under the same deterministic environment. Its automatic scalar keys are different from the manual baseline's `manual/` keys.

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

Threadline has evidence that autologging captures the intended learning observations. Your configuration preserves explicit control of lineage, final metrics and model artifacts while reducing repeated epoch instrumentation.
