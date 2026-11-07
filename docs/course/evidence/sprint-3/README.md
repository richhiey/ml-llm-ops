# Observed registry and monitoring reference

These files come from an actual author CPU pilot. The native run IDs and registered name identify that reference store; they are not preloaded in a learner's local MLflow database. Create and inspect your own runs and registry versions.

- `observations.json` retains measured cohort quality, controlled comparisons, actual loaded model identities and an extract of the named model's local audit. It identifies both the original training source and the later inference source.
- Each cohort's `predictions.csv` retains the actual delivered rows. Known labels are separate in the corresponding `labels.csv`; `bad-current` uses the same images and labels as `current`.
- `input-observations.csv` is a compact export from the actual batch record: the consumed image identifier, PNG fingerprint and mean brightness on the `0–1` scale. Each row describes one thumbnail, not one pixel. It supports independent histogram reconstruction and matching-input checks.
- `fixture.json` records the research split and construction. `shifted-current` is an explicit exercise transformation: multiply the same current-image pixels by `0.45`, round and preserve their labels.
- `inference-source.zip` retains the code actually used by the later consumer, including the authored completed intake check and the explicit reference deployment name. It is different from the older selected model's training archive. The model reports both identities.

The native validation report was retained on the original MLflow run, and alias selection verified its bytes. Full local batch/observation records, environment execution logs and raw HTTP responses are retained in the author proof. Their recorded fingerprints are reference identities; the compact exports above do not claim to be those complete JSON records.

The ordinary and shifted cohort comparisons keep the model and inference code fixed. The bad-model comparison keeps image bytes, ordering and labels fixed. Reference and current are different research groups; current and shifted-current share source image identities but have different pixel bytes.

The final official-test result was reported after selection was fixed and the rollback restored the approved model. These observations do not establish performance on arbitrary photographs, other hardware or future suppliers.
