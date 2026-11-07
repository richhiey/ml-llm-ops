📝
# Validating an assistant-generated experiment summary

Threadline's catalog lead asks an assistant to summarize the experiment study. A fluent recommendation could still quote the wrong run, miss a category regression or turn a one-seed observation into a production claim. You will direct a bounded request and validate the response before it enters the handoff.

Use an assistant approved for your learning environment. Supply the actual run records you are allowed to share. Do not give an assistant credentials or assume it can see your local MLflow store.

# 1. Prepare evidence the assistant can inspect

Use your completed comparison and retrieve the corresponding raw runs in MLflow. Include full run IDs, configurations, comparison controls, primary metric, diagnostic results and the distinction between candidates and the autologging repeat.

The [actual author demonstration](https://github.com/richhiey/ml-llm-ops/tree/main/docs/course/evidence/sprint-2) retains a Codex request, its real response and the validation. It is an authoring example, not a student submission. Its run IDs refer to the author's store; use your own records for your request.

# 2. Ask for a bounded recommendation

Send a request like this, with your actual evidence attached or pasted:

> Recommend one configuration for further registry validation using validation macro F1, maximized across comparable baseline/candidate rows. Cite full run IDs and raw metric values. Explain the changed factor, gain, category regressions and measured training-time tradeoff. Treat repeated configurations as instrumentation evidence. Flag missing controls and do not infer test performance, significance, inference speed, cost or production readiness. Return a short recommendation and a table of checkable claims.

Retain the exact request and unedited response. The author example's [request](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/evidence/sprint-2/assistant-request.md) and [response](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/evidence/sprint-2/assistant-response.md) show what this evidence looks like.

# 3. Check the recommendation against raw records

For the selected run, open its full ID in MLflow and inspect parameters, final metrics, source/split tags and the logged model. `MlflowClient.get_run()` retrieves that recorded object directly; its `data.params`, `data.metrics` and `data.tags` are the values you are checking. The [comparison source](https://github.com/richhiey/ml-llm-ops/blob/main/src/catalog_mlops/comparison.py) shows how those records are checked against the downloaded prediction CSV.

| Claim to validate | Inspect | Decision |
|---|---|---|
| This configuration wins | Eligible full-precision `validation_macro_f1` values | Accept only the largest value under the declared tie rule |
| One factor caused the observed difference | Configurations plus fixed comparison controls | Qualify or reject if another factor changed |
| It improves the difficult categories | Raw per-category counts, precision, recall and F1 | Report regressions as well as gains |
| It uses a specific model | Logged-model source run and learned-state identity | Reject an artifact detached from the evaluated run |
| It is faster or cheaper | Actual timer boundary and available workload evidence | Reject conclusions beyond the measured work |

In the actual author response, the recommended full ID is `99ce416e13ee4eeba47f6adf05d4ed7c`, with macro F1 `0.8572382087673285`. The baseline is `c538c971fdf44099b750af1d9513458b`, with `0.8322013435739599`. Subtracting gives `0.025036865193368563`. Check those values in the raw reference records before accepting the sentence.

Then verify the qualification: shirt recall improved, while T-shirt/top and coat recall fell. The response also reports lower shirt/dress/pullover precision and lower trouser recall. Its training-duration claim refers to updates, epoch validation and telemetry, not serving latency. The [claim validation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/evidence/sprint-2/assistant-validation.md) records the individual checks. The actual response's recommendation survived; validation does not require inventing an assistant error.

# 4. Test claims that should be flagged

The following statements are deliberately constructed counterexamples, not quotations from that actual response. Diagnose each against the same evidence:

- “Every category improved with longer training.”
- “The autologging repeat provides a sixth distinct improvement candidate.”
- “The shorter training run must return predictions faster.”

Retain an accepted/qualified/rejected decision and a reason for each claim in `work/assistant-validation.md`. Include the exact raw ID, field or prediction count that supports the decision. Apply the same process to every recommendation in your own assistant response, correcting the handoff where needed.

# Watch out for

A correct winner does not make every supporting sentence correct. A run name can be reused; retain full IDs. Keep the assistant's original response when recording corrections. A constructed bad claim is useful practice only when labeled separately from the actual response.

# Quick reference

| Evidence | What it supports |
|---|---|
| Native run parameters/tags | Recipe and declared conditions |
| Raw predictions and recomputed metrics | Observed quality |
| Model metadata and weights | Artifact connection |
| Exact request/response and claim decisions | Auditable assistant use |

## Learning outcome

Direct an approved assistant to generate a summary comparison across logged experiment runs, validate every recommendation against the raw MLflow data and the declared primary metric, and flag any inaccuracy or invalid comparison.

## Summary

Threadline has a checked recommendation with traceable numbers and stated limits. The assistant helped communicate the evidence; your validation determines which claims can enter the model handoff.
