# Start the Module A learning path

Linden Facilities needs one complete file containing 24 hourly energy-demand estimates within 60 seconds. You will make the pipeline understandable, extend a validation boundary, compare controlled runs, manage a selected model and hand over a result another engineer can rebuild.

The [Campus learning path](../lessons/README.md) contains the 26 lessons in order. Each concept note develops a mental model, each walkthrough demonstrates a mechanism, each practice leaves decisions to you, and each checkpoint asks you to transfer the taught work to Harbor's acceptance conditions. Keep one editable project across the sprints. Module B is independent.

## Choose your execution route

| Work | Local Python 3.12 | Hosted Colab Python 3.12 |
|---|---|---|
| Read/explain the concepts | Read the lesson; code inspection optional | Same lesson; no runtime required for conceptual reading |
| Follow guided Python work | Four guided notebooks using the locked environment | Open the corresponding guided Colab notebook |
| Investigate independently | A new learner workspace or a script in your project | A copy of the unsolved learner workspace |
| Edit and validate the stage | Edit the project source and run its tests/CLI | Edit the project source; run probes/tests in a new subprocess |
| Compare in the MLflow UI | Local server, browser and selected local IDs | Recreate a local matrix for the required UI work |
| Prove a fresh-environment handoff | New source folder, locked environment and new store | Hosted replay is useful; final fresh-environment proof uses the local route |

Read [Colab runtime and persistence guidance](colab.md) for the hosted limits. No provider key is needed for the pipeline. The assistant-summary activity uses your institution-approved assistant; its recommendation must be checked by you.

## Local setup, from an empty folder

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use Python 3.12. In a terminal:

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops/module-a
uv sync --locked --python 3.12
uv run pytest -q
uv run python -c "import sys, campus_mlops; print(sys.executable); print(campus_mlops.__version__)"
```

The repository folder containing `pyproject.toml` is the reference package root. `uv sync --locked` builds `.venv` from the supplied dependency lock. Expected package version is `0.1.1`; the tests should pass. Record the observed test result. Do not proceed by editing expected values when setup differs.

Open a notebook in an editor and select this `.venv/bin/python` as its kernel. A **kernel** is the Python process that keeps notebook variables and imports alive. Run cells in order. For a plain interactive Python session, run `uv run python` from the project root; Python blocks in lessons go there. Shell blocks go in the terminal.

## Colab setup

Use the [notebook index](../notebooks/README.md). Start a fresh CPU/Python 3.12 runtime and run the setup cell first. It clones a specific source commit and installs the declared dependencies. Check the printed helper version, commit and temporary state path. The source-content assertion protects the supplied reference code.

Use guided notebooks for demonstrations. For independent work, open **00 — Learner workspace** and make a copy for your investigation. Its setup creates no training runs, comparisons, registered versions or rollback solution. The lesson supplies your mission; you add code/Markdown cells and keep your decisions and observations there. Running a solved reference from top to bottom is not a substitute for your practice.

## Keep the reference and your project separate

For the actual stage edit, create an intentionally incomplete copy. Locally, from the reference package root:

```sh
uv run python exercises/make-stage-lab.py --destination ../project-helper
cd ../project-helper
uv sync --locked
```

In the Colab learner workspace:

```python
project = make_project('stage-project')
print(project / 'src/campus_mlops/pipeline.py')
```

Open that printed file in the notebook file browser and edit the function described in the lesson. The starter has finite-value checks but lacks the required domain ranges. Its focused test intentionally fails until your change is correct. Keep the before-result, source diff and after-result.

Do not overwrite the reference package or remove its pin assertion. A changed project has its own source-content hash. Inspect and execute the edited project, not a reference function already imported in memory.

## Translate terminal work into Colab subprocess work

The learner workspace imports these small execution helpers from `learning/workspace.py`. They launch processes; pipeline behavior remains in `campus_mlops`.

| Terminal task | Learner-workspace equivalent |
|---|---|
| `uv run campus-mlops bootstrap --state state-trace` | `course_cli('bootstrap', '--state', str(state/'trace'))` |
| Run Python against edited project | `project_python(project, "from campus_mlops import Config, run_pipeline; print(run_pipeline(Config(range_guard=True))[1])")` |
| Run project CLI | `course_cli('bootstrap', '--state', str(state/'edited'), project=project)` |
| Focused test expected to fail before edit | `project_tests(project, 'tests/test_spine.py::test_contract_extension_and_unchanged_pipeline', '-q', expected_returncode=1)` |
| Full tests after edit | `project_tests(project, '-q')` |
| Prepare an unsolved incident | `prepare_case('rollback', state/'rollback', project=project)` |

The workspace installs the pinned pytest version in hosted mode before you create runs. These helpers use the current interpreter/dependencies and the selected project's `src` in a new process. They establish that edited source executed; they do not build a new locked environment. The final recovery activity uses `uv sync --locked` in a genuinely new environment.

`course_cli` and `project_python` return a `CompletedProcess`; its `.stdout` retains output for inspection, and CLI JSON can be read with `json.loads(result.stdout)`. An unexpected nonzero exit raises an error. Use the expected failure return code only for an intentionally failing probe; never change it to hide an unexplained failure. Start the UI separately in a local terminal.

## Carry evidence forward without carrying hidden state

Save the editable source, pre-run matrix, actual run-ID list, chosen configuration, claim review, model/version records and original manifest. A `Workspace(path)` reopens a store at that path; a new path creates another store. Display names and version counters can repeat across stores, so retain the absolute state path with their IDs.

A guided notebook creates a fresh temporary state each time setup runs. Rerunning setup midway changes which variables point to which store. Preserve evidence and reopen its explicit path instead of assuming a variable still refers to an earlier execution. Colab runtime deletion removes temporary source/state; download the edited project and exported artifacts before ending it. Notebook output text is not a replacement for their files.

The final handoff names the source/data/configuration/environment, actual artifacts, exact command, lineage comparisons and result tolerance. Follow [clean-state recovery](clean-state.md) for that stronger proof. A source archive recovers the training package and tests; use the full repository for lesson assets and notebook learning tools.
