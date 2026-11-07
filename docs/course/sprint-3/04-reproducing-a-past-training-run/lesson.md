✂️
# Reproducing a past training run

Threadline's catalog team wants to inspect the weight-decay experiment again. Its original result is already recorded in MLflow, but the engineer who trained it is unavailable. Your task is to recover that particular recipe and establish whether it can be repeated, rather than training today's code and hoping for a similar score.

Start with the full **weight-decay run ID from your own experiment ledger** and its native model. If you already used that exact run for the guided replay, select another completed candidate and record the choice. Use the declared [clean-state verification specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/reproducibility.md). Investigate a different past run from the one you replayed in the guided work; the author reference uses weight decay. Keep Threadline's currently selected alias in place while doing this investigation.

# Your task

Create a fresh `work/replay-weight-decay` attempt containing the retrieved original recipe, extracted source, new environment, independently trained output, both evaluations and the verification report. Confirm that this destination and its replay environment did not exist before starting. Native download, extraction and shell redirection can overwrite earlier files, so retain previous attempts separately.

Use the demonstrated native artifact retrieval and archived entry files. Run saved-model evaluation and independent training inside the extracted source's environment. Retain its interpreter/import paths and command outputs. Record the original source, data, split, full configuration, environment and model identities before interpreting score differences.

Register the past model under a separate name, `threadline-replay-check`, and connect its version to the original MLflow run and native model address. After the replay checks pass, record its validation evidence with tags. You are checking a historical candidate; do not assign this name or version to Threadline's main `active` alias.

Produce a concise `work/replay-weight-decay/replay-note.md` stating:

- which original run and registered artifact you recovered;
- how the actual archived code and new environment were used;
- whether each required identity matches and what the observed metric differences are;
- how saved-weight evaluation differs from training again;
- whether the declared tolerance is satisfied, with recorded file paths locating your retained evidence.

In the note, use real observations from your execution. A failure with a precise diagnosis is more informative than changing the specification until a result passes.

# Check that the report can reject an incorrect claim

After retaining the original evaluations and report, make a separate copy of the repeated-evaluation JSON. Deliberately increase its reported macro F1 by `0.01`. Verify that altered copy against the same raw run into a new report destination.

Keep the original passed evidence untouched. Explain which consistency checks reject the altered claim and why copying a desired metric into JSON cannot establish reproduction. Do not weaken the tolerance or edit raw predictions to make the altered report pass.

# Working with documentation

| Need | Inspect |
|---|---|
| Retrieve the original files | Native `mlflow artifacts download --help` and your original run's artifacts |
| Identify the actual archived entry points | Extracted `scripts/prepare_data.py`, `train.py` and `evaluate.py` |
| Interpret a failed condition | [Declared replay checks](https://github.com/richhiey/ml-llm-ops/blob/main/docs/reproducibility.md) |
| Connect the model and evidence | [Registry implementation](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/registry.py) and `inspect_registry.py --help` |

# Hints

<details><summary>Hint 1</summary>

Follow the original run's recipe, not a configuration file with a similar name in today's checkout. Match its native model address to the registered version's source run.

</details>

<details><summary>Hint 2</summary>

Use a separate terminal for the extracted code's environment. The current project terminal remains available for registry inspection and verification. A second directory pointing at the original saved checkpoint is not a new training execution.

</details>

<details><summary>Hint 3</summary>

Check identities before comparing scores. The verifier writes failed checks as evidence when the artifacts are readable but their declared conditions disagree. A damaged or missing artifact can instead stop verification with an error; preserve and diagnose that output.

</details>

# Checkpoints

The two evaluations must refer to the intended original and repeated models, using the same validation identities. The repeated output needs its own training record. Exact learned weights can pass when training genuinely ran again.

The registered version must identify the original native MLflow run and retained validation evidence. Confirm that Threadline's main alias has not moved. Keep official-test data outside this investigation.

Only after completing your own attempt, open the reference feedback.

<details>
<summary>Reference feedback</summary>

**Result you should get**

A defensible result retrieves the weight-decay recipe, establishes the fresh execution conditions and checks the declared identities before accepting the numerical replay. In the author's independent replay, the recorded configuration reached accuracy `0.8400` and macro F1 `0.8337648911681302`. Use those as reference observations, not as a substitute for your files. A different result requires explanation under the same specification.

The deliberately altered evaluation must fail. It disagrees with both the independently trained run record and the scores recomputed from its raw predictions.

**How**

Trace your chosen MLflow run → retained recipe and native model → registered version. Retrieve and extract the original source, create its environment, prepare data, evaluate the saved model, train into a new destination and evaluate that new model. Use the current verifier to compare the retained outputs. If a field fails, investigate that field rather than relying on the rounded score. Preserve the actual input/output and execution evidence so another engineer can check your reasoning.

</details>

## Learning outcome

Given a past experiment logged in MLflow, use its recorded code, data, configuration, environment, and registry lineage to reproduce the evaluation result within the tolerance declared in the clean-state verification specification.

## Summary

Threadline can recover a particular historical candidate and distinguish a genuine independent replay from a reused file or edited result. Its evidence connects the model back to the conditions that produced it.
