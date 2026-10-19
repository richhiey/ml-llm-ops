"""Sprint 1 follows the six Campus activities without additional notebooks."""
from textwrap import dedent
import json
import nbformat as n


def build(module, pin, setup):
    nb = n.v4.new_notebook()
    def md(anchor, body):
        cell = n.v4.new_markdown_cell(dedent(body).strip())
        cell.id = anchor; cell.metadata["id"] = anchor
        nb.cells.append(cell)
    def code(anchor, body, student=False):
        cell = n.v4.new_code_cell(dedent(body).strip())
        cell.id = anchor; cell.metadata["id"] = anchor
        if student: cell.metadata["tags"] = ["student-work"]
        nb.cells.append(cell)

    rows = json.loads((module/"maintainer/learning-path.json").read_text())
    lessons = [r for r in rows if r["sprint"] == 1]
    links = {r["id"]: "https://github.com/richhiey/ml-llm-ops/blob/main/module-a/"+r["public_path"] for r in lessons}
    md("start", f"""
    # Sprint 1 · Trace, extend and explain one pipeline

    Linden Facilities needs 24 hourly energy-demand estimates in one CSV within 60 seconds. You will trace its five stages, follow one validation edit, review an unsafe proposal and justify how predictions should be delivered.

    **Use this notebook for the whole sprint.** Follow the six sections below in order. Each Campus page supplies the explanation or brief for that section; run its notebook cells once and keep answers here. A later checkpoint reuses earlier work. Running all reference cells does not complete the independent tasks.

    | Campus activity | Notebook section | Keep, rather than redo |
    |---|---|---|
    | [Pipeline purpose]({links["A-S1-01"]}) | 1 · Understand the five stages | Your stage map |
    | [Trace the scaffold]({links["A-S1-02"]}) | 2 · Follow raw input to predictions | One row trace and baseline batch |
    | [Follow the expert edit]({links["A-S1-03"]}) | 3 · Add the validation stage | One edited project and before/after checks |
    | [Review generated code]({links["A-S1-04"]}) | 4 · Review a proposed guard | Explanation and distinguishing probes |
    | [Choose an inference pattern]({links["A-S1-05"]}) | 5 · Decide how to deliver | Recommendation using the existing batch evidence |
    | [Client checkpoint]({links["A-S1-06"]}) | 6 · Apply the contract to Harbor | Supplier decisions plus reused sprint work |

    **Start locally:** follow [setup](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/setup.md), select the module's Python 3.12 environment and run the provided setup cell once. Its package checks are preparation, not code you must explain. Work is retained under the printed local `work` folder. Running setup again creates a new session and leaves old sessions intact.
    """)
    local_setup = setup[:setup.index("state = Path(tempfile.mkdtemp")]+dedent("""
    work_root = PACKAGE / 'work'
    work_root.mkdir(exist_ok=True)
    session = Path(tempfile.mkdtemp(prefix='sprint-1-', dir=work_root))
    state = session / 'outputs'
    state.mkdir()
    print('Local work folder:', session)
    """)
    code("setup", local_setup)
    nb.cells[-1].metadata["tags"] = ["setup"]
    md("stage-map", """
    ## 1 · Understand the five stages

    A notebook is a useful interface, but an in-memory result can depend on cells run earlier. A **pipeline** makes the sequence and each stage's input/output explicit. **Reproducible** means another person can recover the same recipe and obtain an agreed result; it does not mean executing a cell twice.

    | Stage | Input → output |
    |---|---|
    | Ingestion | Historical CSV → checked table |
    | Preprocessing | Checked table → ordered model features |
    | Training | Training features and known demand → fitted scaler and model |
    | Evaluation | Held-out features and known demand → error measurements |
    | Inference | Planned features and fitted model → predictions |

    Here a **feature** is a model input; `demand_kwh` is the known training **target**. A fitted scaler stores means and scales learned from training rows. Keep it with the model: tomorrow's rows must use those stored values, not fit a new scaler.

    **Pause:** sketch the five-stage map here. Mark where known demand is needed and where a planned row can pass without it. The next section gives concrete objects for this same map, not another submission.
    """)
    md("raw-to-features", """
    ## 2 · Follow raw input to predictions

    **Read the input.** `ingest()` returns a pandas DataFrame, a table with named columns. `row_id` is the unique identifier. `partition` states each historical row's role: 168 training, 48 validation and 24 reserved final rows. The final rows stay out of this sprint's decisions.

    Run the next cell and choose one historical row to trace. Expect the three counts and the columns `temperature_c`, `hour`, `occupancy`, `demand_kwh` and `partition`.
    """)
    code("read-input", """
    import inspect, json, contextlib, io, runpy, shutil
    import pandas as pd
    import numpy as np
    from campus_mlops.pipeline import DATA, FEATURES, TARGET
    frame = ingest()
    print(frame.groupby('partition').size())
    display(frame.head())
    """)
    md("fit-and-evaluate", """
    ### Select features, fit once, evaluate held-out rows

    `preprocess` selects the three ordered features; it does not fit statistics. A Boolean **mask** is one true/false value per row; `.loc[mask]` selects those rows. The same mask must select matching features and targets.

    `train` creates a fitted `StandardScaler` and Ridge regressor together. Ridge is a linear prediction model; `alpha=1` is its supplied configuration, not a value to tune here. `evaluate` predicts validation rows without fitting again. **RMSE** is root mean squared error, in kWh; **MAE** is mean absolute error. Lower is better. Expect baseline validation RMSE about `1.443` kWh; this is a reproducible teaching result, not a claim about real buildings.
    """)
    code("fit-and-evaluate-code", """
    config = Config()
    features = preprocess(frame, config)
    train_rows = frame.partition == 'train'
    valid_rows = frame.partition == 'validation'
    model = train(features.loc[train_rows], frame.loc[train_rows, TARGET], config)
    metrics = evaluate(model, features.loc[valid_rows], frame.loc[valid_rows, TARGET])
    print('Feature order:', features.columns.tolist())
    print('Validation:', metrics)
    assert not (train_rows & valid_rows).any()
    assert features.index.equals(frame.index)
    assert abs(metrics['rmse_kwh'] - 1.4430039250255964) < 1e-6
    """)
    md("fitted-state", """
    ### Find the learned state

    Predict the number of fitting rows, validation rows and model inputs before running. Expect `168`, `48`, steps named `scale` and `ridge`, and `3` features. An attribute ending in an underscore, such as `n_features_in_`, records fitted state; `alpha` is a configuration setting.
    """)
    code("fitted-state-code", """
    print('Train / validation:', int(train_rows.sum()), int(valid_rows.sum()))
    print('Fitted steps:', list(model.named_steps))
    print('Input features:', model.named_steps['scale'].n_features_in_)
    """)
    md("batch-proof", """
    ### Follow planned input to the delivered file

    Planned rows have no known `demand_kwh`. The supplied `bootstrap` wrapper runs the same recipe from saved code and makes a fitted model available for `batch_predict`. Model selection/storage is prepared infrastructure here; you do not need to configure a registry or explain its internals in this sprint.

    Expect a file with 24 finite `prediction_kwh` values, preserving planned `row_id` order. The returned metadata identifies the source execution and model version. Compare its validation metric with the trace above: the delivered model comes from that same baseline recipe. Timing measures this complete batch's model load, prediction and output write.
    """)
    code("batch-proof-code", """
    baseline_state = state / 'baseline'
    with contextlib.redirect_stdout(io.StringIO()):
        delivery = course_cli('bootstrap', '--state', str(baseline_state))
    baseline = json.loads(delivery.stdout)
    predictions = pd.read_csv(baseline_state / 'batch.csv')
    planned = pd.read_csv(DATA / 'batch-v1.csv')
    evidence = baseline['inference']
    display(planned.head())
    display(predictions.head())
    print('Delivered file:', baseline_state / 'batch.csv')
    print('Batch:', evidence)
    assert planned.row_id.tolist() == predictions.row_id.tolist()
    assert np.isfinite(predictions.prediction_kwh).all() and len(predictions) == 24
    assert baseline['training']['metrics'] == metrics
    assert evidence['complete_within_60s']
    """)
    md("trace-notes", """
    **Finish the same stage map:** add one historical `row_id`, its partition and target role, then one planned `row_id` and its output prediction. Which object owns fitted scaling? Why can't a completed prediction file measure tomorrow's prediction error? Keep these short answers here and continue; do not rerun the baseline for later pages.
    """)
    md("stage-edit", """
    ## 3 · Add the validation stage

    Linden receives a numeric `hour=24`. A finite-number check alone accepts it. The new **contract** rejects temperature outside `[-30,50]`, hour outside integer `[0,23]`, and occupancy outside `[0,100]`. Accepted input must return unchanged in a separate copy; invalid input must raise `ValueError`, not be silently repaired.

    Create one editable project inside your local work folder. The existing focused test checks the proposed contract. Its first failure is intentional: expect `DID NOT RAISE`. A good validation score on ordinary rows cannot expose this missing rule.
    """)
    code("stage-edit-code", """
    project = Path(shutil.move(str(make_project('stage-project')), str(session / 'project')))
    target = project / 'src/campus_mlops/pipeline.py'
    print('Keep this project:', project)
    _ = project_tests(project, 'tests/test_spine.py::test_contract_extension_and_unchanged_pipeline',
                      '-q', expected_returncode=1)
    """)
    md("stage-change", """
    ### Follow the expert's bounded edit

    The function below is the expert reference. Read the code alongside this explanation before applying it:

    | Statement | Why it is needed |
    |---|---|
    | `validate_features(frame)` | Reject empty input, missing feature columns and non-finite numbers first |
    | `for column, low, high ...` | Apply a declared rule to each feature |
    | `.between(low, high).all()` | Require every row to lie within inclusive bounds |
    | `raise ValueError(...)` | Stop at invalid input instead of hiding it |
    | `frame.hour % 1 == 0` | Reject fractional hours that pass the range check |
    | `return frame.copy(deep=True)` | Return only after every check; preserve caller-owned input |

    The next cell prints the function and applies only this function to your project, showing the real source diff. This is a follow-the-expert activity; you do not need to type a second implementation. `preprocess` already calls this boundary when `range_guard=True`, so ingestion, fitting and evaluation stay intact.
    """)
    code("stage-change-code", """
    import difflib
    print(inspect.getsource(validate_ranges))
    before = target.read_text()
    start = before.index('def validate_ranges(')
    end = before.index(chr(10) * 2 + 'def preprocess(', start)
    after = before[:start] + inspect.getsource(validate_ranges).rstrip() + before[end:]
    target.write_text(after)
    stage_diff = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                            fromfile='starter', tofile='edited'))
    print(stage_diff)
    _ = (session / 'stage-change.diff').write_text(stage_diff)
    """)
    md("stage-contract", """
    ### Check the contract, including caller-owned input

    `runpy.run_path` reads your saved project file into a separate namespace. `project_guard` below is therefore your edited function, not the notebook's earlier reference import. If you edit that file again, rerun this loading cell before probing it.

    Predict `hour=0`, `23`, `1.5` and `24` before execution. Expect the first two accepted and the last two rejected. `assert_frame_equal` checks values, columns, index and types; `is not` checks that the returned object is a distinct copy. A `try/except` block lets us record an expected rejection without stopping the notebook.
    """)
    code("stage-contract-code", """
    project_guard = runpy.run_path(str(target))['validate_ranges']
    original = frame.copy(deep=True)
    checked = project_guard(frame)
    pd.testing.assert_frame_equal(frame, original)
    pd.testing.assert_frame_equal(checked, original)
    assert checked is not frame
    observed = []
    for hour in [0, 23, 1.5, 24]:
        sample = frame.iloc[[0]].copy()
        sample['hour'] = float(hour)
        try:
            project_guard(sample)
            status = 'accepted'
        except ValueError:
            status = 'rejected'
        observed.append({'hour': hour, 'observed': status})
    display(pd.DataFrame(observed))
    assert [r['observed'] for r in observed] == ['accepted', 'accepted', 'rejected', 'rejected']
    """)
    md("stage-check", """
    ### Confirm the unchanged stages still run

    Rerun the same focused test: expect one passing test. It also checks temperature/occupancy boundaries, missing and non-finite features, and unchanged valid-data metrics. `project_tests` and `course_cli(..., project=project)` use fresh processes against your saved source; this avoids stale notebook imports.

    Run the edited project's full delivery path once. Expect the same validation metrics, all 24 output rows and completion within 60 seconds. Keep this result for the inference decision and checkpoint. Registry lifecycle tests and fresh-environment recovery are later work, not extra Sprint 1 assignments.
    """)
    code("stage-check-code", """
    project_tests(project, 'tests/test_spine.py::test_contract_extension_and_unchanged_pipeline', '-q')
    with contextlib.redirect_stdout(io.StringIO()):
        delivery = course_cli('bootstrap', '--state', str(state / 'edited'), project=project)
    completed = json.loads(delivery.stdout)
    edited_predictions = pd.read_csv(state / 'edited/batch.csv')
    assert completed['training']['metrics'] == metrics
    assert planned.row_id.tolist() == edited_predictions.row_id.tolist()
    assert np.isfinite(edited_predictions.prediction_kwh).all()
    assert completed['inference']['rows'] == 24 and completed['inference']['complete_within_60s']
    print('Edited-project batch:', completed['inference'])
    print('Outputs:', state / 'edited')
    """)
    md("stage-work", """
    ## 4 · Review a proposed guard

    An assistant proposes the function below. Treat it as untrusted exercise material, not an update to install. Your project already contains the explained guard: keep it. **Mutation** means changing the object passed by the caller.

    1. Explain each candidate statement and predict what it does to `hour=24`, a negative hour and a fractional hour.
    2. Probe those cases plus one valid input. Compare the caller's values before/after and whether the returned object is the same object. Keep at least one observed failure against the required contract.
    3. Explain the changes needed before merging. Use your existing `project_guard` to contrast correct behavior; do not rebuild the project or rerun every pipeline stage.

    The Campus hints and pandas documentation are available if needed. The broader boundary and integration checks above remain evidence; repeat only a check affected by a new edit.
    """)
    code("practice-inputs", """
    candidate_path = PACKAGE / 'exercises/generated-stage-candidate.py'
    print(candidate_path.read_text())
    proposed_guard = runpy.run_path(str(candidate_path))['proposed_guard']
    """)
    code("candidate-probes", """
    # Add your predictions and probes here.
    # Use a fresh sample.copy(deep=True) for each case.
    # Keep the unsafe candidate out of target (your working pipeline source).
    """, student=True)
    md("inference-choice", """
    ## 5 · Decide how to deliver predictions

    Use the Campus comparison to decide from the brief: all 24 inputs arrive together; one complete file is needed within 60 seconds; there is no interactive caller.

    **Latency** is time until the required result is ready. **Throughput** is records processed per unit time. A batch can load one model for the whole file and exit. A request service must respond as inputs arrive and meet an availability window. Actual cost depends on workload and resources; no endpoint benchmark or price is supplied.

    Add one short recommendation here addressing latency, throughput and resource obligations. Cite `completed['inference']` from your edited project and explain what different requirement would make request serving appropriate. Do not run another batch or build an endpoint.
    """)
    md("checkpoint-work", """
    ## 6 · Apply the contract to Harbor

    Harbor Facilities supplies a new five-row intake below. It has only `row_id`, `temperature_c`, `hour` and `occupancy`: no historical target or partition. Apply the taught feature-validation contract; do not pass this file to historical `ingest()`, train on it or repair its values.

    Read the Campus client brief. Classify each identifier, justify its rule, then test your decisions using the already loaded `project_guard`. Preserve the raw table. Decide whether the mixed intake can pass as one whole batch. This is new input for the same project, not a new pipeline build.

    Finish with **one notebook plus the existing project/output folder**: your source diff and explanation, candidate review, supplier decisions, passing contract/batch evidence and inference recommendation. Reuse previous outputs; no new notebook, extra report, registry setup or clean-environment run is required.
    """)
    code("supplier-input", """
    supplier_path = project / 'exercises/harbor-intake.csv'
    supplier = pd.read_csv(supplier_path)
    supplier_original = supplier.copy(deep=True)
    display(supplier)
    """)
    code("supplier-work", """
    # Add your row classifications, reasons and guard probes here.
    # Check the mixed batch as well as individual rows.
    # Confirm supplier still equals supplier_original after your checks.
    """, student=True)
    md("finish", """
    ## Finish and keep your work

    Save your answers in this notebook. Keep the printed local session folder: it contains `project/`, the source diff and `outputs/`. Your edited project's batch CSV and metadata are under `outputs/edited/`. Keep this folder for later sprints; moving to another computer requires copying it as well as the notebook.

    Do not run setup again simply to finish a Campus page. Restarting the kernel loses Python variables, but saved local files remain; the paths printed above let you find them. If you must repeat the worked run, it creates another session instead of overwriting this one.
    """)
    nb.metadata.colab = {"name": "01-pipeline-and-extension.ipynb", "provenance": []}
    nb.metadata.kernelspec = {"display_name": "Campus helper Python 3.12", "language": "python", "name": "python3"}
    return nb
