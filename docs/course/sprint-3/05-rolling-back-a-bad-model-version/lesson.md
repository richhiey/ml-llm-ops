✂️
# Rolling back a bad model version

Linden Facilities has a working monitoring response. Now decide which incoming observations justify a candidate, reject an unsuitable one and recover an already active model under a changed acceptance requirement. These are different operational decisions.

## What you will work with

Use the supplied [Linden monitoring inputs and policy](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/exercises/monitoring/linden). They are explicitly synthetic acceptance data. Work in a new investigation store, such as `work/response-investigation`, keeping the cumulative `work/tracking` project unchanged.

Use the already taught `Workspace.run`, registration, observed approval and activation interfaces to establish one guarded incoming baseline in that store. Keep the returned version and source run. Do not run another five-run search. The [operational reference](https://github.com/richhiey/ml-llm-ops/blob/main/docs/operations.md) documents the application interfaces; use explicit store, data, policy and output paths.

For recovery, the exercise intake supplies a separate store at `work/rollback` containing `case.json`, raw runs and registered versions. Open its intake before acting. The [intake instructions](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/README.md) distinguish setup of supplied starting records from your recovery task. Reopen an existing intake rather than regenerating it.

## Your task — decide before taking action

Write the expected action and missing/available evidence for each condition:

- Stable reference/current distributions.
- A warmer feature-only window.
- The warmer window with independent `shift-feedback.csv` labels.
- The warmer window with independent `feedback.csv` labels.
- A separate input copy containing only `24` current rows.

Call `monitor` for each condition with the same incoming model and policy, using different new report destinations. Reconcile predictions against actual actions, counts, distances and validation errors. A report with no labels cannot establish demand error. A valid shifted input is not an invalid input.

For the observed labeled retraining trigger, deliberately use `alpha=1000000` as an intentionally unsuitable candidate. Use `train_candidate` and `compare_candidate` with that actual report and feedback file. Inspect both model errors and each declared acceptance criterion before deciding whether the candidate may become active. Retain its failed comparison and prove the alias unchanged. Successful fitting is not a successful response.

Your useful output is a defensible retain/change decision with raw evidence. Do not edit a `passed` field, change thresholds after seeing scores or open final rows to make a preferred model win.

## Recover an already active version

Inventory `work/rollback` using its actual client/model records. Use `Workspace("work/rollback")` or pass `--state work/rollback` to application commands. Keep every version and artifact.

The revised client requirement is validation RMSE at most `1.6` kWh. Identify the actual active version, each source run, raw validation error and approval status. Explain which previously approved model is suitable now. A prior approval under a looser criterion is insufficient.

Use the real `activate` operation with the suitable actual version and an observed reason, then run a new uniquely named batch against the same isolated store. The [API reference](https://github.com/richhiey/ml-llm-ops/blob/main/docs/api-reference.md) gives argument details. Reconcile the helper's old/new versions, reason and timestamp with the new job's resolved version/source and actual CSV.

Check all `24` IDs once in input order, finite predictions and complete delivery within `60` seconds. Confirm the main project's active version is unchanged. The recovered job is an actual application result; creating the incoming case is not the accomplishment.

## Hints

<details><summary>Hint 1 — Look for missing evidence</summary>

No labels means no observed demand error. Enough independent labels can reveal degradation even when a distribution distance is small. A small monitoring window does not become adequate because it produces a dramatic chart.

</details>
<details><summary>Hint 2 — Separate rejection from recovery</summary>

A pending candidate that never became active can be rejected without rollback. Recovery changes an already active selection to a suitable approved alternative, then verifies a new job.

</details>

## Checkpoints

Your five predictions distinguish the situations using actual evidence. The failed candidate stays pending/inactive. The recovery store ends with a suitable approved version and new valid planner output. Retained history explains the change, and the cumulative project is intact.

<details><summary>Check after recording your decisions and inspecting actual results</summary>

**Result you should get:** stable data continues monitoring; an unlabeled shift and an accurately predicted shifted cohort support investigation; the degraded labeled cohort permits evaluating a candidate; `24` current rows require more observations. The deliberately over-regularized candidate fails acceptance and remains inactive. In the recovery intake, the alpha-10 trial fails the revised `1.6` gate while the earlier alpha-1 version qualifies.

**How:** inspect action, counts and validation RMSE before interpreting distribution flags. Join each actual version to its raw run and approval. Select the qualifying previous version with a reason, then compare its change event and fresh job records. If you trained without justified labels or confused an old CSV with a new job, preserve that failure and repeat only the missing decision/verification. The helper log is mutable and covers helper-mediated changes; it is not a tamper-proof production audit.

</details>

## Learning outcome

Apply a declared feedback policy to unfamiliar monitoring evidence, retain or qualify a retrained candidate using separate validation data, and restore a suitable previously approved active version in a supplied rollback incident, documenting the resulting audit and new inference evidence.

## Summary

You can distinguish continued investigation, rejection of an inactive candidate and recovery from an already active version. Each decision produces an inspectable system state and useful evidence rather than a copied reference verdict.
