from pathlib import Path
import json
import numpy as np
import pandas as pd
import pytest
from linden_mlops import *
from linden_mlops.lifecycle import MODEL_NAME
from linden_mlops.pipeline import FEATURES, DATA


def test_contract_extension_and_unchanged_pipeline():
    raw = ingest()
    original = raw.copy(deep=True)
    checked = validate_ranges(raw)
    pd.testing.assert_frame_equal(raw, checked)
    pd.testing.assert_frame_equal(raw, original)
    assert raw.groupby('partition').size().to_dict() == {'final': 24, 'train': 168, 'validation': 48}
    base = run_pipeline(Config())[1]
    extended = run_pipeline(Config(range_guard=True))[1]
    assert base == extended
    assert extended['rmse_kwh'] < 5
    for col, bad in [('hour',24), ('hour',-1), ('hour',1.5), ('temperature_c',51), ('temperature_c',-31), ('occupancy',101), ('occupancy',-1), ('occupancy',np.nan), ('hour',np.inf)]:
        broken = raw.copy(); broken[col] = broken[col].astype(float); broken.loc[0,col] = bad
        with pytest.raises(ValueError): validate_ranges(broken)
    for col, bounds in [('hour',(0,23)),('temperature_c',(-30,50)),('occupancy',(0,100))]:
        for value in bounds:
            valid=raw.copy(); valid[col]=valid[col].astype(float); valid.loc[0,col]=value
            validate_ranges(valid)
    with pytest.raises(ValueError): validate_ranges(raw.drop(columns=['hour']))
    with pytest.raises(ValueError): validate_ranges(raw.iloc[:0])


def test_lifecycle_and_reproduction(tmp_path):
    ws = Workspace(tmp_path/'original')
    runs = run_matrix(ws, autolog=True)
    rows = export_runs(ws)
    best = rows.sort_values('rmse_kwh').iloc[0]
    assert verify_summary(rows, best.run_id)['recommendation_matches_metric']
    assert not verify_summary(rows, rows.sort_values('rmse_kwh').iloc[-1].run_id)['recommendation_matches_metric']
    polluted=rows.copy(); polluted.loc[polluted.index[0],'data_sha256']='different'
    with pytest.raises(ValueError): verify_summary(polluted,best.run_id)
    first = register(ws, best.run_id)
    with pytest.raises(ValueError): activate(ws, first, 'unapproved')
    approve(ws, first, 'Reference contract tests + controlled RMSE comparison')
    activate(ws, first, 'Initial approval')
    second=register(ws, rows.sort_values('rmse_kwh').iloc[1].run_id)
    approve(ws, second, 'Numerically acceptable candidate')
    activate(ws, second, 'Trial candidate')
    # Candidate can pass numerical gate yet fail an operational acceptance review.
    event=activate(ws, first, 'Rollback: operational review rejected trial')
    assert event['previous_version']==second and event['new_version']==first
    predictions,evidence=batch_predict(ws)
    assert len(predictions)==24 and np.isfinite(predictions.prediction_kwh).all()
    assert evidence['resolved_version']==first and evidence['complete_within_60s']
    assert ws.client.get_model_version(MODEL_NAME,first).run_id==best.run_id
    assert len((ws.path/'audit.jsonl').read_text().splitlines())==3
    report=reproduce(ws,best.run_id,tmp_path/'fresh')
    assert report['passed'] and report['lineage_matched'] and report['rmse_delta']<=1e-6
    with pytest.raises(ValueError): reproduce(ws,best.run_id,tmp_path/'fresh')
    run=ws.client.get_run(best.run_id)
    assert 'ridge__alpha' in run.data.params  # actually logged by sklearn autolog
    assert 'training_mean_squared_error' in run.data.metrics
    assert Path(ws.client.download_artifacts(best.run_id,'reproduction/source.tar.gz')).exists()


def test_comparison_rejects_repeats_missing_controls_and_incompatible_rows():
    """A plausible recommendation must not bypass the declared comparison population."""
    rows = pd.DataFrame([dict(run_id=f'unit-{i}',alpha=str(a),rmse_kwh=float(i+1),
        comparison_group='demand-v1-validation',data_sha256='fixed',code_revision='fixed',
        range_guard='True',evaluation_partition='validation') for i,a in enumerate([.01,.1,1,10,100])])
    assert verify_summary(rows,'unit-0')['recommendation_matches_metric']
    for changed in [rows.assign(alpha='1'),rows.assign(run_id='same'),rows.assign(rmse_kwh=float('nan')),
                    rows.assign(range_guard='False'),rows.assign(data_sha256=None),
                    pd.concat([rows,rows.iloc[[0]].assign(run_id='heldout',comparison_group='final-holdout',evaluation_partition='final')])]:
        with pytest.raises(ValueError):verify_summary(changed,'unit-0')


def test_reproduction_checks_transitive_environment_before_running(tmp_path,monkeypatch):
    import linden_mlops.lifecycle as life
    ws=Workspace(tmp_path/'source')
    record=ws.run(Config(range_guard=True))
    original=life.environment
    assert 'scipy' in original()['packages'], 'Transitive numeric dependency must be recorded'
    def changed_environment():
        result=original();result['packages']['scipy']='0.changed';return result
    monkeypatch.setattr(life,'environment',changed_environment)
    with pytest.raises(ValueError,match='environment'):
        reproduce(ws,record['run_id'],tmp_path/'should-not-exist')
    assert not (tmp_path/'should-not-exist').exists()


def test_failed_run_disables_autolog_for_subsequent_untracked_training(tmp_path,monkeypatch):
    import linden_mlops.lifecycle as life
    ws=Workspace(tmp_path/'source');original=life.run_pipeline
    def fail(*args,**kwargs):raise ValueError('deliberate teaching failure')
    monkeypatch.setattr(life,'run_pipeline',fail)
    with pytest.raises(ValueError,match='deliberate'):
        ws.run(Config(range_guard=True,autolog=True))
    monkeypatch.setattr(life,'run_pipeline',original)
    before=len(ws.client.search_runs([ws.experiment_id]))
    run_pipeline(Config(range_guard=True))
    assert len(ws.client.search_runs([ws.experiment_id]))==before, 'Failed tracked run must not leak autolog state'


def test_approval_rejects_final_partition_and_nonfinite_metric(tmp_path):
    ws=Workspace(tmp_path/'source')
    final=ws.run(Config(range_guard=True),partition='final')
    version=register(ws,final['run_id'])
    with pytest.raises(ValueError,match='finite validation'):
        approve(ws,version,'Final is not the declared selection partition')
    valid=ws.run(Config(range_guard=True))
    version=register(ws,valid['run_id'])
    ws.client.log_metric(valid['run_id'],'rmse_kwh',float('nan'))
    with pytest.raises(ValueError,match='finite validation'):
        approve(ws,version,'Deliberately corrupted raw metric must fail')
