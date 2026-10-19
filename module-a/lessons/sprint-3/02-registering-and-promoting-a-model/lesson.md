📝
# Registering and promoting a model

Linden Facilities has selected a guarded run. We will give its artifact a registered version, attach validation evidence and make it the version used by the next batch.

**Continue here:** [Sprint 3 · continue in the same notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=register-pending). Keep your code and answers in the same sprint notebook. [Local setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md).

## Follow the artifact into active selection

Use **Register a pending artifact**, **Observe the pending boundary** and **Validate the observed behavior and select** in the sprint notebook. A model version is a named registry record; `active` is a mutable alias pointing to one version.

1. **Register the fitted artifact.** The notebook logs a guarded run and registers its model URI. Keep the returned run ID, model URI and version. Expect `validation_status=pending`; registration alone does not select it.
2. **Probe the boundary.** Try to activate the pending version. Expect a deliberate rejection. This is the course helper's policy: MLflow tags and aliases do not enforce approval by themselves.
3. **Validate, then approve.** Inspect valid-copy and invalid-hour probes and the finite held-out RMSE. The helper requires guard enabled and validation RMSE at most `5` kWh, plus a reason. It records approval but does not run your tests for you.
4. **Select and inspect the next batch.** Assign `active` using the returned version and a reason. Verify the registered version's source run matches the training run and the next batch's resolved version. An alias assignment changes future resolution; it does not prove every already-running consumer reloaded.

## Watch out for

Version counters are local to a registered model/store. Reuse actual returned identities. The helper's JSONL event records old/new selection, time, source run and reason; it is mutable and its update is not atomic with the alias change.

## Quick reference

| Operation | Effect |
|---|---|
| `register` | Create a pending version |
| `approve` | Check the teaching gate and record rationale |
| `activate` | Reassign `active` and append a helper event |
| `batch_predict` | Resolve `active` once for the job |

## Check your result

Explain the difference between “registered,” “approved” and “selected.” Point to the run → version → batch chain and the rejected pending-selection output in your notebook.

![Registering and promoting a model: evidence path](assets/registering-and-promoting-a-model__01__en.png)

## Learning outcome

Use the provided model registry scaffold to register a new model version, record its validation status with tags, and promote it by assigning the scaffold's active-model alias.

## Summary

The candidate has moved from a logged artifact to a tagged version and a verified active batch. Each lifecycle action now points back to the same source run.
