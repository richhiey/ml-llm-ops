🏷️
# Why ad hoc tracking breaks down at scale

Linden Facilities has five model results copied into a spreadsheet. Two rows say “best”, one notebook was rerun, and the planner cannot connect either recommendation to the model that produced it. More rows have made the record harder to trust.

## Your route through this lesson

Reconstruct a recommendation and diagnose the context missing from manual records. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** Three distinct failure diagnoses and the records needed to inspect each.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb#scrollTo=tracking-records). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Reconstruct a decision from the receiver's side

Picture yourself taking over the planner's result sheet. It lists five alpha settings, five scores and a highlighted row. Your first question is not whether the highlight looks reasonable. It is whether the numbers answer the same question. Your next question is which fitted artifact belongs to the highlighted result. Finally, you need to know how to recover its recipe.

A manually maintained table can answer these questions when it retains exact identities and links. It becomes fragile when the author copies the latest printout into a reused row, changes a split without changing the label, or renames an artifact without keeping its source run. These are different failures. Adding another score column fixes none of them by itself.

## A score needs its context

An **experiment run** is one execution with a unique identifier and recorded inputs, settings and results. MLflow stores runs with parameters, metrics and artifacts. A **parameter** describes a setting such as `alpha`; a **metric** measures a result such as validation RMSE; an **artifact** is a file such as the fitted model or source bundle.

| Manual failure | Consequence | Evidence systematic tracking should retain |
|---|---|---|
| Copy score without run ID | Cannot find its model | Run → model artifact link |
| Overwrite notebook output | Cannot reconstruct earlier comparison | Separate run records |
| Omit split or snapshot | Compare unlike evaluations | Data hash and partition |
| Rename a model file “final” | Selection becomes ambiguous | Registered version and active alias |
| Record alpha but omit environment | Rerun may use different behavior | Source revision and dependency lock |

A spreadsheet can be a useful evidence view. The problem is depending on manual copying as the only connection between an execution and its context. Tracking integrated into the pipeline records that connection when the work happens.

## Why repeated work makes omissions expensive

With one run, you may remember its configuration. With five configurations, retries and a colleague's experiment, a name such as `baseline` may appear several times. A retry is another execution even when its settings match. If you overwrite the earlier row, you lose the ability to explain whether the change came from a parameter, source edit or a different environment.

Systematic tracking records the execution when it occurs. A run ID identifies that execution, while parameters describe what it used and metrics describe what was measured. An artifact stores something larger than a scalar, such as the fitted model or the archived source. These distinctions let a receiving engineer navigate from a reported score to recoverable material instead of guessing from a filename.

## Follow one claim through its supporting records

Take the claim “we recommend this configuration because it has the lowest validation RMSE among the controlled runs”. To inspect it, follow this chain:

1. The recommendation names a full run ID, not just `alpha=1`.
2. That run's parameters identify the data snapshot, source and evaluation partition.
3. Its metric dictionary contains the declared held-out `rmse_kwh` value.
4. The selected comparison population shows that the other candidates used the same controls.
5. The model URI and reproduction artifacts connect that execution to its fitted result and recipe.

This is **auditability** in practical terms: another person can inspect how the recommendation was reached. It is stronger than a chart with no source records. It is still limited by what was actually recorded and whether the content remains available.

## Understand what tracking cannot recover

Suppose you log a score today but the dataset used yesterday has already been replaced. Recording today's filename cannot restore yesterday's bytes. Likewise, a tag saying `approved` cannot recreate a missing validation test. Tracking makes retained context searchable; it cannot retrospectively invent evidence.

For Linden, the useful habit is to create the record inside the pipeline, retain the source/data/configuration/environment package and carry the returned identities into later decisions. You will inspect those records directly. The lesson's broken handoff check asks you to identify the missing links first, so you can explain why each logged field has a job.

## Tracking still needs judgment

Logging every run does not make comparisons valid. A run with a different evaluation partition should not win because its score looks smaller. Linden must declare controls and a primary metric before interpreting the tracked table. Automatic records reduce transcription work; they do not choose the business question.

![Why ad hoc tracking breaks down at scale: evidence path](assets/why-ad-hoc-tracking-breaks-down-at-scale__01__en.png)

## Check for Understanding

Linden's handoff sheet contains: `run-A: alpha=1, score=1.44`; `run-B: alpha=10, score=1.40`; and a file named `best.pkl`. The sheet omits metric name, evaluation rows and the link from either run to the file. Name three distinct decisions this record cannot support, then specify what you would retrieve before recommending either run.

▶️ **Solution** *(toggle)*

> **Result you should get:** it cannot establish the metric/direction winner, comparability of evaluation conditions, or which artifact would be selected. Retrieve the metric definition/raw value, snapshot/split/config, and source-run-to-model link.
>
> **How:** follow each proposed decision backward to the missing evidence. Copying the two scores into MLflow later would not recover missing context.

## Learning outcome

Identify 3+ failure modes of tracking experiments manually (spreadsheets, notebook print statements) once a team runs many models, and explain why systematic tracking matters for auditability.

## Summary

Linden’s scores can now be questioned through the context each record must retain. You can name how manual omissions break a model decision’s traceability.
