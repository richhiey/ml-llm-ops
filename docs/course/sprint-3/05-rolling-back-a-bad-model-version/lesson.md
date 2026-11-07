✂️
# Rolling back a bad model version

Threadline's catalog staff report less reliable category suggestions even though the prediction service still answers requests. You will construct a real native alias change to a different unapproved candidate, bypassing the reviewed selection command. The author reference uses the lower-scoring translation candidate. You must restore the previous approved model and prove what both the registry and its consumers are using.

The **active alias** is the registry's movable selection. A running consumer keeps the version it loaded at startup. The **audit trail** is the local record of reviewed operations; an outside native change can be missing from it.

# Starting state

Keep the approved version, its passed replay evidence and the original current-cohort observations from the guided work. Use your actual approved version number. Choose a distinct completed candidate with a lower comparable primary score than the approved selection; check your own raw evidence first. Use translation if it satisfies those conditions. Do not call it worse solely because it was worse in the author study. The following course fixture performs a real native registry change; it does not modify the model files or manufacture predictions. Inspect its [visible implementation](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/exercises/introduce_alias_incident.py) before execution.

```bash
python docs/course/exercises/introduce_alias_incident.py --name threadline-catalog --bad-run-id BAD_CANDIDATE_ID --expected-approved APPROVED_VERSION --output work/rollback/incident.json
```

Retain the returned incident record. It records the previous version, newly active version, source run and pending review status. Inspect live registry state and compare it with the local journal. Do not assume the largest version number is the approved target.

# Your task

Before changing the alias, start the familiar registry service on port `8000` in a new activated terminal. It must start **after** the incident so it genuinely loads the bad version. Save its `/health` result and an actual `/predict` response. HTTP success means the request ran; it does not establish classification quality.

Create a new registry batch for the same current-image manifest used by the approved model. Retain its labeled observation and compare it with the earlier approved current observation using `compare_model_quality.py`. That comparison requires identical image bytes, order and known labels. Explain the observed quality change without confusing it with a change in incoming images.

Use the existing reviewed alias-assignment operation to restore the previously approved version. Inspect `assign_alias.py --help`: `--rollback` additionally requires recorded previous selection evidence. Supply the actual currently active bad version as the expected current value, the target's retained validation report, your role and an operational reason.

Retain the live alias readback and journal events. Then check the still-running service on port `8000`. Start a fresh registry service on port `8001`, using the same visible deployment file, and inspect its health and a real prediction response. The old and fresh processes can temporarily report different loaded versions even after the alias is correct.

Finally, run a fresh batch on the unchanged current manifest. Match the restored model identity and predictions against the original approved delivery. Stop both local services after saving their evidence.

# Produce an incident note

Save `work/rollback/incident-note.md` with the observed before/after alias, source runs and model fingerprints; the quality evidence; the target's approval evidence; the actual rollback command and reason; and the loaded identities from the old and fresh consumers.

State exactly what the local audit captured. Identify the separate fixture record that explains the bypassed native change. Include any failed or incomplete operations rather than presenting only a cleaned success story. A mutable local journal is not an immutable record of every possible registry action.

# Hints

<details><summary>Hint 1</summary>

Start with the prior approved selection and its evidence, then inspect the live alias. Registration order and the filename `best` cannot identify the recovery target.

</details>

<details><summary>Hint 2</summary>

Use different output destinations for bad and restored deliveries. The same image manifest lets you distinguish a model change from a different sample of products. Both labeled observations are needed for measured quality.

</details>

<details><summary>Hint 3</summary>

The native operation underneath recovery is still `client.set_registered_model_alias(name, alias, version)`. The reviewed file adds expected-current, approval and retained-evidence checks and records the action. A failed expected-current check means you must inspect actual state, not guess another version number.

</details>

# Checkpoints

The bad model must genuinely be active and consumed before recovery. The restored target must have passed evidence and a recorded earlier selection. The journal must record the actor, time, reason, previous/target version and terminal status, while the live alias confirms the resulting state.

A matching category prediction on one image cannot prove which model was loaded. Check version, source run and model fingerprint. A still-pinned old service is evidence to explain, not a reason to falsely report that rollback failed or automatically replaced its memory.

Only after completing the attempt, open the reference feedback.

<details>
<summary>Reference feedback</summary>

**Result you should get**

The alias again selects the previously approved model, and a fresh consumer identifies that artifact. The process started under the bad selection remains pinned until restarted. The reviewed recovery is present in the local journal; the separate native incident is explained by its own record.

In the author reference, the translation model reduced macro F1 by about `10.1` percentage points on exactly the same current images and labels. The restored delivery matched the original approved predictions. Your own raw observations and identities are the evidence for your incident.

**How**

Trace approval → previous selection → actual bad selection → observed bad consumption → reviewed reassignment → fresh restored consumption. Keep incoming bytes fixed for the paired model comparison. Read both live registry state and the recorded operations, and preserve the limitation that outside native changes can bypass the local journal.

</details>

## Learning outcome

Reassign the active-model alias from a bad version to the previous approved version, and document what the registry audit evidence captured during the rollback.

## Summary

Threadline's recovery is supported by an actual registry change, retained approval and observations from the consumers. The incident note explains both the restored selection and the old process that still needed replacement.
