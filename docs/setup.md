# Local setup and troubleshooting

Use VS Code or your operating system's terminal. Install [Git](https://git-scm.com/downloads) and [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

Follow the complete sequence in the [README](https://github.com/richhiey/ml-llm-ops/blob/main/README.md): clone → locked environment → data inspection → training → evaluation → batch → Uvicorn → curl. It reproduces the guided pipeline walkthrough, with the same files, arguments and output paths.

## Environment

`uv sync --frozen` installs the committed dependency lock into `.venv`. The project selects Python `3.12.12`. Run commands from the repository root unless the archived-code replay explicitly opens a separate terminal in its extracted folder. CPU PyTorch wheels are selected on Windows/Linux; macOS uses the standard wheel with application tensors kept on CPU.

On macOS or Linux, activate the installed environment from the repository root:

```bash
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt, use `.venv\Scripts\activate.bat`. Each new terminal needs activation; restarting a service in an already activated terminal does not. The walkthrough shows the macOS/Linux command. Substitute your platform's activation command at that point. In VS Code notebooks, select `.venv` as the kernel.

If you have an older course clone, preserve personal work elsewhere and start with a fresh clone. An older environment does not establish this setup. Use a short writable path on Windows. If `uv` or Git is unavailable, check your terminal's path and reopen it after installation.

Activate `.venv` once in each terminal. After activation, run the tools directly. `python scripts/train.py` runs the named Python file. `uvicorn scripts.api:app` starts the web server. `curl` is a separate HTTP client already available on many systems. Use curl 7.76 or newer for `--fail-with-body`, and use `curl.exe` in Windows PowerShell.

## Data and retained outputs

Preparation downloads roughly 30 MiB, verifies original file hashes and records fixed partitions. Wait for it to complete before inspection or training. Repeated preparation verifies existing data. If a checksum fails, inspect the named damaged cache file before replacing it.

A training run retains `run.json`, `config.json`, `dataset.json`, `environment.json`, `history.json`, `model.pt`, `source.zip`, `metrics.json` and `validation-predictions.csv`. Source snapshots include the Python entry files in `scripts/` as well as reusable source and environment declarations.

Existing run, intake, request and batch destinations are protected. Resume by inspecting a retained result, or deliberately choose a new path for new work. Stop a running Uvicorn process with `Ctrl+C`; restart it after source edits so it loads the new implementation.

## Checks and optional notebook

```bash
pytest -q
```

The mechanics tests use explicitly synthetic fixtures. They check implementation behavior, not Fashion-MNIST quality. Your real-data training and evaluation establish model quality.

The [companion notebook](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/01-pipeline-and-extension.ipynb) offers full data-reading, CNN, evaluation and plotting implementations for optional inspection. Select this repository's `.venv` kernel in VS Code and prepare the baseline first. Learner attempt cells remain open.

## Resource expectations

Bounded batches and CPU execution are the default. On the author's Apple M4 with 16 GB RAM, the initial four-epoch run took about 10 seconds end to end and peaked below 700 MiB RSS. Downloads, installation, slower processors and concurrent applications affect total setup time. An 8 GB classroom computer is the target profile; hardware-specific verification is still pending.

Keep a few GB free for the environment, cached packages, dataset and retained runs.

## Archived-code replay and Windows shells

The registry walkthrough keeps the main project terminal at the repository root and opens a separate terminal for the archived code. That extracted project gets its own new `.venv`; activate the environment belonging to that folder once. Keep its interpreter/import paths and command outputs as execution evidence. Close the replay terminal when finished and return to the unchanged main terminal.

The walkthrough uses this native MLflow store setting at the repository root:

```bash
export MLFLOW_TRACKING_URI=sqlite:///work/mlflow/tracking.db
```

In PowerShell, replace that one line with:

```powershell
$env:MLFLOW_TRACKING_URI = "sqlite:///work/mlflow/tracking.db"
```

In Command Prompt, use `set MLFLOW_TRACKING_URI=sqlite:///work/mlflow/tracking.db`. Continue to substitute your platform's activation command and `curl.exe` where needed.

Evaluation uses `>` to retain its JSON output. macOS/Linux shells, PowerShell 7 and Windows Command Prompt can write the output without a UTF-16 conversion. In older Windows PowerShell, run the two archived evaluation redirects through Command Prompt instead. [Microsoft documents these encoding defaults](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-7.5).

```powershell
cmd /c "python scripts/evaluate.py --run ../recipe > ../saved-evaluation.json"
cmd /c "python scripts/evaluate.py --run ../retrained > ../retrained-evaluation.json"
```

Use a fresh replay destination before download/extraction/redirection; those native operations can overwrite existing files. Project training, verification and batch commands separately reject existing output destinations. These Windows equivalents document the intended route; the author receiving proof was run on macOS, not Windows hardware.

Use the quoted form `--data-binary "@work/intake/request.json"` shown in the commands. Quoting keeps the file argument literal in PowerShell as well as Bash. [PowerShell argument parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5) explains the initial `@` syntax. In Windows Command Prompt, replace the displayed `cp` command with `copy docs\course\exercises\test_intake_quality.py tests\test_intake_quality.py`. PowerShell supports `Copy-Item` (also available as `cp`).
