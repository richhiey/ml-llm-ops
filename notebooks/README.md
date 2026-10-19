# Four exploration notebooks

Use the [repository setup](../docs/setup.md) and select its Python 3.12 kernel. The [Campus journey](../docs/course/README.md) also works directly from the terminal and Python API; notebooks are optional.

1. [Pipeline and extension](01-pipeline-and-extension.ipynb): trace stages, follow a bounded edit and inspect new inputs.
2. [Tracking and evidence](02-tracking-and-evidence.ipynb): declare five runs, compare logging and save an explicit choice.
3. [Registry and reproduction](03-registry-and-reproduction.ipynb): promote that choice and investigate isolated incidents.
4. [Cumulative handoff](04-cumulative-handoff.ipynb): scope gaps, export the selected recipe and test recovery.

They share this source tree and `work/project.json`. Keep the clone and local files between sprints. A fresh kernel resumes recorded decisions instead of creating a new baseline. Complete independent cells yourself, reuse existing evidence and keep one set of working notes. There is nothing to submit.

Hosted exploration can use the same GitHub notebooks with a Python 3.12 runtime. Save local source/work files before ending temporary runtimes. MLflow UI and fresh-environment receiving checks use local execution. No hosted upload is required.
