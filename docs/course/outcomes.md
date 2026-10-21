# Module A Campus outcome map

The 26 rows below preserve the supplied Module A Campus journey's lesson order, types and verbatim outcomes. The authoring source is the v11 sheet export (SHA256 3f2397d866add08ad3537eada95082db0dbb0d3582444cd82791dcc2eca3cfb2).

Each activity uses the same local project and the corresponding shared-core-module notebook. Read the task, make an attempt, then open the collapsed feedback.

## A-S1-01 · From notebook to pipeline

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/01-from-notebook-to-pipeline/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Explain why a reproducible training/inference pipeline replaces a one-off notebook workflow, and identify the 5 stages a production ML pipeline must cover - ingestion, preprocessing, training, evaluation, inference.

## A-S1-02 · Reading the provided pipeline scaffold

**Type:** Practical Walkthrough · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/02-reading-the-provided-pipeline-scaffold/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Trace how data moves through the provided training/inference pipeline scaffold from raw input to served prediction, and label each stage's purpose.

## A-S1-03 · Adding and validating a bounded pipeline stage

**Type:** Practical Walkthrough · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/03-adding-and-validating-a-bounded-pipeline-stage/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Follow an expert adding one preprocessing or validation stage to the provided pipeline, then verify its input/output contract and confirm that the unchanged stages still run.

## A-S1-04 · Explain-the-code checkpoint

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/04-explain-the-code-checkpoint/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Given an AI-generated addition to the pipeline, explain line by line what it does, test its input/output contract, and identify any part that needs correction before merging.

## A-S1-05 · Batch vs real-time inference tradeoffs

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/05-batch-vs-real-time-inference-tradeoffs/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Compare batch and real-time inference patterns - latency, cost, throughput - and justify which pattern the provided inference brief requires.

## A-S1-06 · Pipeline extension deliverable

**Type:** Assessment Lesson · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/06-pipeline-extension-deliverable/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb)

Deliverable: the provided pipeline scaffold extended with at least 1 validated stage, a line-by-line explanation of the changed logic, and a justified batch-vs-real-time recommendation for the inference brief.

## A-S2-01 · Why ad hoc tracking breaks down at scale

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/01-why-ad-hoc-tracking-breaks-down-at-scale/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Identify 3+ failure modes of tracking experiments manually (spreadsheets, notebook print statements) once a team runs many models, and explain why systematic tracking matters for auditability.

## A-S2-02 · Controls, confounders, and decision metrics

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/02-controls-confounders-and-decision-metrics/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Explain why a run comparison is invalid when dataset split, evaluation conditions, or multiple uncontrolled factors change, and distinguish a primary decision metric from diagnostic metrics.

## A-S2-03 · Building the five-run experiment matrix

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/03-building-the-five-run-experiment-matrix/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Define a five-run experiment matrix for the provided training and inference pipeline starter that holds the dataset split and evaluation conditions constant, names the factor varied in each comparison, selects a primary metric tied to the inference brief, and labels any run that is not directly comparable.

## A-S2-04 · Revisiting MLflow in a pipeline context

**Type:** Practical Walkthrough · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/04-revisiting-mlflow-in-a-pipeline-context/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Use the provided MLflow setup to log parameters, metrics, and artifacts automatically as part of the cumulative pipeline, building on basic experiment logging from T4 (AI track).

## A-S2-05 · Comparing multiple runs systematically

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/05-comparing-multiple-runs-systematically/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Use the MLflow UI to compare 5+ experiment runs against each other and identify the best-performing configuration for a given metric.

## A-S2-06 · Autologging and reducing manual tracking overhead

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/06-autologging-and-reducing-manual-tracking-overhead/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Configure autologging for the pipeline and explain the tradeoff between autologging convenience and control over what gets logged.

## A-S2-07 · Validating an assistant-generated experiment summary

**Type:** Practical Walkthrough · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/07-validating-an-assistant-generated-experiment-summary/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Direct an approved assistant to generate a summary comparison across logged experiment runs, validate every recommendation against the raw MLflow data and the declared primary metric, and flag any inaccuracy or invalid comparison.

## A-S2-08 · Experiment tracking deliverable

**Type:** Assessment Lesson · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/08-experiment-tracking-deliverable/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb)

Deliverable: at least 5 experiment configurations logged and compared in MLflow, an autologging setup, and an AI-assisted summary recommending which configuration to promote - with the summary validated against raw data.

## A-S3-01 · From "which file is production?" to a registry

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/01-from-which-file-is-production-to-a-registry/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Explain 3 problems a model registry solves that ad hoc file-saving does not - versioning, alias/tag-based lifecycle control, and auditability - and recognise staging, production, and archived as superseded stage vocabulary replaced by aliases, tags, and environment-specific registered models.

## A-S3-02 · Registering and promoting a model

**Type:** Practical Walkthrough · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/02-registering-and-promoting-a-model/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Use the provided model registry scaffold to register a new model version, record its validation status with tags, and promote it by assigning the scaffold's active-model alias.

## A-S3-03 · What full reproducibility requires

**Type:** Concept Note · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/03-what-full-reproducibility-requires/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Identify the code version, data snapshot, parameters/configuration, environment, and model artifact that must be traceable together for a training run to be reproducible.

## A-S3-04 · Reproducing a past training run

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/04-reproducing-a-past-training-run/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Given a past experiment logged in MLflow, use its recorded code, data, configuration, environment, and registry lineage to reproduce the evaluation result within the tolerance declared in the clean-state verification specification.

## A-S3-05 · Rolling back a bad model version

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/05-rolling-back-a-bad-model-version/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Reassign the active-model alias from a bad version to the previous approved version, and document what the registry audit evidence captured during the rollback.

## A-S3-06 · Registry lifecycle deliverable

**Type:** Assessment Lesson · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/06-registry-lifecycle-deliverable/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/03-registry-and-reproduction.ipynb)

Deliverable: a model registered, tagged with validation evidence, assigned the active-model alias, then rolled back by alias reassignment - with a documented audit trail and the lineage needed to reproduce the approved run within the tolerance declared in the clean-state verification specification.

## A-S4-01 · Scoping the cumulative pipeline for production-grade reproducibility

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/01-scoping-the-cumulative-pipeline-for-production-grade-reproducibility/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Continue the pipeline built across Sprints 1-3 and scope the remaining work needed to meet the final criteria. A T4 (AI track) model may replace the baseline model only as a deliberate transfer test inside the same scaffold.

## A-S4-02 · Integrating pipeline, tracking, and registry

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/02-integrating-pipeline-tracking-and-registry/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Integrate the existing pipeline stages, MLflow tracking, registry aliases/tags, and inference-mode decision into one end-to-end run that trains, evaluates, logs, and registers a model version.

## A-S4-03 · Proving the selected serving path uses the active version

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/03-proving-the-selected-serving-path-uses-the-active-version/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Exercise the selected batch or real-time inference path with a representative input, verify that it resolves to the intended active model version, and capture the output plus the latency, throughput, or completion evidence named in the inference decision brief.

## A-S4-04 · Setup, run, and expected-evidence instructions

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/04-setup-run-and-expected-evidence-instructions/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Produce environment/setup and run instructions that start from the clean-state verification specification's declared clean state, name the data snapshot and exact execution command, and state the expected lineage fields, inference evidence, and result tolerance a second engineer must verify.

## A-S4-05 · Proving the pipeline reproduces

**Type:** Independent Practice · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/05-proving-the-pipeline-reproduces/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Re-run the completed pipeline from the declared clean state, verify its lineage and result against the tolerance declared in the clean-state verification specification, and document and diagnose any divergence.

## A-S4-06 · Reproducible pipeline deliverable

**Type:** Assessment Lesson · [Campus activity](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/06-reproducible-pipeline-deliverable/lesson.md) · [Notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/04-cumulative-handoff.ipynb)

Deliverable: the cumulative end-to-end pipeline (train -> track -> register -> select active version -> exercise the selected inference path) reproduced from the declared clean state, with traceable code/data/configuration/environment lineage, reproducible setup/run instructions, inference evidence, and at least one non-trivial extension documented and explained.
