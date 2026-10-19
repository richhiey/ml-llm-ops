# Run the course locally

Set up once, then use **one notebook per sprint**. Keep your code, decisions and checkpoint answers in that notebook. Campus notes explain the same work; they do not require another copy or a second set of exercises.

## 1. Install and open

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run in a terminal:

```sh
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops/module-a
uv sync --locked --python 3.12
```

Open the sprint notebook in VS Code or your notebook editor. Select `module-a/.venv/bin/python` as its kernel, then run cells in order. The environment includes `ipykernel`. A kernel is the Python process that retains your notebook variables. If imports fail, check the selected interpreter before installing other packages.

## 2. Learn and keep your work

Start at [the four sprint notebooks](../README.md). In Sprint 1, follow its six numbered sections in order; the code-review and supplier cells are for your own attempt. The other sprint notebooks use guided examples followed by **Your turn** and **Sprint checkpoint**. Each sprint builds one project; reuse earlier outputs instead of repeating them for every Campus page.

Sprint 1 setup creates a retained local session under the printed `module-a/work/` folder, with `project/` and `outputs/` inside it. Later reference notebooks currently use temporary output folders. Save your notebook **and** its project/output folder. Sprint 1 creates an editable project with an intentionally incomplete guard; its first focused test should fail. The guided edit fixes it; the same focused test and complete batch path should then pass. Keep the printed project path for later work.

The reference package is pinned. The validation walkthrough loads the saved guard as `project_guard` for direct input probes; reload that cell after changing the source. Run edited project integration code through `project_python`, `project_tests` or `course_cli(..., project=project)`, which use a fresh process and your project's source. This avoids stale notebook imports. For example:

```python
project_tests(project, '-q')
project_python(project, "from campus_mlops import Config, run_pipeline; print(run_pipeline(Config(range_guard=True))[1])")
```

## 3. Open MLflow when the activity asks

The tracking notebook prints its UI command. Run it in a separate terminal from `module-a`, prefixed with `uv run`, and open `http://127.0.0.1:5050`. Use the actual printed state path, which contains your five run IDs. Stop the server with Ctrl+C when finished.

The final receiving task uses a new source folder, locked environment and tracking store. Follow [fresh-environment recovery](clean-state.md) at that point; a new notebook store alone is a smaller check.

## Optional: use Colab

The four sprint links open the same GitHub notebooks. Choose CPU and runtime version **2026.07** (Python 3.12), then run setup first. It installs the pinned source and dependencies. If it requests a restart, choose **Runtime → Restart session**, then run again; do not delete the runtime during setup. Save your own notebook copy only when you want to keep edits. The course does not require extra Drive copies per lesson.

Use local execution for MLflow UI work and the final fresh-environment check. Hosted temporary files disappear when a runtime is deleted. Local notebooks are the verified route; hosted execution is optional.
