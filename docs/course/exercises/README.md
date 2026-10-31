# Course intake assets and setup responsibility

These files are outside application runtime. They provide unknown inputs and clearly labeled review material; they are not evidence that a learner has completed an app change or requested an assistant response. The app package neither imports these tools nor archives them with a model recipe.

## Ready input files

- `harbor-intake.csv`: five unfamiliar feature rows for domain probes; it is not the `24`-row planned delivery.
- `harbor-plan-a.csv`, `harbor-plan-b.csv`, `harbor-plan-c.csv`: supplied complete-plan acceptance inputs. Inspect each before deciding which contract it meets.
- `generated-stage-candidate.py`: intentionally unsafe authored assistant-style proposal kept outside installed source.
- `sprint-1-attempt.py`: optional unsolved review/supplier task shell. Source patches and ordinary application tests remain the actual engineering deliverable.
- `experiment-matrix-starter.csv` and `claim-evidence-sheet.csv`: optional blank working aids.
- `monitoring/linden/` and `monitoring/harbor/`: existing synthetic reference/current/stable/feedback inputs, policy and data-card hashes. No app input-generation step is required.

## Instructor or self-study provisioning

Before an isolated client investigation, the incoming store must exist. An instructor can provide it; a self-study learner can provision it explicitly using this external setup tool. This is preparation of an unknown exercise state, not the assessed response or a real production incident. Use a new destination and retain it thereafter:

```sh
uv run python docs/course/exercises/prepare-evidence.py rollback --destination work/rollback
uv run python docs/course/exercises/prepare-evidence.py registry-assessment --destination work/harbor-registry
```

Each destination is itself an MLflow store containing `mlflow.db`, artifacts and `case.json`. Open `Workspace("work/rollback")` or the actual supplied path. `case.json` records `case`, `state`, registered version IDs and the incoming requirement. Provisioning trains/registers/selects baseline versions only in that new isolated store, preserving the cumulative `work/tracking` project. Learners must still inspect the incoming active/pending states, decide, explain and carry out the recovery themselves. Never count provisioning as evidence of recovery skill.

For comparison/receiving acceptance, prepare a separate unknown copy from retained real work:

```sh
uv run python docs/course/exercises/prepare-evidence.py comparison --destination work/harbor-comparison
uv run python docs/course/exercises/prepare-evidence.py receiving --bundle work/handoff-export --destination work/receiving-review
```

Comparison reads actual five-run evidence and emits `observations.json`/`client-note.txt`; the note is intentionally questionable fixture prose, not an actual new assistant response. Receiving copies a verified real bundle into `candidate-bundle` and changes a file in that copy; the original export/index remains trusted evidence. Reopen existing prepared inputs rather than rerunning setup. The real release descriptor is authored/verified against actual app records; no fake integration index is generated.

The independent tests of these provisioning boundaries live here in `tests/test_fixture_provenance.py`; the application's own regression tests remain under root `tests/`. Optional preparation of a new synthetic cohort is available to instructors with `monitoring --destination NEW_DIR --cohort linden|harbor`. Published cohort hashes and names must match the provided static assets; no real-world performance claim follows from them.
