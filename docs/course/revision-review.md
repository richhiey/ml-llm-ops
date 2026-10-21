# Module A Campus review and verification

Reviewed and revised on 21 October 2026. This review covers the 26 Module A Campus lessons and their four local notebooks. The source journey's titles, order, lesson types and exact learning outcomes are unchanged. The [outcome map](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/outcomes.md) makes that alignment inspectable.

## Where the learning journey needed work

| Gap | Resulting revision | Example |
|---|---|---|
| Independent work sometimes supplied the implementation or decision too early. | Learners now make and explain their own decisions before opening collapsed result-first feedback. Autologging, rollback and integration require investigation. | [Autologging practice](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/06-autologging-and-reducing-manual-tracking-overhead/lesson.md) |
| Assessments repeated familiar steps without enough transfer. | New cases require classifying unseen supplier rows, excluding a repeated training observation, applying a revised approval gate and diagnosing a damaged export copy. | [Experiment tracking assessment](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/08-experiment-tracking-deliverable/lesson.md) |
| Checkpoints did not consistently help learners diagnose a wrong result. | Feedback states the expected result, explains why it matters and gives a targeted check or repair. All 11 independent practices and four assessments include post-attempt self-checks. | [Clean reproduction practice](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-4/05-proving-the-pipeline-reproduces/lesson.md) |
| The Sprint 2 rubric asked for final-holdout evidence before selection was complete. | The assessment and private rubric now use validation evidence. Final observation stays at the end of the cumulative handoff, after configuration selection is fixed. | [Experiment tracking assessment](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/sprint-2/08-experiment-tracking-deliverable/lesson.md) |
| Notebook navigation and repository references had drifted. | Every lesson names its matching notebook activity. Repository references use GitHub URLs; public reference documentation remains available. All development and receiving instructions use the local project. | [Notebook index](https://github.com/richhiey/ml-llm-ops/blob/main/notebooks/README.md) |
| Visual explanations needed a stronger connection to actual execution. | Four shared plotting functions produce notebook figures and Campus reference images from actual records. SVG text remains editable. Captions identify axes, units, provenance and interpretation limits. | [Figure guide](https://github.com/richhiey/ml-llm-ops/blob/main/docs/visualizations.md) |

The notebooks import reusable pipeline, lifecycle, project, exercise and visualization modules. Investigation packets are isolated copies of retained evidence; preparing them does not train or change the cumulative project. These same modules form the baseline for the cumulative project.

## What was verified locally

- All 26 source titles, types, order and exact outcomes matched the retained journey. Canonical Campus links, notebook activity metadata, local-link policy and post-attempt feedback checks passed.
- Four notebooks executed 51 code cells with zero errors in private copies containing representative learner attempts. Published attempt cells remain unsolved; complete them before running cells that consume their results.
- The source project and an independently restored receiver each passed all 22 tests on Python 3.12.13 in fresh locked environments. Each suite emitted three MLflow integer-schema warnings.
- A custom five-run matrix selected `alpha=0.2`; that actual recipe survived registration, batch inference and portable recovery. The original store was unavailable during the receiving proof and was restored afterward.
- The receiver matched all five recipe invariants, with absolute validation RMSE delta `0` against `0.000001` kWh tolerance. Its output contained 24 aligned, finite predictions and completed the measured batch within 60 seconds.
- The new investigation failures and repairs were exercised: the training-observation trap, mixed identity index, guard-disabled approval rejection, damaged-copy checksum rejection and repair, and invalid receiver inputs.
- All four final figures were checked against their source observations and inspected as rendered images. SVG exports contain editable text and no embedded raster images. [Reference observations and image hashes](https://github.com/richhiey/ml-llm-ops/blob/main/docs/course/figures/reference-observations.json) are retained.

Verified source revision: `sha256:76ea3db250d29684cddaf3ec45af17c0ca9c40315cbde0ca7ea4748a4389bc67`. Lock SHA-256: `ba27bb07af2c216dfcc76c170aa103c7e734671ed5041999bff75e4b12fb6f78`.

## Remaining evidence gaps

MLflow's local server passed health and HTML checks, but the available browser connection could not open a rendered UI. UI comparison and registry navigation therefore remain unverified in this revision. Raw records, artifacts, registry operations and notebook figures were exercised; they do not substitute for UI inspection.

The assistant-validation rehearsal used an explicitly authored fixture because an institution-approved assistant session was unavailable. Learner instructions still require retaining their actual request and response. The fixture is never presented as an observed assistant conversation.

Environment installation used cached packages. An uncached network installation and human learner trials have not been tested. This is technical and editorial verification, rather than evidence of classroom timing or learner success. Live lessons remain outside this revision's scope.
