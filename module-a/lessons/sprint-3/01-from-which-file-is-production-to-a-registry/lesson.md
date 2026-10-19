🏷️
# From "which file is production?" to a registry

Linden Facilities has `model-final.pkl` and `model-final-new.pkl`. The planner cannot tell which is active, which passed validation or which run created either file. A filesystem name is carrying three different meanings badly.

## Your route through this lesson

Separate artifact identity, validation, active selection and retained change evidence. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** An explanation of three registry benefits and correct interpretation of old stage vocabulary.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=registry-identities). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Separate four questions a filename cannot answer

Imagine two engineers hand you files both called `model-final.pkl`. They may contain different fitted objects. You cannot tell which was trained with which source, whether either passed the team's checks, or which one the batch job should load next. Renaming one `production` combines identity, validation and selection into a label without creating their supporting records.

A registry gives those questions separate places. The registered model name groups related versions. A version identifies an artifact associated with a source run. Tags record descriptive metadata, such as a validation decision and its rationale. An alias selects a version under a meaningful name such as `active`. The alias is allowed to move precisely because the version identities remain available for comparison.

## Give model identity and selection separate places

A **model registry** groups stable version identifiers under a registered model name. A **version** identifies a particular logged artifact and source run. An **alias** is a mutable name for a selected version. A **tag** is metadata describing a model or version, such as validation status.

| Ad hoc problem | Registry evidence | Linden example |
|---|---|---|
| Files overwrite or multiply | Distinct version identities | `dev.linden-demand`, versions `1`, `2` |
| Filename mixes approval with selection | Validation tags and active alias | `validation_status=approved`, alias `active` |
| Cannot explain the deployed artifact | Source run and artifact lineage | Version → run → source/data/config |

A registered version is not a training run. One run logs a model; registration creates a lifecycle identity for that artifact. The alias points to a version, not to a score.

## Follow an artifact into a selection

Consider an illustrative sequence; version counters depend on the actual store. A training run logs a fitted scaler and estimator under a model URI. Registration creates version 1 pointing to that logged artifact and records the source run. After validation, the team selects version 1 with `active`. A later run becomes version 2. Registering version 2 alone does not change the alias; the next batch should still resolve version 1 until a selection is explicitly made.

| State after an action | What is now true | What is not implied |
|---|---|---|
| Model logged | An artifact belongs to a run | It has a registered lifecycle version |
| Version registered | The registry can identify it | It passed validation |
| Validation tags recorded | A decision and rationale are visible | The tests necessarily ran |
| `active` assigned | Future alias resolution selects it | A job already in progress reloads it |

These distinctions are useful during failure. A candidate can remain registered and inspectable even when it is rejected. A rollback can move `active` back without retraining or deleting either artifact.

## Approval is a policy, not a magic label

The helper registers a pending version, records validation rationale, then permits activation only for approved versions. MLflow itself allows metadata changes; the scaffold supplies the teaching policy. A manually typed tag cannot prove that its tests actually ran.

`active` is resolved at the beginning of each batch job, then the job loads the fixed version. Changing the alias affects the next job. It does not retrain or delete anything.

## Read old stage vocabulary without carrying forward its assumptions

Older examples may move a version through `Staging`, `Production` and `Archived`. The current workflow uses aliases and tags, and separate registered models when environments need separate organization or control. An alias is a named reference; a validation tag records a decision. Neither word alone creates permissions, deployment processes or immutable storage.

Our registered name `dev.linden-demand` expresses a local teaching convention. A real organization would need to configure its storage, access and deployment boundaries separately. When reading an older tutorial, translate its intended selection and validation behavior rather than copying a stage label and assuming it performs that behavior.

## Current state and history answer different questions

A registry lookup can tell you what `active` points to now. After a rollback, that same lookup cannot explain what it pointed to earlier or why it changed. Linden's helper therefore writes an application event containing the prior version, selected version, source run, time and reason.

That event is evidence of a helper-mediated change. A direct registry edit can bypass it, and the local JSONL file can be modified. The lesson is to connect current selection, source lineage and retained change evidence, while describing the limits honestly. A registry solves organization and traceability problems; it does not make every operational guarantee automatic.

## Separate identity from integrity

A stable version number helps identify an artifact; it does not make your local artifact storage immutable. Registry metadata can change and versions can be deleted. Keep the source run, recoverable artifact and validation record together. The name `dev.linden-demand` expresses this course's environment convention; a name alone does not create access isolation.

Compare the meanings: a run ID identifies an execution; `models:/m-...` identifies an MLflow 3 logged model; `models:/dev.linden-demand/2` identifies a registered version; `models:/dev.linden-demand@active` asks for the current alias selection. Do not substitute these identifiers in a handoff.

## Check for Understanding

A colleague registers a new version and immediately announces that tomorrow’s batch will use it. The old version still has `active`. Explain which claim is unsupported, what to inspect and which separate decision must be made before the new version can serve.

▶️ **Solution** *(toggle)*

> **Result you should get:** registration alone has not moved `active`; a new job still resolves the old selection. Inspect current alias and candidate validation/source-run evidence.
>
> **How:** distinguish artifact identity from validation and selection. Validate the candidate under the policy, explicitly assign the alias, then inspect a newly executed batch’s resolved version and source run.

## Learning outcome

Explain 3 problems a model registry solves that ad hoc file-saving does not - versioning, alias/tag-based lifecycle control, and auditability - and recognise staging, production, and archived as superseded stage vocabulary replaced by aliases, tags, and environment-specific registered models.

## Summary

Linden can distinguish a model’s version identity, its validation evidence and the mutable selection used by inference. Those separate records also make rollback questions answerable.
