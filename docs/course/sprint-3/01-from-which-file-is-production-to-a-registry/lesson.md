🏷️
# From "which file is production?" to a registry

Linden Facilities has `model-final.pkl` and `model-final-new.pkl`. The planner cannot tell which is active, which passed validation or which run created either file. A filesystem name is carrying three different meanings badly.


Read this explanation alongside the [repository setup](https://github.com/richhiey/ml-llm-ops/blob/main/docs/setup.md). Use your existing project evidence for the checks; no new model execution is needed.

## Give model identity and selection separate places

A **model registry** groups stable version identifiers under a registered model name. A **version** identifies a particular logged artifact and source run. An **alias** is a mutable name for a selected version. A **tag** is metadata describing a model or version, such as validation status.

| Ad hoc problem | Registry evidence | Linden example |
|---|---|---|
| Files overwrite or multiply | Distinct version identities | `dev.linden-demand`, versions `1`, `2` |
| Filename mixes approval with selection | Validation tags and active alias | `validation_status=approved`, alias `active` |
| Cannot explain the deployed artifact | Source run and artifact lineage | Version → run → source/data/config |

A registered version is not a training run. One run logs a model; registration creates a lifecycle identity for that artifact. The alias points to a version, not to a score.

## Approval is a policy, not a magic label

The helper registers a pending version, records validation rationale, then permits activation only for approved versions. MLflow itself allows metadata changes; the scaffold supplies the teaching policy. A manually typed tag cannot prove that its tests actually ran.

`active` is resolved at the beginning of each batch job, then the job loads the fixed version. Changing the alias affects the next job. It does not retrain or delete anything.

## Read old stage vocabulary without carrying forward its assumptions

Older examples may move a version through `Staging`, `Production` and `Archived`. The current workflow uses aliases and tags, and separate registered models when environments need separate organization or control. An alias is a named reference; a validation tag records a decision. Neither word alone creates permissions, deployment processes or immutable storage.

Our registered name `dev.linden-demand` expresses a local teaching convention. A real organization would need to configure its storage, access and deployment boundaries separately. When reading an older tutorial, translate its intended selection and validation behavior rather than copying a stage label and assuming it performs that behavior.

## Current state and history answer different questions

A registry lookup can tell you what `active` points to now. After a rollback, that same lookup cannot explain what it pointed to earlier or why it changed. Linden's helper therefore writes an application event containing the prior version, selected version, source run, time and reason.

That event is evidence of a helper-mediated change. A direct registry edit can bypass it, and the local JSONL file can be modified. The lesson is to connect current selection, source lineage and retained change evidence, while describing the limits honestly. A registry solves organization and traceability problems; it does not make every operational guarantee automatic.

## Check for Understanding

A colleague registers a new version and immediately announces that tomorrow’s batch will use it. The old version still has `active`. Explain which claim is unsupported, what to inspect and which separate decision must be made before the new version can serve.

<details>
<summary>Check your diagnosis after attempting it</summary>

> **Result you should get:** registration alone has not moved `active`; a new job still resolves the old selection. Inspect current alias and candidate validation/source-run evidence.
>
> **How:** distinguish artifact identity from validation and selection. Validate the candidate under the policy, explicitly assign the alias, then inspect a newly executed batch’s resolved version and source run.

</details>

## Learning outcome

Explain 3 problems a model registry solves that ad hoc file-saving does not - versioning, alias/tag-based lifecycle control, and auditability - and recognise staging, production, and archived as superseded stage vocabulary replaced by aliases, tags, and environment-specific registered models.

## Summary

Linden can distinguish a model’s version identity, its validation evidence and the mutable selection used by inference. Those separate records also make rollback questions answerable.
