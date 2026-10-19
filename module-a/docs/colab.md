# Work with the course in Colab

Open a notebook from the [notebook index](../notebooks/README.md), connect a CPU runtime, and run its setup cell first. Use Python 3.12. Google's [runtime versions page](https://research.google.com/colaboratory/runtime-version-faq.html) lists the available versions; at this review, `2026.07` uses Python 3.12.13. Choose it under **Runtime → Change runtime type → Runtime Version** if the current runtime uses a different Python version. Past versions have a limited availability window, so the setup cell checks the actual interpreter.

The setup cell clones an immutable commit of `richhiey/ml-llm-ops` under `/content`, installs its locked runtime dependencies and imports the package from that checkout. `requirements-colab.txt` is exported from `uv.lock`, with environment markers selecting the platform's packages. No helper implementation is copied into a notebook. The notebook checks both the package version and source-content revision.

Start in a fresh runtime. If you imported a different NumPy, pandas, scikit-learn or MLflow version before setup, disconnect/delete the runtime and reconnect before running from the top. Installing over an already imported numerical library does not replace the in-memory module safely.

## What persists

Each notebook creates a new temporary tracking directory and prints its path. Runtime deletion removes that directory and its artifacts. Download your evidence and source/model artifacts before deleting the runtime; notebook outputs alone are not a recovery package. Never paste keys into a notebook. These exercises do not require a provider key.

The four notebooks are complete worked references. Your independent stage edit happens in a project copy, and the rollback practice starts before the rollback. Do not submit reference outputs as your own investigation.

## Reproduction and the UI

Reproduction within one Colab runtime checks that runtime's installed distributions and platform. Colab also supplies many packages outside the course lock. A hosted run's manifest therefore does not describe a minimal fresh `uv` environment. For the clean-environment project handoff, use the locked local setup, create the selected run there, then follow [clean-state recovery](clean-state.md). The strict comparison correctly rejects a Colab-to-macOS environment change; do not weaken it to make the check green.

Notebook 02 prints an MLflow UI command for the local setup. A printed localhost address is not a working browser connection to a hosted Colab machine. Perform the UI comparison from a local clone using a prepared matrix state. We do not open a public MLflow tunnel from Colab.

## Authoring updates

Change package code and tests first, sync `uv.lock`, and export runtime requirements with:

```sh
uv export --locked --no-dev --no-emit-project --no-hashes --format requirements-txt --output-file requirements-colab.txt
```

Commit the source, update the notebook's immutable commit plus helper-content pin, and execute all four notebooks before publishing their update. Keep outputs from an actual execution as verification evidence; do not invent hosted results. Local kernel execution and a fresh clone/install check are separate from a hosted Colab browser test.
