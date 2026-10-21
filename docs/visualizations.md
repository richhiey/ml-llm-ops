# Read notebook figures as evidence

The four local notebooks import shared plotting functions from [linden_mlops.visuals](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/visuals.py). A figure displays the supplied records; it does not fit another model, change a selection or establish production readiness.

Each function returns a Matplotlib Figure. Its linden_data attribute contains the exact observations or checks used by the plot. Notebook cells display those values next to the figure. save_figure writes the same layout as editable SVG and PNG under the caller's chosen work/figures folder.

| Notebook figure | Read these labels | What the evidence supports |
|---|---|---|
| Partition and contract | Rows by fixed partition; discrete hour cases and accepted/rejected markers | Data roles and observed domain validation. Final rows are counted only; their targets are not plotted. |
| Experiment comparison | Positive alpha on a logarithmic horizontal axis; validation RMSE and MAE in kWh in separate panels | Ranking among exactly five comparable validation runs. The RMSE winner's marker also identifies it on the diagnostic panel. |
| Artifact identity | Full selected/source run IDs, registered version and batch-resolved version/run | The recorded batch used the selected artifact. The drawing rejects an inconsistent chain. |
| Receiving checks | Explicit lineage and output acceptance results; absolute RMSE delta in kWh and tolerance | Whether these actual receiving records satisfy the shown checks. Missing required evidence cannot become a passing default. |

## Compare before concluding

The experiment plot uses discrete observations without drawing an unmeasured fitted curve between alphas. A tiny metric lead is a ranking under this fixture's conditions, not a confidence interval or proof of better forecasting on real buildings. Training diagnostics and final scores stay out of the comparison.

The identity diagram is derived from records. It is not a screenshot of MLflow. A version counter alone does not express approval or current selection, and a later alias lookup does not establish what an earlier job loaded.

The receiving figure checks actual row identity/order and finite outputs independently of the saved report. Its delta marker remains visible at zero, and a result above tolerance is shown beyond the boundary. Batch time measures model loading, prediction and file writing; setup and training are separate.

## Use the figure in your project

Give a plotting function the actual objects from your retained project. Save its image with your records and keep the raw fields needed to inspect it. If a figure refuses the input, investigate the stated missing or incompatible evidence before changing the plot.

Campus illustrations are reference executions from the local author verification. Your own declared alpha values, run IDs and measured timings can differ. Use the [exact outcome map](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/outcomes.md) to find the matching notebook and activity.
