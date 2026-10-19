# Four-sprint learning-path verification

Reviewed 19 October 2026. Students use exactly four notebooks, one per sprint. The [Campus notes](../lessons/README.md) provide explanations and activity briefs for the same work; guided execution, independent work and the checkpoint share each sprint file. Instructor materials remain in the private course-authoring workspace.

## Current checks

- Sprint 1 was rerun in a fresh local Python 3.12 kernel: **11 guided cells plus two unsolved student-work templates**, no unexpected errors. A separate private copy rehearsed both independent tasks. Sprints 2–4 retain their unchanged earlier execution records (eight code cells each). Running empty templates is not independent-task evidence.
- Earlier helper verification passed **6 tests**. This content revision changes no helper code; the Sprint 1 focused contract test and saved-project full batch path were verified before/after the stage edit.
- All **26 outcomes, types and positions** match the authoritative CSV through the private draft checker. Notebook sections and resource links are checked by `uv run python maintainer/verify_learning_path.py`; see [results](learning-path-verification.json).
- The experiment plan appears before the matrix executes. The logging comparison reuses its alpha=1 autologged run and adds one logging-off run. Checkpoints reuse the same sprint work.
- Reference package 0.1.1 remains pinned to source commit `f1ae85914f49a4f1c4bdd6a0ca62c4c4076158ea`. Its pipeline, data and lock are unchanged. Notebook generation lives here, away from the learner entry route.

## Earlier core-scaffold evidence

[Verification metadata](verification.json) records current checks separately from the earlier source/archive, editable-project and fresh-environment rehearsals. Their full transcripts remain in the authoring workspace. The fresh-source/environment/store handoff matched source/data/config/environment/partition, reproduced with RMSE delta 0.0 kWh within 1e-6, and produced 24 predictions within 60 seconds. These are prior core-scaffold results, not a new hosted execution claim for the four consolidated notebooks.

## Limits

Local execution is the verified route; hosted Colab browser execution of the consolidated notebooks and learner trials remain unverified. [Setup](../docs/setup.md) explains local and optional Colab execution, and [clean recovery](../docs/clean-state.md) covers the final receiving task. A notebook replay uses the current environment and does not replace a fresh locked environment. UI comparison and assistant claim review require the learner's actual work. Synthetic scores and local SQLite/JSONL records do not establish production forecasting or immutable auditing.

## Sprint 1 learning-route review

The six Campus activities now map to six ordered notebook sections. The trace uses supplied delivery infrastructure; the student adds and explains one guard, investigates a separate proposed change, then reuses its integration evidence for the delivery recommendation and new-client checkpoint. No endpoint build, registry configuration or fresh-environment assignment is added. Work persists under the ignored local `work/` folder. Current execution/route metadata distinguishes guided cells from unsolved student templates. Human learner trials remain pending.
