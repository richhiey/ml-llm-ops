📝
# Validating an assistant-generated experiment summary

Linden Facilities has a useful result table, but an assistant can still misread metric direction or compare incompatible runs. We will ask for a recommendation and check every claim before it influences promotion.

## Your route through this lesson

Direct an assistant using selected raw evidence and validate its recommendations claim by claim. Run the explained blocks in order, pausing to compare each result with its interpretation. Use the local Python 3.12 setup or the linked Colab route. Terminal commands and notebook Python are different interfaces; the setup guide shows their equivalents.

**Finish with:** Prompt/input/response, numeric check, claim table and corrected recommendation.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/02-tracking-and-evidence.ipynb#scrollTo=assistant-review). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Before you start

Use an institution-approved assistant and your five-run workspace. If you lack an executed matrix, prepare one with `uv run python exercises/prepare-practice.py matrix --state state-compare` from the helper/project root. Otherwise use your actual state path in the code below. Do not send private data or credentials. The course snapshot is synthetic. If assistant access is unavailable, use the [saved assistant reference](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/assistant-summary-reference.md) to rehearse validation, and record that a new live request remains unperformed.

## Decide what counts as a claim

An assistant response often combines several claims in one sentence. “Run X has the best error, uses the same data, and is ready to become active” contains a numeric ranking, a control check and an operational recommendation. Each needs a different source. A correct first number does not validate the rest of the sentence.

Your output will have four parts: the selected raw table, the exact prompt/response, a claim-evidence table and a corrected recommendation. The response stays unchanged so a reviewer can see what you checked. A correction is your separate conclusion after inspection, not an edited record pretending the assistant said it correctly first.

## 1. Export the raw evidence

```python
from campus_mlops import Workspace, export_runs, verify_summary
import json
ws = Workspace('state-compare')
selected_ids = json.loads((ws.path / 'matrix-run-ids.json').read_text())
all_rows = export_runs(ws)
rows = all_rows[all_rows.run_id.isin(selected_ids)].copy()
assert set(rows.run_id) == set(selected_ids)
rows.to_csv(ws.path / 'selected-runs.csv', index=False)
print(rows[['run_id', 'alpha', 'rmse_kwh', 'evaluation_partition']])
```

**Expected:** exactly the selected IDs are present, with at least five distinct alpha configurations. Inspect source/data/guard/partition controls before exporting. `verify_summary` rejects mixed or repeated evidence rather than silently discarding incompatible rows; retain excluded evidence separately.

## Verify the population before asking for advice

After exporting `rows`, inspect the controls explicitly:

```python
controls = ['data_sha256', 'code_revision', 'evaluation_partition', 'range_guard']
print(rows[controls].drop_duplicates())
print(rows['alpha'].astype(float).nunique())
assert len(rows) >= 5 and rows['run_id'].is_unique
assert rows['alpha'].astype(float).nunique() >= 5
```

**Expected:** one shared control combination and at least five alpha values. The selected ID file is a record of the population you intended to compare; `export_runs` alone includes every finished run in the store. If it also contains an older baseline or a different partition, retain that record separately with an exclusion reason. Sending a mixed table and asking the assistant to “find the best” has already left the comparison rule ambiguous.

The numeric helper enforces some of these conditions, but you still need to explain what was controlled. A hash proves identity against the supplied bytes, not that the dataset is representative of a real facility.

## 2. Direct the assistant precisely

Use this prompt with your inspected table:

> Compare these five runs using validation `rmse_kwh`, lower is better. Name the recommended run ID, alpha and metric value. Check data hash, code revision, evaluation partition and guard consistency. Separate MAE/training diagnostics from the primary metric. Cite table fields for every recommendation, flag incompatible comparisons, and state what the table cannot establish about serving or deployment readiness. Do not invent results.

**Expected:** a saved response with a run-specific recommendation. Save the exact prompt, input table and response before editing. Generated wording may vary; a recommendation is not proof of correctness.

## 3. Check the numeric selection

Replace the placeholder below with the response's actual recommended run ID:

```python
check = verify_summary(rows, 'ACTUAL_RECOMMENDED_RUN_ID')
print(check)
```

**Expected for the reference matrix:** best alpha `0.01`, RMSE about `1.434281768`. The returned boolean should be true only for the lowest-RMSE row under the controls. Check the chosen run directly with `ws.client.get_run(...)`; do not accept a copied rounded value as the only evidence.

## Read both a passing and a failing numeric check

For a deliberate test independent of the assistant's actual answer:

```python
best_id = rows.sort_values('rmse_kwh').iloc[0]['run_id']
worst_id = rows.sort_values('rmse_kwh').iloc[-1]['run_id']
print(verify_summary(rows, best_id)['recommendation_matches_metric'])
print(verify_summary(rows, worst_id)['recommendation_matches_metric'])
```

**Expected:** `True`, then `False`. This shows the numeric gate distinguishes the declared ranking. It does not show that a natural-language response was checked: you must also pass the actual recommended run ID and inspect the assistant's stated metric value and controls against `get_run`.

If your independently declared matrix differs from the reference fixture, use its actual raw winner. If the response names an ID absent from the selected table, flag it as unsupported before considering its prose explanation.

## 4. Audit claims beyond the winner

Use the [claim evidence sheet](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/exercises/claim-evidence-sheet.csv) to create a claim/evidence/verdict/correction table. For “ready to deploy”, the verdict is unsupported by metrics alone: the table does not prove input contracts, active version, inference completion or clean-state replay. For a lower training error used to overrule validation RMSE, mark the decision rule invalid. For a changed partition, exclude the comparison.

**Expected:** every recommendation has a raw run field or an explicit unsupported verdict. As a deliberate negative test, call `verify_summary(rows, rows.sort_values("rmse_kwh").iloc[-1].run_id)` and confirm `recommendation_matches_metric` is false. This is a test case, not a claimed assistant response. Save your corrected recommendation separately from the original response.

## Work a small claim review before reviewing the whole response

These are illustrative claims, not a claimed live response:

| Claim | Evidence needed | Appropriate verdict |
|---|---|---|
| “The recommended ID has the lowest validation RMSE” | Selected rows and raw metric | Supported only if the ID/value/direction match |
| “Lower training error makes it the validation winner” | Training and validation metric definitions | Invalid decision rule |
| “All five use the same snapshot” | Every selected `data_sha256` | Supported only after checking all rows |
| “The winning run is ready to serve” | Contract tests, selection and inference evidence | Unsupported by this table alone |

For each actual claim, record its exact wording, the source field or missing evidence, a verdict and a correction. A useful correction is bounded: “lowest validation RMSE among these controlled runs; activation still needs validation and serving checks.” This is more informative than marking the entire response good or bad.

## Watch out for

`verify_summary` checks numeric selection and limited controls; it cannot decide whether all natural-language caveats are true. Include human claim review. Record assistant access failures honestly and distinguish a saved reference exercise from a new request.

## Quick reference

| Evidence | Check |
|---|---|
| `runs.csv` | Fixed controls and raw values |
| `verify_summary(rows, run_id)` | Primary metric winner |
| `get_run(run_id)` | Source record |
| Claim table | Semantic accuracy and unsupported conclusions |

![Validating an assistant-generated experiment summary: evidence path](assets/validating-an-assistant-generated-experiment-summary__01__en.png)

## Validate an overclaim, not only a number

A response can name the correct winner and still be wrong. Split “run X has the lowest validation RMSE, so it is ready to serve” into two claims. The first can be checked in the selected raw rows. The second needs input-contract tests, active-version resolution and completion evidence absent from the run table. Mark that recommendation unsupported and name the missing proof; do not mark the entire response correct because its first number matches.

## Learner checklist

- I retained selected raw IDs, the actual prompt/response, the numeric check and a claim-by-claim corrected recommendation.
- I can name one failure and the evidence needed to diagnose it.

## Learning outcome

Direct an approved assistant to generate a summary comparison across logged experiment runs, validate every recommendation against the raw MLflow data and the declared primary metric, and flag any inaccuracy or invalid comparison.

## Summary

The assistant’s recommendation is now an inspectable set of claims. Your raw-data checks distinguish a valid metric choice from unsupported promotion advice.
