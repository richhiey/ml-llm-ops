"""Prepare isolated Campus evidence tasks from the learner's existing project.

This tool reads completed evidence; it never trains, selects, registers, promotes,
or edits the cumulative project. Deliberate exercise changes live only in a new
destination. Run with `uv run python -m linden_mlops.course_evidence --help`.
"""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import tempfile

from linden_mlops.lifecycle import MODEL_NAME, ROOT, Workspace
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


def integration(project, workspace):
    selection = project.selected()
    rows = project.matrix(workspace)
    registry = project.require('registry')
    version = workspace.client.get_model_version(MODEL_NAME, str(registry['version']))
    if registry['run_id'] != selection['run_id'] or version.run_id != selection['run_id']:
        raise ValueError('Saved selected run and registered version must agree before preparing the handover task')
    active = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')
    if str(active.version) != str(version.version) or active.run_id != selection['run_id']:
        raise ValueError('The main active alias must point to the selected registered version')
    batch_path = workspace.path / 'batch.json'
    csv_path = workspace.path / 'batch.csv'
    batch = json.loads(batch_path.read_text())
    if (batch.get('run_id') != selection['run_id']
            or str(batch.get('resolved_version')) != str(version.version)
            or batch.get('model') != MODEL_NAME or not csv_path.is_file()):
        raise ValueError('Retain batch.json and batch.csv for the main selected active model before preparing this task')
    alternate = next(run_id for run_id in rows.run_id if run_id != selection['run_id'])
    draft = {
        'schema_version': 1,
        'record_type': 'draft_exercise_handoff_index',
        'notice': 'Intentionally mixed draft index for an investigation exercise; this is not an execution record.',
        'training_run_id': alternate,
        'registered_version': str(version.version), 'model_name': MODEL_NAME,
        'batch_evidence_path': str(batch_path), 'batch_predictions_path': str(csv_path),
    }
    brief = (
        'Harbor Facilities: draft handover review\n\n'
        'The draft index was assembled from existing records and may contain a '
        'mismatch. Establish whether its training, registered artifact and '
        'retained inference evidence form one coherent chain. Correct the '
        'draft index in this exercise directory and retain a short explanation '
        'pointing to the authoritative records you used. Preserve the original '
        'project, registry, alias and batch artifacts. Do not train or promote '
        'a replacement to make the draft appear consistent.\n'
    )
    return {'handoff-index.json': draft, 'brief.txt': brief}


def prepare(command, destination, work_dir=None, bundle=None):
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
        files = comparison(project, workspace) if command == 'comparison' else integration(project, workspace)
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['comparison', 'integration', 'receiving'])
    parser.add_argument('--destination', required=True, help='New isolated exercise directory')
    parser.add_argument('--work-dir', help='Existing cumulative project work directory')
    parser.add_argument('--bundle', help='Existing verified export (receiving only)')
    args = parser.parse_args(argv)
    if args.bundle and args.command != 'receiving':
        parser.error('--bundle is available only for receiving')
    try:
        print(prepare(args.command, args.destination, args.work_dir, args.bundle))
    except (ValueError, FileNotFoundError, KeyError, StopIteration) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
