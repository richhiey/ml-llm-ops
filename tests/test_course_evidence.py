"""Real-record provenance and isolation for the Campus evidence investigations."""
import json
from pathlib import Path
import shutil

import pytest

from linden_mlops import Config, Workspace, activate, approve, register
from linden_mlops import course_evidence as evidence
from linden_mlops.lifecycle import MODEL_NAME, batch_predict, export_runs
from linden_mlops.pipeline import sha256
from linden_mlops.project import Project
from linden_mlops.recovery import export_run, verify_bundle



@pytest.fixture(scope='module')
def completed_project(tmp_path_factory):
    location = tmp_path_factory.mktemp('evidence-project')
    project = Project(work_dir=location / 'work')
    workspace = Workspace(project.tracking)
    alphas = project.plan([.2, .4, 1, 5, 20])
    records = [workspace.run(Config(alpha=alpha, range_guard=True, autolog=True))
               for alpha in alphas]
    project.record_matrix(workspace, records)
    selected = project.select(workspace, project.matrix(workspace).sort_values('rmse_kwh').iloc[0].run_id)
    version = register(workspace, selected['run_id'])
    project.save(registry={'run_id': selected['run_id'], 'version': version})
    approve(workspace, version, 'Actual guarded validation evidence for isolated exercise test')
    activate(workspace, version, 'Isolated test fixture selected version')
    batch_predict(workspace)
    bundle = export_run(workspace, selected['run_id'], project.work / 'handoff-export')
    return project, workspace, bundle


def snapshot(directory):
    return {str(file.relative_to(directory)): sha256(file)
            for file in directory.rglob('*') if file.is_file()}


def test_exercises_preserve_source_and_expose_actual_evidence(completed_project, tmp_path):
    project, workspace, bundle = completed_project
    before = snapshot(project.work)
    count = len(export_runs(workspace))
    selected = project.selected()
    active = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')

    comparison = evidence.prepare('comparison', tmp_path / 'comparison', project.work)
    data = json.loads((comparison / 'observations.json').read_text())
    observations = data['observations']
    assert len(observations) == 6
    assert len({item['observation_id'] for item in observations}) == 6
    assert len({item['run_id'] for item in observations}) == 5
    for item in observations:
        actual = workspace.client.get_run(item['run_id'])
        assert item['controls'] == actual.data.params
        assert item['value'] == actual.data.metrics[item['metric_name']]
        assert item['alpha'] == float(actual.data.params['alpha'])
    assert all(item['metric_name'] == 'rmse_kwh' and item['evaluation_basis'] == 'validation'
               for item in observations[:5])
    assert observations[-1]['metric_name'] == 'training_root_mean_squared_error'
    assert observations[-1]['evaluation_basis'] == 'training'
    assert observations[-1]['alpha'] == 1
    assert observations[-1]['run_id'] in [item['run_id'] for item in observations[:5]]

    integration = evidence.prepare('integration', tmp_path / 'integration', project.work)
    draft = json.loads((integration / 'handoff-index.json').read_text())
    assert draft['record_type'] == 'draft_exercise_handoff_index'
    assert draft['training_run_id'] in project.require('matrix_run_ids')
    assert draft['training_run_id'] != selected['run_id']
    assert draft['registered_version'] == str(active.version)
    version = workspace.client.get_model_version(draft['model_name'], draft['registered_version'])
    inference = json.loads(Path(draft['batch_evidence_path']).read_text())
    assert version.run_id == inference['run_id'] == selected['run_id']
    assert workspace.client.get_model_version_by_alias(MODEL_NAME, 'active').version == active.version

    receiving = evidence.prepare('receiving', tmp_path / 'receiving', project.work)
    candidate = receiving / 'candidate-bundle'
    assert (candidate / 'bundle.json').read_bytes() == (bundle / 'bundle.json').read_bytes()
    assert json.loads((candidate / 'config.json').read_text())['alpha'] > 0
    assert (candidate / 'config.json').read_bytes() != (bundle / 'config.json').read_bytes()
    with pytest.raises(ValueError, match='changed: config.json'):
        verify_bundle(candidate)
    shutil.copy2(bundle / 'config.json', candidate / 'config.json')
    assert verify_bundle(candidate) == verify_bundle(bundle)
    assert len(export_runs(workspace)) == count, 'Preparation must never rerun training'
    assert snapshot(project.work) == before, 'Preparation must not alter source project or exported files'


def test_reject_missing_state_existing_dest_and_store_nesting(completed_project, tmp_path):
    destination = tmp_path / 'new'
    with pytest.raises(ValueError, match='Complete the cumulative'):
        evidence.prepare('comparison', destination, tmp_path / 'absent')
    assert not destination.exists()
    assert not (tmp_path / 'absent').exists()
    destination.mkdir()
    with pytest.raises(ValueError, match='must not exist'):
        evidence.prepare('receiving', destination, bundle=tmp_path / 'missing')
    assert list(destination.iterdir()) == []
    project, _, _ = completed_project
    nested = project.tracking / 'exercise'
    with pytest.raises(ValueError, match='outside the original tracking'):
        evidence.prepare('comparison', nested, project.work)
    assert not nested.exists()


def test_reject_untrusted_receiving_source_before_creating_destination(completed_project, tmp_path):
    _, _, bundle = completed_project
    damaged = tmp_path / 'damaged'
    shutil.copytree(bundle, damaged)
    (damaged / 'config.json').write_text('{}')
    destination = tmp_path / 'not-prepared'
    with pytest.raises(ValueError, match='changed: config.json'):
        evidence.prepare('receiving', destination, bundle=damaged)
    assert not destination.exists()
