# Clean-state verification specification

This specification is declared before a replay. It checks a past Fashion-MNIST run on the same declared CPU environment. A matching score alone is insufficient.

| Check | Acceptance |
|---|---|
| Code | Extract and execute the original run's `source.zip`; its source fingerprint must match |
| Data | Verified original image/label bytes, category order and exact recorded split |
| Recipe | Same configuration and initial weight values; start training from scratch |
| Environment | Same recorded Python, platform, architecture and package versions; create a fresh `.venv` from the archived lock |
| Original model | Native MLflow model belongs to the recorded run and has the evaluated checkpoint's learned weight values |
| Saved-model evaluation | Accuracy and macro F1 agree with raw predictions, retained results and MLflow within absolute `1e-12` |
| Independent training | Separate output directory and training record, different execution timestamp, separate evaluation files; copying the original run does not qualify |
| Repeated evaluation | Accuracy and macro F1 each differ from the original by at most absolute `0.002` on the same validation images |

`0.002` is **0.2 percentage points** on the `0–1` scale. These are course acceptance tolerances, not universal guarantees. The author observed exact agreement on the declared machine. Another operating system or processor can fail the environment check even when scores are close; report that as a portability observation, not a passed same-environment replay.

A newly trained checkpoint file may have a different byte fingerprint even when its learned numbers are identical. The report therefore records the repeated artifact separately and also reports whether the learned weight values match exactly. Exact learned weights are permitted; a copied original execution record is not.

## Keep execution evidence alongside the report

Retain the fresh folder, interpreter path, package import path and command outputs showing preparation, saved-model evaluation, new training and repeated evaluation. The verifier checks recorded artifacts; it cannot establish from files alone that a learner actually created a clean process or environment.

The archived code contains the preparation, training and evaluation entry files that produced the run. Current registry inspection files are separate tools; do not copy them into the old archive and then claim the source remained identical. Keep the original recipe alongside the independently trained output.

## Connect validation to a retrievable model

`verify_reproduction.py` writes the observed checks and input identities. `validate_model.py` recomputes them, retains the report on the original MLflow run under `registry-validation/<report SHA>.json`, checks its downloaded bytes and tags the registered model version with that evidence address and fingerprint.

`validation_scope=clean-cpu-replay-v1` means these replay checks passed. Suitability for a catalog brief is a separate decision based on the original controlled comparison and its business requirements. Threadline's equal-category rule and Morrow's category recall requirements can select different models.

The reviewed alias-selection command requires passed validation, retained matching evidence, the expected current version and the evaluated model identity. MLflow's native tag and alias APIs do not enforce this course policy automatically. The local journal records these command operations; outside changes and mutable local files need separate evidence.

## Keep the final test set for reporting

Use validation images for the configuration study. Once selection is fixed and the approved model is loaded, `evaluate_holdout.py` reports its official-test result without training or changing that choice. Retain this as final reporting evidence, rather than using it to rank more candidates.
