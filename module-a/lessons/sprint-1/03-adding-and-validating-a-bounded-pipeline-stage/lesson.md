📝
# Adding and validating a bounded pipeline stage

Linden Facilities receives `hour=24`, which is numeric but outside its planning contract. We will edit a starting validation stage, observe its missing behavior, add explicit rejection rules, and prove that valid predictions still work.

## Your route through this lesson

Make the source edit, test its contract and interpret before/after behavior. Run the explained blocks in order, pausing to compare each result with its interpretation. Use the local Python 3.12 setup or the linked Colab route. Terminal commands and notebook Python are different interfaces; the setup guide shows their equivalents.

**Finish with:** Changed project source, explained diff and passing contract/integration checks.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab workspace](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/00-learner-workspace.ipynb#scrollTo=stage-work). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Finished state and starting files

You will finish with a changed `pipeline.py`, an explained diff (the lines added or removed), a rejected invalid input and unchanged valid-data metrics. A **regression check** confirms that behavior outside the intended change still works. The reference helper remains intact; an editable project copy will carry your cumulative work. The worked notebook is an instructor reference, not a substitute for making this edit.

## Turn the contract into examples before editing

Linden accepts temperatures from `-30` through `50`, integer hours from `0` through `23`, and occupancy from `0` through `100`. All feature values must also be finite. “Finite” excludes missing values and positive/negative infinity; it does not exclude a numeric but impossible `hour=24`.

Write a prediction table before changing the source. Include an ordinary valid row, both hour boundaries, a fractional hour, an out-of-range occupancy, a missing feature and an infinite value. Record whether each should return an unchanged copy or raise `ValueError`. An **exception** stops normal execution and gives the caller a failure to handle. It is preferable to silently inventing a corrected supplier measurement under this contract.

| Property | How to distinguish it |
|---|---|
| Inclusive bounds | Boundary values accepted, values outside rejected |
| Integer hour | `1` accepted; `1.5` rejected despite being within bounds |
| No mutation | Original valid values/index unchanged after the call |
| Complete checking | Invalid occupancy rejected even when temperature/hour are valid |

The test and worked function below implement these decisions. The point is to connect each statement to a behavior you can test, rather than copy code because the final score looks normal.

## Use the same edit in Colab without a stale import

For local work, open the project folder in your editor and select that project's `.venv`. In the Colab learner workspace, create the incomplete project with `make_project('stage-project')`, open its printed `src/campus_mlops/pipeline.py` path in the file browser and make the same edit. The workspace's `project_python(project, code)` runs a **new Python process** using that project's `src`; it avoids reusing the reference module already imported by the notebook.

Use `project_python` to call `run_pipeline`, probe accepted/rejected rows and run the project CLI. Keep the earlier failing output. Do not replace the reference checkout's function or remove its source-pin assertion. The reference pin identifies supplied code; your edited project must record its own `code_revision()` when it logs a run. The notebook workspace includes the exact commands for invoking tests if pytest is available; the supported full locked test suite and fresh-environment proof remain the local route.

## 1. Create the incomplete starting project

From the reference helper folder, run:

```sh
uv run python exercises/make-stage-lab.py --destination ../project-helper
cd ../project-helper
uv sync --locked
```

For Colab, create this same starter with `project = make_project("stage-project")` instead of running the terminal block. Open the printed project path.

**Why:** this copy has a finite-only `validate_ranges` function, with domain rules deliberately absent. It also contains `expert-stage.patch` for comparison after the edit. Existing destination folders are rejected so work is not overwritten.

**Expected:** the setup prints the new project path. Open `src/campus_mlops/pipeline.py` there and confirm `validate_ranges` currently returns `validate_features(frame).copy(deep=True)`. All following commands run from this project folder, using its own environment.

## 2. Observe the missing rule before correcting it

Run the named test:

```sh
uv run pytest tests/test_spine.py::test_contract_extension_and_unchanged_pipeline -q
```

In Colab use `project_tests(project, "tests/test_spine.py::test_contract_extension_and_unchanged_pipeline", "-q", expected_returncode=1)`. The nonzero return is expected only for this deliberately incomplete stage.

**Why:** a failing-before example establishes what the addition must change. The test includes `hour=24`, accepted by the finite-only starter.

**Expected:** this deliberately incomplete starter fails with `DID NOT RAISE` for an invalid range case. This is the exercise's intended failure. Also run `run_pipeline(Config(range_guard=True))` in the project Python environment and record validation RMSE near `1.443003925` kWh: ordinary snapshot rows do not expose the defect.

## 3. Add the validation stage

Replace only `validate_ranges` in the project `pipeline.py` with this expert implementation:

```python
def validate_ranges(frame):
    """Bounded extension: reject invalid readings; never clip/drop/reorder valid rows."""
    validate_features(frame)
    for column, low, high in [("temperature_c", -30, 50), ("hour", 0, 23), ("occupancy", 0, 100)]:
        if not frame[column].between(low, high).all():
            raise ValueError(f"{column} outside [{low}, {high}]")
    if not (frame.hour % 1 == 0).all():
        raise ValueError("hour must be an integer")
    return frame.copy(deep=True)
```

**Why:** input validation should reject invalid measurements before feature extraction; it should not silently repair, drop or reorder rows. `validate_features` first checks the required finite numeric features. The loop applies inclusive lower/upper bounds to each field; `.all()` requires every row to pass. The remainder check rejects a fractional hour even when it lies inside `0..23`. The deep copy preserves the caller's valid table.

**Expected:** the function now contains all three ranges and the integer-hour condition. Check the indentation: `return` belongs after the loop, so all three fields are checked. No target, split, training or metric code changes.

## Read the control flow in the edit

`.between(low, high)` returns one Boolean per row, including the boundary values. `.all()` reduces those decisions to one answer: every row passes. `not ...` enters the exception branch when any row violates the rule. The loop moves to the next feature only if the current feature passes. A `raise` ends the call immediately, so the error names the first violation checked, not necessarily every defect in a mixed table.

The remainder expression `frame.hour % 1` distinguishes integer-valued hours from fractions. For `1.5`, the remainder is `0.5`; for `23`, it is `0`. The final copy is made only after all checks pass. Putting `return` inside the loop would stop after temperature and leave other columns unchecked.

These are input-validation rules. They do not change scaling, Ridge coefficients or the held-out rows. Ordinary snapshot data already satisfies them, which explains why the baseline metric can match before the new boundary is correct. An unchanged score is necessary regression evidence here, but it cannot replace invalid-input tests.

## 4. Connect the new boundary to the unchanged stages

Read `preprocess` directly below it. Its guarded branch already calls `validate_ranges(frame)` when `config.range_guard` is true; the unguarded branch remains the baseline. This is the bounded integration point.

In a Python session using the project environment, run the following block. In Colab pass the whole block as the code string to `project_python(project, code)` so its imports use your edited project in a new process; executing it directly in the reference kernel would test the wrong source:

```python
from campus_mlops import Config, ingest, run_pipeline, validate_ranges
import pandas as pd
raw = ingest()
pd.testing.assert_frame_equal(validate_ranges(raw), raw)
assert run_pipeline(Config())[1] == run_pipeline(Config(range_guard=True))[1]
bad = raw.copy()
bad.loc[0, 'hour'] = 24
try:
    validate_ranges(bad)
except ValueError as error:
    print(error)
else:
    raise AssertionError('Invalid hour was accepted')
```

**Expected:** valid rows/index/features remain equal, metrics are unchanged, and the invalid call prints `hour outside [0, 23]`. Test `hour=0`, `23`, `1.5`, a missing feature and a non-finite value too. The integer check and range check address different failures.

## 5. Verify the complete path and explain the change

```sh
uv run pytest -q
uv run campus-mlops bootstrap --state state-extension
```

In Colab run `project_tests(project, "-q")`, then `course_cli("bootstrap", "--state", str(state/"extension"), project=project)`.

**Why:** the focused test checks the boundary; the full tests and prepared bootstrap check unchanged training, tracking, registry and batch mechanics. Their registry setup is supplied infrastructure at this point.

**Expected:** the suite passes; bootstrap produces `24` predictions and a resolved version matching its registered version. Compare your edited function with `expert-stage.patch`. Explain each changed statement and its effect on an accepted and a rejected input.


## Watch out for

- An early `return` inside the loop validates only the first field. Test a bad `occupancy`, not just a bad hour.
- Clipping `24` to `23` hides a bad record; rejecting it preserves the contract.
- A finite-only check accepts `1.5`; an inclusive range check alone does too.
- Use the project environment after changing source. Published reference notebooks intentionally reject a different source pin. Use project CLI/tests for your extension; record its own source revision when tracking it.

## Quick reference

| Check | Evidence |
|---|---|
| Finite-only starter | Intended failing contract test |
| Edited `validate_ranges` | Range and integer-hour rejection |
| `preprocess(..., Config(range_guard=True))` | New boundary reached |
| Unguarded versus guarded run | Equal valid-data metrics |
| Full tests and bootstrap | Unchanged stages and batch output |

## Learner checklist

- I changed source in my project copy and can explain every statement.
- I observed an invalid input accepted before and rejected after.
- I checked exact boundaries, a fractional hour, invalid occupancy and missing/non-finite features.
- Valid rows and downstream results remain unchanged; the prepared batch completes.

![Bounded stage evidence](assets/adding-and-validating-a-bounded-pipeline-stage__01__en.png)

## Learning outcome

Follow an expert adding one preprocessing or validation stage to the provided pipeline, then verify its input/output contract and confirm that the unchanged stages still run.

## Summary

Linden's project now contains an actual validation-stage addition, supported by a failing-before case and passing contract/integration evidence. You can explain where it runs and why valid predictions stay unchanged.
