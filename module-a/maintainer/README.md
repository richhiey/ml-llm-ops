# Course maintenance

Students start at [Module A](../README.md). This folder contains source-alignment metadata, notebook generation and verification, kept outside their learning route.

From `module-a`:

```sh
uv run python maintainer/make_notebooks.py --source-commit COMMITTED_SOURCE_SHA
uv run python maintainer/execute_notebooks.py
uv run python maintainer/verify_learning_path.py
uv run pytest -q
```

Use an actual pushed source commit in the first command. Commit helper/API changes before regenerating notebooks; the setup pins that source. Notebook and Campus anchors are mapped in `learning-path.json`. All 26 source outcomes, types and ordering must stay exact. Add no extra notebook for a lesson.

[Final review](verification.md) · [Machine-readable checks](learning-path-verification.json)

For a focused revision, add `--sprint 1` (or 2–4) to notebook generation and execution. This preserves the other sprint files. Sprint 1 content is built in `sprint_one.py`; practice/assessment cells tagged `student-work` are intentionally unsolved and require a separate private feasibility rehearsal.
