# Local setup

Use a terminal in VS Code or your operating system's terminal. Install Git and `uv` first using their official instructions. Python is managed by the project's `.python-version` file. [Git downloads](https://git-scm.com/downloads) · [uv installation](https://docs.astral.sh/uv/getting-started/installation/)

## 1. Get the source and environment

```bash
git clone https://github.com/richhiey/ml-llm-ops.git
cd ml-llm-ops
uv sync --frozen
uv run --frozen python --version
```

Expect Python `3.12.12`. `uv sync --frozen` installs the committed dependency lock into `.venv`. Run commands from this repository's root. The configuration uses CPU PyTorch wheels on Windows/Linux and the standard macOS wheel, with all application tensors kept on CPU.

If you already have an older clone of this course, retain personal work outside it and use a fresh clone for the replacement project. An old environment and demand-model commands do not establish the new setup.

## 2. Prepare the research dataset

```bash
uv run --frozen catalog-mlops prepare
```

Expect `fashion-mnist-cpu-v1`, a split hash and counts including `train=12000` and `validation=3000`. The command downloads roughly 30 MiB, verifies file hashes and creates the fixed split manifest. Wait for the command to finish before training. A repeated preparation verifies existing data. A checksum mismatch identifies a damaged cache file to remove and download again.

## 3. Train and retain one baseline

```bash
uv run --frozen catalog-mlops train --config configs/baseline.json --output work/runs/baseline
uv run --frozen catalog-mlops evaluate --run work/runs/baseline
```

Expect four epoch observations and a completed result directory containing `run.json`, `config.json`, `dataset.json`, `environment.json`, `history.json`, `model.pt`, `source.zip`, `metrics.json` and `validation-predictions.csv`. Evaluation reloads the saved model and uses its declared validation IDs.

An existing run directory is preserved. Inspect it to resume your investigation, or choose a different output path for a genuinely new run. Do not delete a run to conceal a failed comparison.

## 4. Run the regression checks

```bash
uv run --frozen pytest -q
```

The mechanics tests use a small explicitly synthetic fixture. They check preprocessing, model reload, intake behavior, batch/HTTP consistency and evidence integrity. They do not establish Fashion-MNIST quality. The walkthrough trains on the real dataset.

## 5. Use the local notebook

Open `notebooks/01-pipeline-and-extension.ipynb` in VS Code and select the repository's `.venv` Python kernel. Run it from the repository root, or let its first cell locate the parent repository when opened from `notebooks/`. It shows the data loading, CNN, evaluation and plots directly with standard libraries and inspects your retained baseline. A missing baseline is an instruction to finish step 3 first.

## Resource expectations

CPU execution and bounded batches are the default. On the author's Apple M4 with 16 GB RAM, the initial four-epoch run took about 10 seconds end to end and peaked below 700 MiB RSS. Downloads, dependency installation, slower processors and concurrent applications affect the full setup. An 8 GB classroom computer is the target profile, with hardware-specific verification still pending.

Use a short writable clone path on Windows. Keep a few GB free for the environment, cached packages, dataset and run artifacts. If a command is unavailable, verify that `uv` and Git are on your terminal's path, then reopen the terminal.
