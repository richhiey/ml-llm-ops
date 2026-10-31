"""Instructor-only preparation of isolated acceptance inputs outside the app.

Comparison/receiving copy retained records. Registry incident setup
trains, registers and activates models only in a new explicitly chosen client
store; it never edits the cumulative project's state or source. Monitoring setup
creates labeled synthetic data. These operations are fixture provisioning,
not student application work or evidence of a new assistant interaction.
"""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import tempfile

from linden_mlops.lifecycle import MODEL_NAME, ROOT, Workspace, register, approve, activate
from linden_mlops import Config, run_matrix
from linden_mlops.operations import Policy
from linden_mlops.pipeline import TARGET, sha256
from dataclasses import asdict
import numpy as np
import pandas as pd
from linden_mlops.project import Project
from linden_mlops.recovery import verify_bundle


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def open_project(work_dir=None):
    work = Path(work_dir or os.environ.get('LINDEN_WORK_DIR', ROOT / 'work')).resolve()
    # Project/Workspace create missing directories. Require an existing project
    # before constructing either so a failed exercise cannot seed empty state.
    if not (work / 'project.json').is_file() or not (work / 'tracking/mlflow.db').is_file():
        raise ValueError('Complete the cumulative project activities first; existing project.json and tracking store are required')
    project = Project(work_dir=work)
    workspace = Workspace(project.tracking)
    return project, workspace


def comparison(project, workspace):
    rows = project.matrix(workspace)
    observations = []
    anchor = None
    for number, run_id in enumerate(project.require('matrix_run_ids'), 1):
        run = workspace.client.get_run(run_id)
        observations.append({
            'observation_id': f'observation-{number:02d}', 'run_id': run_id,
            'alpha': float(run.data.params['alpha']), 'metric_name': 'rmse_kwh',
            'evaluation_basis': run.data.params['evaluation_partition'],
            'value': float(run.data.metrics['rmse_kwh']),
            'controls': dict(run.data.params),
            'comparison_group': run.data.tags.get('comparison_group'),
        })
        if float(run.data.params['alpha']) == 1.0:
            anchor = run
    metric = 'training_root_mean_squared_error'
    if anchor is None or metric not in anchor.data.metrics:
        raise ValueError('The completed matrix needs an already autologged alpha=1 training_root_mean_squared_error observation; do not retrain to prepare this task')
    value = float(anchor.data.metrics[metric])
    if not math.isfinite(value) or value < 0:
        raise ValueError('Recorded training RMSE must be finite and nonnegative')
    observations.append({
        'observation_id': 'observation-06', 'run_id': anchor.info.run_id,
        'alpha': float(anchor.data.params['alpha']), 'metric_name': metric,
        'evaluation_basis': 'training', 'value': value,
        'controls': dict(anchor.data.params),
        'comparison_group': anchor.data.tags.get('comparison_group'),
    })
    # rows is intentionally obtained through Project.matrix to enforce its
    # source/data/comparability requirements, not reconstructed by sorting IDs.
    assert len(rows) == 5
    evidence = {'schema_version': 1, 'provenance': {
        'source': 'existing_project_tracking_records',
        'project_record': str(project.file), 'tracking_store': str(project.tracking),
    }, 'observations': observations}
    note = (
        'Harbor Facilities: authored exercise note for review\n\n'
        'This is a deliberately questionable stakeholder draft, not a response '
        'from your assistant or an observed operational result.\n\n'
        f'I recommend observation-06 (run {anchor.info.run_id}) as a sixth '
        'independent candidate in this comparison. Its RMSE is lower, so it '
        'should be cheaper to operate and is ready for deployment. Please '
        'confirm this recommendation for the planner.\n\n'
        'Review the recorded observations and controls. Produce a corrected '
        'comparison and an evidence-bounded recommendation with source run IDs. '
        'Identify which claims still need separate evidence.\n'
    )
    return {'observations.json': evidence, 'client-note.txt': note}




def prepare(command, destination, work_dir=None, bundle=None):
    if command not in {'comparison', 'receiving'}:
        raise ValueError('Unknown external evidence preparation kind')
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Exercise destination must not exist; retain earlier evidence')
    source = None
    if command == 'receiving':
        work = Path(work_dir or os.environ.get('LINDEN_WORK_DIR', ROOT / 'work')).resolve()
        source = Path(bundle).resolve() if bundle else work / 'handoff-export'
        verify_bundle(source)
        config = json.loads((source / 'config.json').read_text())
        original_alpha = float(config['alpha'])
        if not math.isfinite(original_alpha) or original_alpha <= 0:
            raise ValueError('Exported alpha must be finite and positive')
        config['alpha'] = original_alpha / 2 if original_alpha > 1 else original_alpha + 1
        if destination == source or source in destination.parents:
            raise ValueError('Exercise destination must be outside the original export')
        files = {'brief.txt': (
            'Harbor Facilities: receiving review\n\n'
            'candidate-bundle is a deliberately damaged exercise copy of your '
            'verified handoff export. The original export is retained unchanged. '
            'Inspect this candidate as the receiving engineer. Decide whether '
            'it is safe to replay, diagnose any failed integrity check, and '
            'repair only the copy from trusted evidence before replaying it. '
            'Keep the recorded checksum index as the acceptance contract. '
            'Retain the rejection, your repair rationale, and the subsequent '
            'verification result.\n'
        )}
    else:
        project, workspace = open_project(work_dir)
        if destination == project.work or destination in project.work.parents:
            raise ValueError('Exercise destination must not replace the project')
        if destination == project.tracking or project.tracking in destination.parents:
            raise ValueError('Exercise destination must be outside the original tracking store')
        files = comparison(project, workspace)
    # Build in a sibling staging directory, then publish atomically. Failures
    # leave no half-prepared exercise and never replace an existing destination.
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.course-evidence-', dir=destination.parent))
    try:
        for name, value in files.items():
            if isinstance(value, dict):
                write_json(staging / name, value)
            else:
                (staging / name).write_text(value)
        if source is not None:
            shutil.copytree(source, staging / 'candidate-bundle')
            write_json(staging / 'candidate-bundle/config.json', config)
        # rename on POSIX refuses an existing nonempty directory; explicitly
        # check again so even an empty exercise destination is not overwritten.
        if destination.exists():
            raise ValueError('Exercise destination must not exist; retain earlier evidence')
        staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return destination



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


def prepare_case(case, state):
    if case not in {'matrix', 'rollback', 'registry-assessment', 'past-run'}:
        raise ValueError('Unknown case')
    path = Path(state).resolve()
    if path.exists():
        raise ValueError('Use a new state path; existing evidence is preserved')
    ws = Workspace(path)
    index = {'case': case, 'state': str(path)}
    if case == 'matrix':
        records = run_matrix(ws, autolog=True)
        ids = [record['run_id'] for record in records]
        (path / 'matrix-run-ids.json').write_text(json.dumps(ids, indent=2) + '\n')
        rows = export_runs(ws)
        rows[rows.run_id.isin(ids)].to_csv(path / 'runs.csv', index=False)
        index['run_ids'] = ids
    else:
        configurations = {'rollback': [1, 10], 'registry-assessment': [.1, 10, 100], 'past-run': [1]}
        versions = []
        for number, alpha in enumerate(configurations[case], start=1):
            record = ws.run(Config(alpha=alpha, range_guard=True, autolog=True), name=f'intake-{number}')
            version = register(ws, record['run_id'])
            versions.append(version)
            if alpha != 100:
                approve(ws, version, 'Original guarded finite validation RMSE<=5 policy; inspect raw evidence')
                activate(ws, version, 'Initial client selection' if number == 1 else 'Client trial before revised acceptance')
        index['registered_versions'] = versions
        if case == 'registry-assessment':
            index['incident'] = 'Client now requires validation RMSE<=1.45 kWh; retain all versions and restore a suitable previously approved version.'
        elif case == 'rollback':
            index['incident'] = 'Client now requires validation RMSE<=1.6 kWh; inspect the current trial and the earlier approved version.'
        else:
            index['past_run_id'] = record['run_id']
    (path / 'case.json').write_text(json.dumps(index, indent=2) + '\n')
    return index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['comparison', 'receiving', 'rollback', 'registry-assessment', 'past-run', 'monitoring'])
    parser.add_argument('--destination', required=True, help='New isolated exercise directory')
    parser.add_argument('--work-dir', help='Existing cumulative project work directory')
    parser.add_argument('--cohort', choices=['linden', 'harbor'], default='linden')
    parser.add_argument('--bundle', help='Existing verified export (receiving only)')
    args = parser.parse_args(argv)
    if args.bundle and args.command != 'receiving':
        parser.error('--bundle is available only for receiving')
    try:
        if args.command == 'monitoring':
            print(json.dumps(prepare_monitoring(args.destination, args.cohort), indent=2))
        elif args.command in {'rollback', 'registry-assessment', 'past-run'}:
            print(json.dumps(prepare_case(args.command, args.destination), indent=2))
        else:
            print(prepare(args.command, args.destination, args.work_dir, args.bundle))
    except (ValueError, FileNotFoundError, KeyError, StopIteration) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
