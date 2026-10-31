# Read notebook figures as evidence

The four local notebooks import shared plotting functions from [linden_mlops.visuals](https://github.com/richhiey/ml-llm-ops/blob/main/src/linden_mlops/visuals.py). A figure displays the supplied records; it does not fit another model, change a selection or establish production readiness.

Each function returns a Matplotlib Figure. Its linden_data attribute contains the exact observations or checks used by the plot. Notebook cells display those values next to the figure. save_figure writes the same layout as editable SVG and PNG under the caller's chosen work/figures folder.

| Notebook figure | Read these labels | What the evidence supports |
|---|---|---|
| Partition and contract | Rows by fixed partition; discrete hour cases and accepted/rejected markers | Data roles and observed domain validation. Final rows are counted only; their targets are not plotted. |
| Experiment comparison | Positive alpha on a logarithmic horizontal axis; validation RMSE and MAE in kWh in separate panels | Ranking among the supplied comparable validation runs. The RMSE winner's marker also identifies it on the diagnostic panel. |
| Artifact identity | Full selected/source run IDs, registered version and batch-resolved version/run | The recorded batch used the selected artifact. The drawing rejects an inconsistent chain. |
| Receiving checks | Explicit lineage and output acceptance results; absolute RMSE delta in kWh and tolerance | Whether these actual receiving records satisfy the shown checks. Missing required evidence cannot become a passing default. |

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
