📝
# Registering and promoting a model

Linden Facilities has selected a guarded run. We will give its artifact a registered version, attach validation evidence and make it the version used by the next batch.

## Your route through this lesson

Carry an actual run through pending registration, validation, active selection and new inference. Run the explained blocks in order, pausing to compare each result with its interpretation. Use the local Python 3.12 setup or the linked Colab route. Terminal commands and notebook Python are different interfaces; the setup guide shows their equivalents.

**Finish with:** Run/model/version/source-run chain, tags, active batch and application event.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=register-pending). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Before you start

Use the helper environment and [registry notebook](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb). A registered **version** links to a specific artifact and source run; the **active alias** is a mutable selection. The local registry shares the SQLite backend with tracking.

## Follow the three identities without guessing counters

The run ID identifies a training execution. The model URI identifies its logged fitted artifact. The registered version gives that artifact a lifecycle identity under `dev.linden-demand`. You will carry the returned run ID into `register`, then carry the returned version into approval and selection. These values are related; they are not interchangeable.

Make a small record with `run_id`, `model_uri`, `version`, `validation_status` and `active`. Fill it after each action. Registration should add a version without making it active. Approval should change validation metadata without moving the alias. Activation should select an approved version. Keeping those transitions separate makes a failed gate understandable.

## 1. Log a candidate and register its artifact

```python
from campus_mlops import *
from campus_mlops.lifecycle import MODEL_NAME
ws = Workspace('state-registry')
record = ws.run(Config(alpha=1, range_guard=True), name='candidate')
version = register(ws, record['run_id'])
print(version)
```

**Expected:** a version string, `1` in a new store. `register` uses the actual logged model URI, not a guessed filename. Check the version's `run_id` equals the recorded run.

## 2. Inspect pending validation state

```python
candidate = ws.client.get_model_version(MODEL_NAME, version)
print(candidate.run_id, candidate.tags)
```

**Expected:** `validation_status=pending`. An unapproved version must not become active through the helper. This makes the selection rule visible before promotion.

## Observe the policy boundary before approval

With the new version still pending, deliberately try selecting it:

```python
try:
    activate(ws, version, 'Probe: pending selection must fail')
except ValueError as error:
    print('Expected rejection:', error)
else:
    raise AssertionError('Pending version became active')
assert ws.client.get_model_version(MODEL_NAME, version).run_id == record['run_id']
```

**Expected:** `Only approved versions may be active`. The rejected attempt must not become a successful alias event. This is a helper policy: MLflow can store tags/aliases, while the course functions decide which combination is allowed.

Before approving, run the contract tests in your local project using `uv run pytest -q`, retain the result and inspect the raw validation metric. The helper's finite `<=5` gate and `range_guard=True` check are necessary conditions, but it does not execute those tests for you. A rationale should identify real validation evidence rather than repeat the word “approved”.

## 3. Record the validation decision

After running the contract tests, use:

```python
approve(ws, version, 'Contract tests passed; guarded validation RMSE <= 5 kWh')
print(ws.client.get_model_version(MODEL_NAME, version).tags)
```

**Expected:** `validation_status=approved` with a validation rationale. The helper checks guard and the numeric teaching gate; the rationale should point to your actual test record. Alpha `100` fails the reference 5-kWh gate, demonstrating why registration and approval are different.

## 4. Assign active and prove inference follows it

```python
event = activate(ws, version, 'Validated baseline selected')
output, evidence = batch_predict(ws)
print(event)
print(evidence)
```

**Expected:** `new_version` and `resolved_version` match `version`, with `24` output rows. Inspect `state-registry/audit.jsonl` and `batch.json`. An alias update by itself is insufficient evidence that inference loaded the intended artifact.

## Verify the complete lineage after selection

After activation and batch inference:

```python
selected = ws.client.get_model_version_by_alias(MODEL_NAME, 'active')
registered = ws.client.get_model_version(MODEL_NAME, version)
assert str(selected.version) == str(version) == evidence['resolved_version']
assert registered.run_id == record['run_id'] == evidence['run_id']
assert len(output) == 24
print(registered.tags['validation_status'], event['reason'])
```

**Expected:** `approved` and your selection reason, with every identity comparison passing. The first chain proves which version the new job resolved. The second connects that version to the trained artifact's source run. A matching version number in a different store would not be the same evidence, which is why all operations use the same workspace.

Read the last line of `ws.path/'audit.jsonl'`. It should name the selected version, source run and reason. In a new store the previous version is absent; in a reused store it may be another version. Keep that observed value instead of editing the event to match a sample.

Finally, explain the stopping point for a candidate whose validation error exceeds the teaching gate: it may be logged and registered, but approval should fail and activation must not follow. Its artifact remains useful failure evidence.

## Watch out for

Version numbers depend on existing state. Do not substitute an assumed `1` for the returned value. A validation tag describes an approval; it does not run the tests. A job already holding a model object does not automatically reload it after alias reassignment.

## Quick reference

| Operation | Result |
|---|---|
| `register(ws, run_id)` | Pending version |
| `approve(ws, version, rationale)` | Validation tags |
| `activate(ws, version, reason)` | Active alias and helper audit event |
| `batch_predict(ws)` | Resolved version plus outputs |

![Registering and promoting a model: evidence path](assets/registering-and-promoting-a-model__01__en.png)

## Pause before promotion

Before `approve`, locate the raw validation metric and the test record you are citing. The function checks a finite validation score, enabled guard and rationale; it does not execute your contract tests on your behalf. After activation, look up `ws.client.get_model_version(MODEL_NAME, version).run_id` and compare it with both `record['run_id']` and `evidence['run_id']`. These links make the promotion decision inspectable.


## Learner checklist

- I observed pending/approved tags, the returned version, matching active batch/source run and an audit event.
- I can name one failure and the evidence needed to diagnose it.

## Learning outcome

Use the provided model registry scaffold to register a new model version, record its validation status with tags, and promote it by assigning the scaffold's active-model alias.

## Summary

The candidate has moved from a logged artifact to a tagged version and a verified active batch. Each lifecycle action now points back to the same source run.
