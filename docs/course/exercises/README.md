# Evidence investigations

These Campus exercises use your completed project records. They introduce a questionable draft or a damaged **copy** for you to investigate. They do not claim that an assistant produced a supplied note or that an altered copy was an observed execution.

Run from the repository containing `pyproject.toml`, after completing the relevant cumulative project activity:

```bash
uv run python docs/course/exercises/prepare-evidence.py comparison --destination work/comparison-review
uv run python docs/course/exercises/prepare-evidence.py integration --destination work/integration-review
uv run python docs/course/exercises/prepare-evidence.py receiving --destination work/receiving-review
```

Prepare only the exercise requested by your Campus task. Each command prints its new directory. An existing destination is rejected so you keep earlier evidence. Use `--work-dir PATH` when your cumulative project is elsewhere. The receiving command also accepts `--bundle PATH` for an existing portable export.

| Exercise | Required evidence | Starting assets |
|---|---|---|
| `comparison` | Your five saved matrix runs with their existing autologged training diagnostic at `alpha=1` | `observations.json`, `client-note.txt` |
| `integration` | Your saved selection, registered version, matching `active` alias, and retained `tracking/batch.json` and `batch.csv` | `handoff-index.json`, `brief.txt` |
| `receiving` | A valid `work/handoff-export`, or the export passed with `--bundle` | `candidate-bundle/`, `brief.txt` |

The comparison file preserves actual run IDs, recorded metric names, evaluation bases, values, and all logged parameters under `controls`. Its observation labels identify measurements, not separate executions. The stakeholder note is authored exercise text requiring review. No model calls or training occur during preparation.

The integration index is explicitly a draft assembled for investigation. Registry, alias and original batch evidence remain authoritative. Repair your draft using those records; creating another model does not resolve a documentation mismatch.

The receiving candidate is copied from an export that passes `verify_bundle` before preparation. Only the exercise copy is changed. Its original checksum index remains intact so integrity checks can expose the damage. Keep the original export as trusted recovery evidence; do not rewrite checksums to accept an unexplained change.

Preparation validates prerequisites before creating the destination, stages files in a new sibling directory, and never changes project decisions or existing model artifacts. If prerequisites are missing, return to your retained project evidence rather than repeating training simply to create an exercise.

The preparation logic lives in the shared `linden_mlops.course_evidence` module, which is included in exported source archives. In restored source, you can use `uv run python -m linden_mlops.course_evidence` with the same arguments; the documentation script is a thin wrapper.
