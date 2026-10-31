# Course journey

Use one local clone, the [setup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md), and reusable core modules. Source/terminal is primary; [four local notebooks](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/README.md) are optional companions. Retain good evidence instead of regenerating completed work.

| Sprint | Evidence carried forward | Check before the next stage |
|---|---|---|
| 1 | Your saved `batch_input.py` change, its call in `lifecycle.py`, focused tests and actual named batch output | The complete-plan checks distinguish bad input from valid input; you can explain the source change and the batch’s model/input identity. Installation alone does not establish this work. |
| 2 | Declared configurations, five controlled run IDs, selected validation run and logging/assistant-claim evidence | Source and data stay fixed across the comparison. `work/project.json` reopens the actual selection; a chart or a copied example ID cannot replace it. |
| 3 | Approved/active model identity, monitoring policy/observations, candidate decision, observed job/incident and separate client recovery evidence | Record the actual resulting active version and its source run. The original experiment winner and a later accepted feedback model are different decisions. |
| 4 | Verified `release.json`, canonical export with selected training bytes, supplementary runbook/extension evidence and clean receiving proof | The release names the model actually served. The receiver uses restored source, its own locked environment and new store, with the producer store temporarily unavailable and then restored. |

This table is a handoff check, not an extra submission. Keep the same completed source branch and main `work/project.json`; retain good records rather than repeating work. If a prerequisite artifact is absent, complete that activity before running a later consumer. A new clone installs the baseline application and does not recreate your source changes or decisions.

Incoming client investigations use separate stores named in their briefs. Their decisions do not replace the main project’s selection or active model. Source changes after an experiment invalidate its fixed-source comparison; preserve the records and deliberately revalidate in a new work directory when necessary. Export the intended active run explicitly through the verified release. Final holdouts stay closed until configuration selection and handoff choices are fixed.

## Sprint 1 · Build a reliable pipeline

- [From notebook to pipeline](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/01-from-notebook-to-pipeline/lesson.md) · Concept Note
- [Reading the provided pipeline scaffold](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/02-reading-the-provided-pipeline-scaffold/lesson.md) · Practical Walkthrough
- [Adding and validating a bounded pipeline stage](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/03-adding-and-validating-a-bounded-pipeline-stage/lesson.md) · Practical Walkthrough
- [Explain-the-code checkpoint](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/04-explain-the-code-checkpoint/lesson.md) · Independent Practice
- [Batch vs real-time inference tradeoffs](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/05-batch-vs-real-time-inference-tradeoffs/lesson.md) · Concept Note
- [Pipeline extension deliverable](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-1/06-pipeline-extension-deliverable/lesson.md) · Assessment Lesson

## Sprint 2 · Track and compare experiments

- [Why ad hoc tracking breaks down at scale](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/01-why-ad-hoc-tracking-breaks-down-at-scale/lesson.md) · Concept Note
- [Controls, confounders, and decision metrics](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/02-controls-confounders-and-decision-metrics/lesson.md) · Concept Note
- [Building the five-run experiment matrix](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/03-building-the-five-run-experiment-matrix/lesson.md) · Independent Practice
- [Revisiting MLflow in a pipeline context](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/04-revisiting-mlflow-in-a-pipeline-context/lesson.md) · Practical Walkthrough
- [Comparing multiple runs systematically](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/05-comparing-multiple-runs-systematically/lesson.md) · Independent Practice
- [Autologging and reducing manual tracking overhead](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/06-autologging-and-reducing-manual-tracking-overhead/lesson.md) · Independent Practice
- [Validating an assistant-generated experiment summary](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/07-validating-an-assistant-generated-experiment-summary/lesson.md) · Practical Walkthrough
- [Experiment tracking deliverable](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/08-experiment-tracking-deliverable/lesson.md) · Assessment Lesson

## Sprint 3 · Registry, drift and response

- [From "which file is production?" to a registry](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/01-from-which-file-is-production-to-a-registry/lesson.md) · Concept Note
- [Registering and promoting a model](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/02-registering-and-promoting-a-model/lesson.md) · Practical Walkthrough
- [Recognising drift and choosing a response](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/03-recognising-drift-and-choosing-a-response/lesson.md) · Concept Note
- [From a monitoring signal to an evaluated candidate](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/04-from-a-monitoring-signal-to-an-evaluated-candidate/lesson.md) · Practical Walkthrough
- [Rolling back a bad model version](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/05-rolling-back-a-bad-model-version/lesson.md) · Independent Practice
- [Registry lifecycle deliverable](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-3/06-registry-lifecycle-deliverable/lesson.md) · Assessment Lesson

## Sprint 4 · Reproducible operational handoff

- [What full reproducibility requires](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/01-what-full-reproducibility-requires/lesson.md) · Concept Note
- [Integrating pipeline, tracking, and registry](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/02-integrating-pipeline-tracking-and-registry/lesson.md) · Independent Practice
- [Proving the selected serving path uses the active version](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/03-proving-the-selected-serving-path-uses-the-active-version/lesson.md) · Independent Practice
- [Setup, run, and expected-evidence instructions](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/04-setup-run-and-expected-evidence-instructions/lesson.md) · Independent Practice
- [Proving the pipeline reproduces](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/05-proving-the-pipeline-reproduces/lesson.md) · Independent Practice
- [Reproducible pipeline deliverable](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/06-reproducible-pipeline-deliverable/lesson.md) · Assessment Lesson

[Approved outcome map](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/outcomes.md) · [Operational runbook](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md) · [Verification limits](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/revision-review.md)
