🏷
# Why ad hoc tracking breaks down at scale

Threadline's first CNN finds many categories correctly, but its shirt recall is weak. The team now wants to investigate several changes. A score beside a filename will no longer be enough to explain which change helped.

The model, task and research images stay familiar. The new challenge is keeping each learning attempt connected to the conditions and evidence that produced it.

# A score loses its meaning when its context disappears

A **run** is one execution of a declared training configuration. An **experiment** groups related runs investigating the same task. Before choosing a candidate for catalog review, Threadline needs to answer: what changed, what stayed fixed and which saved weights achieved the reported result?

Consider these plausible record-keeping problems. They are teaching scenarios, not observed company incidents.

| Manual record | What can go wrong | What the team needs to retain |
|---|---|---|
| A notebook prints a better score | It may use a different split, metric or preprocessing | Data/split identity and evaluation conditions |
| A spreadsheet says “learning rate reduced” | The author may also have changed epochs | Complete configuration for every run |
| Several files are named `best-model.pt` | The selected score can become detached from its weights | An identified model artifact connected to its run |
| Someone copies a rounded value into a report | A transcription error or near tie can change the ranking | Raw metric values and their supporting predictions |
| A colleague leaves with the notebook | The team cannot retrieve the code or environment | Recorded, retrievable source and environment |

A spreadsheet can still help discuss findings. It is a weak sole source of truth when its entries are manually copied from changing code and outputs.

# Systematic tracking preserves the question and its answer

MLflow records **parameters** (settings such as epochs), **metrics** (observations such as validation macro F1) and **artifacts** (files such as predictions and learned weights). A run ID connects them. A metric can have a history: validation loss at each epoch, rather than only its final value.

This supports **auditability**: another person can inspect what happened and why the team made a decision. Tracking does not automatically make a comparison fair. A perfectly recorded run on another split still answers a different question.

Threadline will keep the original saved baseline as historical evidence. For the controlled study, it will freeze the current source after the intake work and confirm the baseline recipe under that source. Every candidate then uses the same controls. A new source version must be acknowledged rather than silently mixed into the study.

# Check for Understanding

You inherit a note saying “use the longer run,” an accuracy screenshot and two weight files with the same name in different folders. Prepare a short handoff request: identify at least three independent failure risks, the evidence you would retrieve for each, and what decision must wait until that evidence is available.

<details>
<summary>Solution</summary>

**Result you should get**

The handoff should request complete configurations, matching data/split and metric definitions, and a verified connection between the evaluated predictions and one retrievable model. It should withhold the model-selection decision until those conditions can be checked. Source and environment are also required to replay the result.

**How**

Separate “was a score observed?” from “which conditions and artifact produced it?” The screenshot supplies one observation, while a duplicate filename identifies neither weights nor configuration. Put each finding in a run record and compare only after checking the controls. A larger displayed accuracy cannot settle a macro-F1 decision.

</details>

## Learning outcome

Identify 3+ failure modes of tracking experiments manually (spreadsheets, notebook print statements) once a team runs many models, and explain why systematic tracking matters for auditability.

## Summary

Threadline can now specify the evidence each run must retain. The next decision is which changes form a fair experiment and which metric should choose between them.
