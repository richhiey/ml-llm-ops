✂️
# Experiment tracking deliverable

Harbor Facilities wants to know which configuration it should promote and why. You will hand over a controlled comparison and a checked assistant recommendation. A client note bundles differently labeled observations and a confident recommendation. Audit it before deciding whether it changes your evidence-based selection.


## Notebook workspace

Use the [sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) in your local project environment. Find the section for **Experiment tracking deliverable** using its Campus activity ID **A-S2-08**. It imports the shared core modules for the demonstrations; keep your own decisions and checks in the attempt cells. Reuse this same clone and saved work between activities.

## Work in the repository

Reuse your existing five logged configurations, actual autologging evidence, MLflow UI inspection and approved assistant response. Prepare the new client intake from those actual records:

```sh
uv run python docs/course/exercises/prepare-evidence.py comparison --destination work/harbor-comparison
```

Open `observations.json` and `client-note.txt` in that directory. Preparation reads your logged matrix; it does not train another model. Keep the generated files unchanged and record your audit in the same working note as your previous claim checks. The client note is an intentionally unreliable assessment fixture, not a new response from your approved assistant. Preserve the actual prompt, input table and assistant response from your earlier work as separate evidence. No new notebook or duplicate assistant call is required.

## What you will work with

Reuse your cumulative helper project and its fixed synthetic snapshot, [contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md), [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) and [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/clean-state.md). Keep `row_id`, `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition` unchanged in the source data. Harbor is a new acceptance client inside the same scaffold; it does not introduce a replacement project.

## As you work, keep these questions in mind

How many independent configurations does the intake actually represent? Do the metric names refer to the same evaluation rows? Which recommendation can the records support, and which claims require another kind of evidence?

## Quick diagnosis

Before changing any selection, count the observation labels and distinct run IDs in `observations.json`. Mark each observation's metric and row basis. Record whether every label represents another independent comparable configuration; then test the client's recommendation against raw MLflow records.

## Making improvements

### Task A — Audit the controlled comparison

Retain evidence for your five distinct declared configurations: matrix, actual IDs, raw parameters/metrics/artifacts and shared data, split, source, guard and evaluation controls. Trace every intake observation to its source run. Decide which observations belong in the validation ranking and which are diagnostics. Record the corrected ranking using your actual five IDs and raw `rmse_kwh` values. Keep the final partition unopened until selection is fixed for the final handoff; do not evaluate it to resolve this intake.

### Task B — Demonstrate autologging

Reuse the enabled-before-fit setup and your real autolog on/off comparison. Trace the intake's training metric to its logged field and row basis alongside the explicit validation metric. Autologging captures estimator fields during fitting; explicit logging records the pipeline’s declared validation result. Explain which fields autologging owns, why `log_models=False` is used and what explicit logging still controls. Preserve your existing five-run MLflow UI inspection record.

### Task C — Validate the recommendation

Keep the actual approved-assistant prompt, input and response, together with your prior claim-by-claim verification. Separately audit the supplied client note: for each claim, cite a raw field, correct it or state the missing evidence. Decide whether it changes the justified configuration-to-promote recommendation, naming the actual selected run ID. Operational claims need operational evidence; do not manufacture measurements.

## Final check

Check your existing working notes with links to the actual output files and run IDs. Explain one decision by pointing to its raw evidence. Keep unsupported claims visible and correct them before relying on them. Use only previously practiced interfaces; no new platform is required.

## Check your audit after the attempt

<details>
<summary>Solution — observation identity, metric basis and claim scope</summary>

**Result you should get:** the intake has `6` observation labels but `5` distinct run IDs and configurations. Five observations contain validation `rmse_kwh`; the sixth is an actual `training_root_mean_squared_error` from one of those same five runs. It is a diagnostic observation, not a sixth independent validation candidate. The corrected winner is the lowest raw validation `rmse_kwh` among your five comparable IDs. No reference alpha or example ID overrides that result.

The client note's sixth-candidate recommendation is invalid because it double counts a run and mixes training and validation rows. Its claims about lowest serving cost and readiness are unsupported by these error metrics. A defensible correction names the validation winner, the fixed controls and the cost/operational checks still needed. The final partition remains unopened. The real approved-assistant response stays in your evidence; a supplied fixture cannot establish that you directed an assistant.

**How:** first produce the intake counts and validation ranking, then match each observation's run ID and metric to the raw run in MLflow:

```python
from pathlib import Path
import json

observations = json.loads(
    Path("work/harbor-comparison/observations.json").read_text()
)["observations"]
print("observations:", len(observations))
print("distinct runs:", len({row["run_id"] for row in observations}))
validation = [row for row in observations
              if row["metric_name"] == "rmse_kwh"
              and row["evaluation_basis"] == "validation"]
assert len(validation) == len({row["run_id"] for row in validation}) == 5
for row in sorted(validation, key=lambda row: row["value"]):
    print(row["run_id"], row["alpha"], row["value"])
```

The counts are `6` observations and `5` distinct runs; the printed ranking contains your actual five validation run IDs. Match each value to its original logged field and confirm the shared controls before accepting that ranking. Recheck the proposed winner with the previously practiced `verify_summary` call on your five-run matrix. It verifies the numeric recommendation; it does not establish the client's operational claims.

If you counted six configurations, revisit unique run IDs rather than observation names. If the training score wins your ranking, restore the metric/partition filter. If the five candidates have different controls, resolve that incompatibility before declaring a winner. A cheap-to-run or deployment-ready claim needs separate measured evidence, not a more persuasive summary.

</details>

## Learning outcome

Deliverable: at least 5 experiment configurations logged and compared in MLflow, an autologging setup, and an AI-assisted summary recommending which configuration to promote - with the summary validated against raw data.

## Summary

Harbor receives a recommendation supported by controlled runs, actual logging evidence and a checked assistant response. The original response remains available beside its corrections.
