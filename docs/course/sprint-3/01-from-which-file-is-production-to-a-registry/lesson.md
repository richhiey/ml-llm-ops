🏷
# From "which file is production?" to a registry

Threadline Retail is the fictional online clothing shop whose staff check model suggestions for product categories. Its engineers have compared several training recipes for the same small convolutional neural network, or CNN. A recipe with a stronger validation score is useful only if the team can retrieve its exact saved model and establish which model is answering requests.

Imagine two folders both containing `best-model.pt`. One belongs to the original four-epoch recipe; the other belongs to the selected candidate. Renaming one file `production.pt` does not explain which experiment produced it, whether it passed the team's checks, or what a running service actually loaded.

A **consumer** is a prediction job or server that loads a model and uses it. A **model registry** keeps named models and numbered versions connected to their recorded experiments. It gives the team a shared way to identify a model and select which version a consumer should load.

# Give each saved model an address

An MLflow **run** records one execution of a training recipe. Its native logged model is the saved model retained by MLflow. Registering that artifact gives it a numbered version under a **registered name**, such as `threadline-catalog`.

| Identity | What it answers | Example meaning |
|---|---|---|
| Run ID | Which training execution produced this result? | One execution of the eight-epoch recipe |
| Logged-model address | Which native saved model belongs to that run? | The model URI returned when MLflow logged it |
| Registered name | Which application model are we managing? | `threadline-catalog` |
| Version | Which registered artifact do we mean? | Version `1` under that name |

A **URI** is an address used by a tool to find something. `models:/threadline-catalog/1` asks MLflow for that exact registered version. Version numbers are local counters under a name; version `2` does not mean better quality than version `1`.

This solves the first file-saving problem: the team can identify and retrieve a particular model without guessing from its filename. It still needs the underlying artifacts and their content fingerprints to check that the retrieved bytes match the recorded result.

# Separate review status from selection

A **tag** is a named piece of information attached to a model version. Here, `validation_status=pending` means its checks have not yet been accepted. `validation_status=passed` means the declared clean-replay checks passed. That scope establishes repeatability; suitability for the catalog brief still depends on its quality requirements. The version also retains the address and fingerprint of its validation evidence.

An **alias** is a movable name pointing to a version. Our alias `active` identifies the version a newly started consumer should load. Assigning this alias is the course's **promotion** operation: selecting the reviewed model for this local application.

| Registry information | Meaning | What it does not establish alone |
|---|---|---|
| `validation_status=passed` on version `1` | The declared validation evidence passed | That version `1` is currently selected |
| `active` points to version `1` | A new consumer resolving `active` is directed there | That every existing service has reloaded it |
| Consumer reports loaded version `1` | That process actually loaded version `1` | That a later alias change changed its memory |

The distinction matters to catalog staff. A service loads a model into memory at startup and keeps using it. Changing the alias affects the next model-loading operation; it does not reach into every running process and replace its learned weights.

Our reviewed selection command requires passed evidence and checks which version the alias currently points to against the expected previous version. MLflow's native API can also assign aliases directly. Tags describe status; they do not automatically prevent someone from selecting a pending version through another route. You will inspect both the intended selection and the identity a consumer reports. [MLflow aliases, tags and model loading](https://mlflow.org/docs/3.5.1/ml/model-registry/workflow/#deploy-and-organize-models-with-aliases-and-tags)

# Keep enough history to explain a change

The third problem is explaining how the selection changed. An **audit trail** records what happened so another person can inspect it: who acted, when, why, which version was selected before and after, and whether the operation completed or failed.

The local project records those details for its reviewed registry commands. It also reads the alias back from MLflow after changing it. A current registry screen and a mutable local journal are different evidence: the screen shows current state, while the journal records the operations that passed through our commands. An outside native change can bypass that journal. Keep separate incident evidence and compare the journal with live registry state.

A **rollback** selects a previously approved version again after a bad selection. The team should retrieve that version's evidence, reassign `active`, and check a fresh consumer. Deleting the bad version would remove information needed to explain the incident.

# Recognize older stage-based examples

Older MLflow material uses fixed stages named `Staging`, `Production` and `Archived`. That model-stage API is deprecated. Current workflows use aliases, tags and, where environments need separation, different registered model names. A test environment is still a useful concept; the superseded part is MLflow's fixed stage field. [MLflow migration from stages](https://mlflow.org/docs/3.5.1/ml/model-registry/workflow/#migrating-from-stages)

| Older stage vocabulary | Current way to express the need |
|---|---|
| `Staging` | A review tag and a model in a test environment |
| `Production` | A selected alias in the intended environment |
| `Archived` | A retirement tag and retained historical artifacts |

For example, `threadline-catalog-dev` and `threadline-catalog-prod` could identify separate environment-specific models. Those names are illustrative; this local project uses one registered name. Names alone do not configure access controls.

# Selection still needs observation

Even the correct saved model can struggle when incoming images change. **Data drift** means the incoming data distribution changes; for example, thumbnails may become darker. **Prediction drift** means the distribution of suggested categories changes. Neither observation tells us by itself whether the suggestions became less correct.

Known category labels let us calculate actual quality, such as macro F1, the equal-weight average of the ten category F1 scores. We will compare incoming image groups under the same model, inspect changes, and use labels when available before choosing a response. A changed input-export setting and a wrongly selected model require different investigations.

# Check for Understanding

Consider this deliberately constructed incident: version `1` has passed validation, an outside native command points `active` to pending version `2`, and an already-running service reports loaded version `1`.

Prepare a short recovery note. Identify what a newly started consumer would load, whether editing version `1`'s tag alone would restore selection, and what evidence would show that a replacement service loaded the intended version. State one limit of the local audit trail.

<details>
<summary>Solution</summary>

**Result you should get**

A new consumer resolving the current alias would load version `2`. Tagging version `1` does not move the alias. Restore the previously approved selection, then check that a fresh consumer reports version `1` and its recorded model identity. The old service's version `1` report does not prove that the alias was repaired.

**How**

Read review status, selected alias and loaded identity separately. Record the native incident and the recovery action. Compare the live alias with the reviewed command journal; an outside change can be absent from that journal.

</details>

## Learning outcome

Explain 3 problems a model registry solves that ad hoc file-saving does not - versioning, alias/tag-based lifecycle control, and auditability - and recognise staging, production, and archived as superseded stage vocabulary replaced by aliases, tags, and environment-specific registered models.

## Summary

Threadline can now name the exact saved model, distinguish review status from selection, and investigate how a selection changed. Checking the version a consumer actually loaded closes the gap between a registry decision and the suggestions staff receive.
