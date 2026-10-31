# Read notebook figures as evidence

Notebooks 01 and 02 use [linden_mlops.visuals](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/visuals.py) for contract and experiment plots. Notebook 03 uses `plot_monitoring` from [linden_mlops.operations](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/operations.py). Notebook 04 leaves the handoff investigation to your own attempt; it does not supply a plotting cell. A figure displays the supplied records; it does not fit another model, change a selection or establish production readiness.

The plotting functions return Matplotlib Figures. Each figure's `linden_data` attribute contains its plotted observations or checks. Inspect those fields alongside the underlying records. `save_figure` from `visuals` writes the same layout as editable SVG and PNG under the caller's chosen `work/figures` folder.

| Available helper | Use in the supplied notebooks | Labels and interpretation |
|---|---|---|
| `visuals.plot_contract` | Notebook 01 | Fixed partition row counts and discrete hour probes show data roles and observed domain validation. Final targets are not plotted. |
| `visuals.plot_experiments` | Notebook 02 | Positive alpha on a logarithmic axis; validation RMSE and MAE in kWh in separate panels. Ranking applies to the supplied comparable runs. |
| `operations.plot_monitoring` | Notebook 03 | Distances divided by their declared thresholds are dimensionless. A ratio of 1 reaches an alert boundary; an alert alone does not establish model degradation. |
| `operations.plot_candidate` | Optional helper; no supplied notebook call | Incumbent and candidate RMSE in kWh use the same independent labeled feedback cohort and declared maximum-error boundary. |
| `visuals.plot_identity` | Optional helper; no supplied notebook call | Selected/source run IDs, registered version and batch-resolved identity must agree. This does not establish approval by itself. |
| `visuals.plot_recovery` | Optional helper; no supplied notebook call | Actual lineage/output checks and absolute RMSE delta in kWh show whether the supplied receiving records satisfy their tolerance. Missing evidence cannot become a passing default. |

## Compare before concluding

The experiment plot uses discrete observations without drawing an unmeasured fitted curve between alphas. A tiny metric lead is a ranking under this fixture's conditions, not a confidence interval or proof of better forecasting on real buildings. Training diagnostics and final scores stay out of the comparison.

The identity diagram is derived from records. It is not a screenshot of MLflow. A version counter alone does not express approval or current selection, and a later alias lookup does not establish what an earlier job loaded.

The receiving figure checks actual row identity/order and finite outputs independently of the saved report. Its delta marker remains visible at zero, and a result above tolerance is shown beyond the boundary. Batch time measures model loading, prediction and file writing; setup and training are separate.

## Use the figure in your project

Give a plotting function the actual objects from your retained project. Save its image with your records and keep the raw fields needed to inspect it. If a figure refuses the input, investigate the stated missing or incompatible evidence before changing the plot.

Sprint 1 embeds six educational figures. Relationship, ownership and timing diagrams are labeled schematic; the new complete-plan stage chart uses actual accepted/rejected input probes. Captions distinguish supplied requirements from measurements. A figure newly plotted in a notebook uses the records supplied by that notebook execution, including your retained project or monitoring reports. Embedded Campus images labeled as author references instead retain their separate author-run observations. Your actual alpha values, run IDs and measured timings can differ. Use the [exact outcome map](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/outcomes.md) to find the matching notebook and activity.

## Campus diagrams for tracking and lifecycle decisions

Sprint 2 embeds one main SVG/PNG pair in each of its eight lessons. Sprint 3 embeds figures in its two registry lessons, drift concept and monitoring walkthrough; its independent practice and assessment rely on the learner's actual operational artifacts. The [reference observations](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/figures/reference-observations.json) retain asset fingerprints, observation provenance and interpretation limits, including retained assets from earlier revisions. An asset's presence in that manifest does not mean it is embedded in the current lesson. Missing-link, plan, claim and alias diagrams are schematic; they are not MLflow screenshots. Reference error magnitudes used to explain MAE/RMSE are explicitly illustrative. The experiment comparison uses actual local validation observations and appears only inside post-attempt feedback. Its detail view has a different labeled scale to expose close raw values; the main plot preserves the full observed range.

An automatic/manual logging diagram uses observed key sets and equal held-out predictions from a matched pair. Registry/batch identity is backed by actual source-run and resolved-version records. Replay diagrams show conditions to verify rather than inventing a passing student result. Client diagrams leave counts, grouping and qualifying versions for the learner to determine.

## Campus handoff visuals

Sprint 4 embeds three figures: recoverable recipe ingredients in the concept note, the export/receiving boundary in the runbook practice, and the clean receiving reference after the learner's receiving attempt. The first two show evidence relationships and schematic boundaries. The receiving image uses actual author-run original/repeated validation metrics, the retained report and independently checked input/output, with separate evidence for restored source, new environment/state and original-store isolation. Zero delta is an observed value, not a default for missing evidence. The report flag alone cannot establish all of those facts.

The remaining handoff activities require the learner's actual release, serving and receiving artifacts. Package identity supports reuse only when linked to an already demonstrated clean execution of the same recipe under applicable conditions. Supplementary HANDOFF.md/extension explanation is distinct from the automatic export's indexed runtime content.
