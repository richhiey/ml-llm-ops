"""Exercise persistence and recovery through actual MLflow records and files."""
import json
import pytest
from linden_mlops import Config, Workspace, export_runs
from linden_mlops.project import Project
from linden_mlops.recovery import export_run, restore_source, verify_bundle, reproduce_bundle


def test_selected_configuration_survives_new_sessions_and_portable_recovery(tmp_path):
    project = Project(work_dir=tmp_path/'project')
    alphas = project.plan([.2, .4, 1, 5, 20])
    ws = Workspace(project.tracking)
    records = [ws.run(Config(alpha=a, range_guard=True, autolog=True)) for a in alphas]
    project.record_matrix(ws, records)
    best = project.matrix(ws).sort_values('rmse_kwh').iloc[0]
    selection = project.select(ws, best.run_id)
    resumed = Project(work_dir=project.work)
    assert resumed.selected() == selection
    assert selection['config']['alpha'] == .2, 'Do not silently restore the reference alpha .01'
    assert resumed.require('matrix_run_ids') == [r['run_id'] for r in records]
    assert len(export_runs(ws)) == 5, 'Resuming must not train the matrix again'
    worst = project.matrix(ws).sort_values('rmse_kwh').iloc[-1]
    with pytest.raises(ValueError, match='lowest validation'):
        resumed.select(ws, worst.run_id)
    assert Project(work_dir=project.work).selected() == selection
    with pytest.raises(ValueError, match='completed matrix'):
        resumed.plan([.01, .1, 1, 10, 100])
    bundle = export_run(ws, best.run_id, tmp_path/'bundle')
    assert verify_bundle(bundle)['config'] == selection['config']
    source = restore_source(bundle, tmp_path/'restored')
    assert (source/'src/linden_mlops/pipeline.py').is_file()
    assert (source/'uv.lock').is_file()
    with pytest.raises(ValueError, match='must not exist'):
        restore_source(bundle, source)
    # The replay reads exported recipe files, not original database/artifact paths.
    original = project.tracking.rename(project.work/'original-offline')
    try:
        report = reproduce_bundle(bundle, tmp_path/'received')
        assert report['passed'] and report['config'] == selection['config']
        assert report['absolute_rmse_delta'] <= 1e-6
    finally:
        original.rename(project.tracking)
    config = bundle/'config.json'
    config.write_text('{}')
    with pytest.raises(ValueError, match='changed'):
        verify_bundle(bundle)


def test_project_requires_valid_plan_and_explicit_progress(tmp_path):
    project = Project(work_dir=tmp_path)
    for values in [[1]*5,[.1,.2,.3,.4,.5],[-1,.2,1,2,3],[.1,.2,1,2,float('nan')]]:
        with pytest.raises(ValueError):project.plan(values)
    with pytest.raises(ValueError, match='earlier selection'):
        project.selected()
    project.save(stage_complete={'source':'observed'})
    assert Project(work_dir=tmp_path).require('stage_complete')['source']=='observed'


def test_cli_reuses_matrix_and_selected_config(tmp_path, capsys):
    from linden_mlops.cli import main
    work = tmp_path / 'cli-project'
    config = tmp_path / 'experiment.json'
    config.write_text(json.dumps({'alphas':[.2,.4,1,5,20], 'primary_metric':'rmse_kwh',
                                 'direction':'minimize', 'partition':'validation'}))
    def command(name, *args):
        main([name, '--work-dir', str(work), *args])
        return capsys.readouterr().out
    command('plan', '--config', str(config))
    command('matrix')
    project = Project(work_dir=work)
    ids = project.require('matrix_run_ids')
    command('matrix')
    assert Project(work_dir=work).require('matrix_run_ids') == ids
    ws = Workspace(project.tracking)
    assert len(export_runs(ws)) == 5
    best = project.matrix(ws).sort_values('rmse_kwh').iloc[0]
    # Explicit run registration also works before a project selection is saved.
    assert json.loads(command('register', '--run-id', best.run_id))['run_id'] == best.run_id
    command('select', '--run-id', best.run_id)
    assert json.loads((work/'selected-config.json').read_text())['alpha'] == .2
    first = json.loads(command('register'))
    assert json.loads(command('register')) == first
    with pytest.raises(SystemExit) as error:
        command('activate', '--reason', 'Pending probe')
    assert error.value.code == 2
    command('approve', '--reason', 'Observed contract checks and validation acceptance')
    command('activate', '--reason', 'Explicit selected run')
    evidence = json.loads(command('batch'))
    assert evidence['run_id'] == best.run_id
    final = json.loads(command('final'))
    assert json.loads(command('final'))['run_id'] == final['run_id']
    assert len(export_runs(ws)) == 6
