# Verified behavior — 19 October 2026

The checked source is identified in [verification.json](verification.json) and [the notebook pin](../notebooks/helper-pin.json). Observations below came from execution on macOS ARM64 / Python 3.12.13.

- All **6 helper tests passed**. They cover stage contracts, controlled comparisons, tracking, registry selection, inference and reproduction, plus repeated-configuration rejection, changed transitive environment rejection, autolog cleanup after failure and rejection of final/nonfinite approval metrics. MLflow emitted 3 integer-schema warnings; missing inputs are rejected before prediction.
- All **4 notebooks / 20 code cells** executed in separate fresh local kernels with no errors.
- A new seeded Python environment cloned the pinned source from GitHub, installed exported runtime requirements, and executed every setup/exercise cell in all four notebooks. The hosted setup branch was selected with a test marker and `/content` redirected to a local temporary folder. This caught and fixed the editable-import issue. It was **not hosted Colab browser execution**.
- A source archive was extracted into a new folder, dependencies were installed into a new locked virtual environment, and tests plus the full handoff ran against a new store. All source/data/config/environment/partition comparisons matched. Absolute validation RMSE difference was **0.0 kWh** against the `1e-6` tolerance. The active model produced **24 rows** within the 60-second teaching requirement.

The earlier course authoring review also exercised a deliberately incomplete stage before/after repair, a rollback case with a newer pending decoy, whole-batch rejection of an unseen supplier intake, selected-ID exports in a nonempty store and recovery of actual model/source artifacts. Campus rubrics and detailed logs are held in the separate lesson-authoring workspace.

Hosted Colab browser execution and Linux numerical equivalence have not been verified. Read [Colab guidance](colab.md) for runtime, storage, UI and strict-environment boundaries. Synthetic results are teaching evidence; they do not establish forecasting quality for a real facility.
