📝
# Validating an assistant-generated experiment summary

Linden Facilities has a useful result table, but an assistant can still misread metric direction or compare incompatible runs. We will ask for a recommendation and check every claim before it influences promotion.


## Work in the repository

Use `work/runs.csv` and your saved matrix IDs. Request the actual response from your approved assistant using the prompt below. In a local script, open `Project()` and `Workspace(p.tracking)`, then call `verify_summary(p.matrix(ws), proposed_run_id)` from `linden_mlops`. The result's `recommendation_matches_metric` must agree with your manual/UI inspection. Test the numerically worst run once as a deliberately wrong recommendation; expect `False`. Keep your claim checks in one local note or optional notebook, not a second report.

The [optional sprint notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/02-tracking-and-evidence.ipynb) offers the same concepts for exploration. Keep one set of work; no notebook is required for this activity.

## Review a recommendation against the runs

Use the raw rows and API check described above, including a deliberately wrong recommendation. You will also inspect an actual assistant response; a passing numeric check cannot validate all its prose.

1. **Check the input table.** Export only your five returned IDs. Confirm unique IDs, distinct declared alphas, shared controls and finite validation RMSE before requesting advice. Leave the final holdout closed.
2. **Direct your approved assistant.** Supply the raw table and ask: “Recommend a run using lower validation `rmse_kwh`. Name the run ID, explain comparability and controls, and separate measured findings from claims requiring more evidence.” Keep its actual response in your working notes.
3. **Validate the numeric choice.** Run `verify_summary` against its nominated ID. Use the actual result of your declared matrix; its best alpha need not match the supplied example. The intentionally worst-run example must fail. A rejection can also mean incompatible controls; inspect the reason before ranking.
4. **Audit the other claims.** Break the response into claims and match each to a source field. “Lowest validation RMSE” is testable from the table. “Cheapest service” needs operational cost evidence; “always the best alpha” needs broader experiments. Correct or qualify unsupported claims.

## Watch out for

Do not relabel training error as validation error. A close winning margin supports this fixture's ranking, not a universal recommendation. Use your institution-approved assistant and permitted data; no provider credential is required by the course helper.

## Quick reference

| Claim | Check |
|---|---|
| Winner | Returned ID + lowest comparable validation RMSE |
| Fair comparison | Data/split/features/guard/evaluation controls |
| Operational recommendation | Evidence outside the metric table, or an explicit caveat |

## Check your review

Keep one compact table in your working notes: claim → supporting field → accepted/corrected/unsupported. Include one supported numeric claim and any actual overclaim you corrected; if none occurred, state that the reviewed claims were supported. Reuse the table at the sprint checkpoint.

![Validating an assistant-generated experiment summary: evidence path](assets/validating-an-assistant-generated-experiment-summary__01__en.png)

## Learning outcome

Direct an approved assistant to generate a summary comparison across logged experiment runs, validate every recommendation against the raw MLflow data and the declared primary metric, and flag any inaccuracy or invalid comparison.

## Summary

The assistant’s recommendation is now an inspectable set of claims. Your raw-data checks distinguish a valid metric choice from unsupported promotion advice.
