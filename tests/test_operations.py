"""Operational decisions, contaminated evidence and feedback-recipe recovery."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import pytest
from linden_mlops import Config, Workspace, register, approve, activate, batch_predict
from linden_mlops.lifecycle import MODEL_NAME
from linden_mlops.operations import (monitor, train_candidate,
    compare_candidate, promote_candidate, write_incident, Policy)
from linden_mlops.recovery import export_run, reproduce_bundle, verify_bundle
from linden_mlops.pipeline import TARGET, sha256
from linden_mlops.lifecycle import write_json
from dataclasses import asdict


def prepare_monitoring(destination, case='linden'):
    """Create stable, covariate-shift and degraded-response assets once; no model fit."""
    if case not in {'linden', 'harbor'}:
        raise ValueError('Case must be linden or harbor')
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Monitoring destination must not exist; reopen retained inputs')
    destination.mkdir(parents=True)
    rng = np.random.default_rng(817 if case == 'linden' else 1129)

    def features(n, label, shifted=False):
        return pd.DataFrame({'row_id': [f'{case}-{label}-{i:03}' for i in range(n)],
            'temperature_c': rng.uniform(8, 28, n) + (8 if shifted else 0),
            'hour': np.arange(n) % 24, 'occupancy': rng.integers(10, 91, n)})

    reference = features(192, 'reference')
    stable = reference.copy(); stable.row_id = [f'{case}-stable-{i:03}' for i in range(len(stable))]
    shifted = reference.copy(); shifted.row_id = [f'{case}-shift-{i:03}' for i in range(len(shifted))]
    shifted.temperature_c += 8
    for name, frame in [('reference', reference), ('stable', stable), ('current', shifted)]:
        frame.to_csv(destination / f'{name}.csv', index=False)
    feedback = features(240, 'feedback', shifted=True)
    base = 45 - .7*feedback.temperature_c + .3*feedback.hour + .55*feedback.occupancy
    noise = rng.normal(0, 1.0, len(feedback))
    feedback[TARGET] = base + noise + (12 if case == 'linden' else 10)
    feedback['partition'] = ['validation' if i % 10 in {0, 1} else 'final' if i % 10 == 2 else 'train' for i in range(len(feedback))]
    feedback.to_csv(destination / 'feedback.csv', index=False)
    feedback[TARGET] = base + noise
    feedback.to_csv(destination / 'shift-feedback.csv', index=False)
    write_json(destination / 'policy.json', asdict(Policy()))
    card = {'case': case, 'synthetic': True, 'seed': 817 if case == 'linden' else 1129,
        'reference_rows': 192, 'monitoring_rows': 192, 'feedback_partitions': {'train': 168, 'validation': 48, 'final': 24},
        'shift': 'temperature +8 C; stable output law in shift-feedback; intercept +12/+10 kWh in feedback',
        'limits': 'Constructed independent teaching cohorts; no real chronology, calibration or production claim.',
        'files': {p.name: sha256(p) for p in destination.glob('*.csv')}}
    write_json(destination / 'data-card.json', card)
    return card



def test_feedback_cycle_uses_disjoint_evaluation_rejects_bad_candidate_and_recovers(tmp_path):
    ws = Workspace(tmp_path/'store')
    original = ws.run(Config(range_guard=True))
    version = register(ws, original['run_id']); approve(ws, version, 'Guarded validation evidence')
    activate(ws, version, 'Initial selected recipe')
    inputs = tmp_path/'inputs'; prepare_monitoring(inputs)
    def observe(name, current='current.csv', feedback=None):
        return monitor(ws, inputs/'reference.csv', inputs/current, inputs/'policy.json', tmp_path/f'{name}.json',
                       inputs/feedback if feedback else None)
    assert observe('stable', 'stable.csv')['action'] == 'continue_monitoring'
    assert observe('unlabeled')['action'] == 'investigate'
    assert observe('shift-only', feedback='shift-feedback.csv')['action'] == 'investigate'
    few = pd.read_csv(inputs/'current.csv').iloc[:24]; few.to_csv(inputs/'few.csv',index=False)
    assert observe('few', 'few.csv', 'feedback.csv')['action'] == 'collect_more'
    report = observe('degraded', feedback='feedback.csv')
    assert report['action'] == 'retrain_candidate' and report['validation_rmse_kwh'] > 3
    with pytest.raises(ValueError,match='trigger'):
        train_candidate(ws, tmp_path/'unlabeled.json', inputs/'feedback.csv')
    bad = train_candidate(ws, tmp_path/'degraded.json', inputs/'feedback.csv', alpha=1000000)
    comparison = compare_candidate(ws, tmp_path/'degraded.json', inputs/'feedback.csv', bad['version'], tmp_path/'bad.json')
    assert not comparison['passed']
    tampered = dict(comparison, passed=True); (tmp_path/'bad.json').write_text(json.dumps(tampered))
    with pytest.raises(ValueError,match='fails response'):
        promote_candidate(ws, tmp_path/'bad.json', 'An edited Boolean cannot authorize promotion')
    assert str(ws.client.get_model_version_by_alias(MODEL_NAME,'active').version) == version
    good = train_candidate(ws, tmp_path/'degraded.json', inputs/'feedback.csv')
    comparison = compare_candidate(ws, tmp_path/'degraded.json', inputs/'feedback.csv', good['version'], tmp_path/'good.json')
    assert comparison['passed'] and comparison['candidate_rmse_kwh'] < comparison['incumbent_rmse_kwh']
    frame=pd.read_csv(inputs/'feedback.csv')
    assert set(comparison['evaluation_rows']).isdisjoint(frame.loc[frame.partition=='train','row_id'])
    promote_candidate(ws, tmp_path/'good.json', 'Lower error on the same independent feedback validation rows')
    with pytest.raises(ValueError,match='Active version changed'):
        train_candidate(ws, tmp_path/'degraded.json', inputs/'feedback.csv')
    batch_predict(ws, output_name='response-batch')
    incident = write_incident(ws,tmp_path/'degraded.json',tmp_path/'good.json',tmp_path/'incident.json',
        'Labeled error justified a candidate; the response comparison passed.', 'Facilities analyst: inspect the next labeled cohort.')
    assert incident['resulting_version']==good['version']
    assert [item['time'] for item in incident['timeline']] == sorted(item['time'] for item in incident['timeline'])
    assert incident['alias_events'][-1]['new_version'] == good['version']
    activate(ws, version, 'Prepared operational incident: restore prior approved version; quality follow-up remains explicit')
    batch_predict(ws, output_name='rollback-batch')
    rollback = write_incident(ws,tmp_path/'degraded.json',tmp_path/'good.json',tmp_path/'rollback-incident.json',
        'Restored the prior approved version after a separate operational rejection; the labeled degradation remains a follow-up.',
        'Facilities analyst: investigate the unresolved current-condition quality before normal service resumes.', batch_name='rollback-batch')
    assert rollback['action'] == 'rolled_back' and rollback['resulting_version'] == version
    bundle=export_run(ws,good['run_id'],tmp_path/'export')
    assert verify_bundle(bundle)['data_sha256'] != original['data_sha256']
    offline=ws.path.rename(tmp_path/'offline')
    try:
        receiving=reproduce_bundle(bundle,tmp_path/'received')
        assert receiving['passed'] and receiving['absolute_rmse_delta'] <= 1e-6
    finally: offline.rename(ws.path)
    source=bundle/'training-data.csv'; source.write_text(source.read_text()+'\n')
    with pytest.raises(ValueError,match='changed'):
        verify_bundle(bundle)


def test_monitoring_rejects_invalid_policy_and_contract_inputs(tmp_path):
    for kwargs in [{'min_rows':0},{'max_rmse_kwh':float('nan')},{'hour':-1},{'min_labels':2.5}]:
        with pytest.raises(ValueError): Policy(**kwargs)
    inputs=tmp_path/'inputs';prepare_monitoring(inputs)
    with pytest.raises(ValueError,match='must not exist'):prepare_monitoring(inputs)
    from linden_mlops.operations import _inputs
    original=pd.read_csv(inputs/'current.csv')
    for frame in [original.assign(hour=24),original.assign(occupancy=np.nan),original.assign(row_id='duplicate')]:
        frame.to_csv(inputs/'broken.csv',index=False)
        with pytest.raises(ValueError):_inputs(inputs/'broken.csv')
