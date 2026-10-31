"""Actual model loading, job preservation and release/export acceptance."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from linden_mlops import Config, Workspace, register, approve, activate, batch_predict
from linden_mlops.lifecycle import MODEL_NAME, verify_summary
from linden_mlops.pipeline import DATA
from linden_mlops.release import verify_release, write_release
from linden_mlops.recovery import export_run, verify_bundle


@pytest.fixture(scope='module')
def trained(tmp_path_factory):
    root = tmp_path_factory.mktemp('delivery')
    ws = Workspace(root / 'store')
    run = ws.run(Config(range_guard=True), name='forecast')
    source = root / 'planned.csv'
    source.write_bytes((DATA / 'batch-v1.csv').read_bytes())
    return ws, run, source


def test_explicit_model_delivery_needs_no_registry_and_preserves_existing_jobs(trained):
    ws, run, source = trained
    output, observed = batch_predict(ws, source, 'explicit', model_uri=run['model_uri'])
    assert observed['run_id'] == run['run_id'] and observed['resolved_version'] is None
    assert output.row_id.tolist() == pd.read_csv(source).row_id.tolist()
    assert np.isfinite(output.prediction_kwh).all()
    before = (ws.path / 'explicit.csv').read_bytes(), (ws.path / 'explicit.json').read_bytes()
    with pytest.raises(ValueError, match='already exists'):
        batch_predict(ws, source, 'explicit', model_uri=run['model_uri'])
    assert before == ((ws.path / 'explicit.csv').read_bytes(), (ws.path / 'explicit.json').read_bytes())
    with pytest.raises(ValueError, match='simple filename'):
        batch_predict(ws, source, '../escape', model_uri=run['model_uri'])


def test_release_consumes_actual_model_job_and_rejects_inconsistent_descriptor(trained, tmp_path):
    ws, run, source = trained
    version = register(ws, run['run_id'])
    approve(ws, version, 'Observed guarded validation and input regression checks')
    activate(ws, version, 'Explicit release candidate')
    batch_predict(ws, source, 'release-job')
    path = tmp_path / 'release.json'
    result = write_release(ws, version, 'release-job', path)
    assert verify_release(ws, path) == result
    for changed in [dict(result, run_id='wrong'), dict(result, version='999'),
                    dict(result, data_sha256='different'), dict(result, config={'alpha': 999})]:
        path.write_text(json.dumps(changed))
        with pytest.raises(ValueError):
            verify_release(ws, path)
    path.write_text(json.dumps(result))
    metadata = ws.path / 'release-job.json'
    retained_metadata = metadata.read_bytes()
    try:
        changed_source = json.loads(retained_metadata)
        changed_source['serving_code_revision'] = 'sha256:unexported-serving-change'
        metadata.write_text(json.dumps(changed_source))
        with pytest.raises(ValueError, match='training and serving source'):
            verify_release(ws, path)
        with pytest.raises(ValueError, match='training and serving source'):
            export_run(ws, run['run_id'], tmp_path / 'stale-source-export', release=path)
        assert not (tmp_path / 'stale-source-export').exists()
    finally:
        metadata.write_bytes(retained_metadata)
    output = ws.path / 'release-job.csv'
    before = output.read_bytes()
    try:
        pd.read_csv(output).iloc[::-1].to_csv(output, index=False)
        with pytest.raises(ValueError, match='delivery acceptance'):
            verify_release(ws, path)
    finally:
        output.write_bytes(before)
    bundle = export_run(ws, run['run_id'], tmp_path / 'bundle', release=path)
    assert verify_bundle(bundle)['run_id'] == result['run_id']
    assert json.loads((bundle / 'release.json').read_text()) == result
    with pytest.raises(ValueError, match='differs'):
        export_run(ws, 'different-run', tmp_path / 'wrong-export', release=path)
    assert not (tmp_path / 'wrong-export').exists()


def test_cli_export_requires_explicit_run_or_verified_release(tmp_path):
    from linden_mlops.cli import main
    destination = tmp_path / 'export'
    with pytest.raises(SystemExit) as error:
        main(['export', '--work-dir', str(tmp_path / 'project'), '--destination', str(destination)])
    assert error.value.code == 2
    assert not destination.exists()


def test_numeric_comparison_accepts_declared_population_without_course_count():
    rows = pd.DataFrame([dict(run_id=f'run-{i}', alpha=str(alpha), rmse_kwh=score,
        comparison_group='facility-2026-validation', data_sha256='same-data',
        code_revision='same-source', range_guard='True', evaluation_partition='validation')
        for i, (alpha, score) in enumerate([(.2, 2.), (.4, 1.)])])
    assert verify_summary(rows, 'run-1')['recommendation_matches_metric']
    assert verify_summary(rows.iloc[:1], 'run-0')['recommendation_matches_metric']
    with pytest.raises(ValueError, match='distinct'):
        verify_summary(rows.assign(alpha='.2'), 'run-1')
