🏷️
# What full reproducibility requires

Linden Facilities has a model artifact and its RMSE, yet another engineer cannot reproduce the result. The missing piece might be the input data, source logic, config or even the library version used to load the artifact.

## Your route through this lesson

Work backward from a result to both identifiers and recoverable content. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** A complete connected recipe inventory with correct hash/commit/environment boundaries.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/03-registry-and-reproduction.ipynb#scrollTo=reproduce-reference). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Distinguish loading an artifact from rebuilding a result

There are two useful recovery questions. “Can I load the fitted model and get predictions?” requires the artifact and a compatible loading environment. “Can I rebuild the recorded evaluation result?” also requires the training recipe: source, data, configuration and environment. The first is not a shortcut to proving the second.

Suppose an engineer loads yesterday's model and gets the same predictions. That is evidence that the artifact can still serve those inputs. It does not show that training from the supplied source would produce that artifact today. Conversely, retraining something with a similar RMSE does not prove that the original recipe was used. A reproduction claim needs both a connected identity record and an actual execution.

## Record a connected set, not five isolated labels

**Lineage** is the connection from a result to the inputs and transformations that produced it. A reproducible training run needs both identifiers and recoverable content. A file hash helps detect differences; it cannot recreate a missing file.

| Element | Linden evidence | What it prevents |
|---|---|---|
| Code | Source-content revision + `source.tar.gz` | Reusing a changed training function |
| Data | Snapshot bytes + SHA256 | Quietly replacing evaluation rows |
| Config | `config.json`, alpha, guard, partition | Guessing the original factors |
| Environment | Python/package versions + `uv.lock` | Depending on today's resolver result |
| Model | Logged model URI + registry source run | Loading a similarly named artifact |
| Execution/result | Exact command, metrics and tolerance | Calling an unexplained score “close enough” |

A **hash** is a content fingerprint. GitHub identifies repository commits, while the helper records a defined source-content hash and recoverable archive for each training run. Both identities remain useful.

## Work backward from one result

Start at a run's `rmse_kwh`. Which rows did it measure? The evaluation partition and snapshot identify that question. Which model produced the predictions? The logged model URI and source run connect the fitted object. Which settings and implementation produced that model? The config, source-content hash and recoverable archive answer that. Which numerical libraries executed them? The recorded environment and dependency lock answer the remaining software question.

A useful handoff keeps these links together. Five filenames in five folders are weaker than a manifest that names the exact data, configuration, model and execution for one run. **Recoverable** means the actual bytes can be obtained, not merely that someone has typed their hash into a document.

## Know what each identifier covers

A Git commit identifies a repository snapshot, including its history relationship. The helper's `code_revision` identifies a defined set of content: package Python files, bundled data/card, `pyproject.toml` and `uv.lock`. A notebook or documentation edit can create a new Git commit without changing that training-content hash. An edit to the training function changes the content hash even before you commit it.

This course now uses both: GitHub versions the learning resources and code; each tracked run records its training-content fingerprint and source archive. Do not replace one identifier with the other or assume the content hash covers every file in the repository.

## A lockfile is necessary but not sufficient

`uv.lock` records resolved dependencies. It does not pin the dataset, choose alpha, or recover an edited source function. Conversely, copying a model pickle does not prove the training result can be rebuilt. Keep the fitted artifact and the recipe as distinct evidence.

A declared clean state removes inherited tracking stores, registry versions and notebook variables. A new source folder and environment test whether setup is sufficient; a new state directory alone tests a smaller property.

## Define agreement before rerunning

The [clean-state specification](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/clean-state.md) accepts absolute RMSE difference at most `1e-6` kWh with matching source, data, config and environment. Run IDs, timestamps and artifact paths can change. Timing is measured anew and must satisfy the inference deadline; it is not compared with a numerical equality tolerance.

If the score matches but the data hash differs, the reproduction fails. If lineage matches but RMSE exceeds tolerance, investigate numerical or execution differences before claiming success. Reproducibility is a contract to check, not a property conferred by logging fields.

![What full reproducibility requires: evidence path](assets/what-full-reproducibility-requires__01__en.png)

## Predict failures before trying a rerun

| Change in the receiving environment | Expected interpretation |
|---|---|
| New run ID and artifact directory | Normal new execution identities |
| Same CSV filename, changed data bytes | Different snapshot; lineage fails |
| Same direct requirements, changed SciPy | Different installed environment; investigate before execution |
| Same score, changed training source | Result similarity does not repair lineage |
| Matching inputs, RMSE delta above tolerance | Numerical/execution discrepancy remains unresolved |

The environment comparison is deliberately strict: it records installed distributions, Python and OS family/architecture, not just direct dependencies. A hosted Colab runtime includes additional packages, so its record is not interchangeable with a minimal local environment. The clean-handoff exercise establishes a run in the locked local environment and reconstructs that declared environment; it does not silently ignore inconvenient differences.

## Check for Understanding

An engineer has the manifest, `uv.lock` and a model URI, but the original artifact directory has been removed. Inventory which claims remain inspectable and which recovery is blocked. State what must be recovered before the handoff can be called reproducible.

▶️ **Solution** *(toggle)*

> **Result you should get:** the manifest still describes recorded identities/settings, but the missing source/model bytes cannot be reconstructed from their names, hashes or URI. Recover the retained source and fitted artifact from exported files or the original storage.
>
> **How:** trace each manifest field to content that can actually be opened. A lock reconstructs declared packages, not missing data or source. A model URI is a recovery link, not a cryptographic integrity guarantee. Preserve original evidence and restore into a new folder before rerunning.

## Learning outcome

Identify the code version, data snapshot, parameters/configuration, environment, and model artifact that must be traceable together for a training run to be reproducible.

## Summary

You can name both the identifiers and recoverable content behind a result. The tolerance and clean starting state make “reproducible” a claim another engineer can test.
