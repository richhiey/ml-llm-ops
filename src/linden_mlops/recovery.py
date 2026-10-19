"""Export a run as portable files and verify a new execution against its recipe."""
from pathlib import Path
import json
import shutil
import tarfile
import mlflow

from .pipeline import Config, DATA, sha256
from .lifecycle import (Workspace, code_revision, environment, register, approve,
                        activate, batch_predict, TOLERANCE, write_json)


def export_run(workspace, run_id, destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Export destination must not exist; retain earlier evidence')
    destination.mkdir(parents=True)
    workspace.connect()
    reproduction = Path(workspace.client.download_artifacts(run_id, 'reproduction'))
    for name in ['manifest.json', 'config.json', 'environment.txt', 'source.tar.gz']:
        shutil.copy2(reproduction / name, destination / name)
    manifest = json.loads((destination / 'manifest.json').read_text())
    model = Path(mlflow.artifacts.download_artifacts(artifact_uri=manifest['model_uri']))
    shutil.copytree(model, destination / 'model')
    files = {str(p.relative_to(destination)): sha256(p)
             for p in sorted(destination.rglob('*')) if p.is_file()}
    write_json(destination / 'bundle.json', {'schema_version': 1, 'run_id': run_id, 'files': files})
    return destination


def verify_bundle(bundle):
    bundle = Path(bundle).resolve()
    index = json.loads((bundle / 'bundle.json').read_text())
    required = {'manifest.json', 'config.json', 'environment.txt', 'source.tar.gz'}
    if index.get('schema_version') != 1 or not required.issubset(index.get('files', {})):
        raise ValueError('Incomplete recovery bundle')
    if not any(name.startswith('model/') for name in index['files']):
        raise ValueError('Recovery bundle needs the fitted model files')
    for name, expected in index['files'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe recovery path')
        file = bundle / relative
        if not file.is_file() or sha256(file) != expected:
            raise ValueError(f'Recovery file missing or changed: {name}')
    return json.loads((bundle / 'manifest.json').read_text())


def restore_source(bundle, destination):
    """Extract only into a new directory; Python's data filter rejects unsafe members."""
    bundle, destination = Path(bundle).resolve(), Path(destination).resolve()
    verify_bundle(bundle)
    if destination.exists():
        raise ValueError('Source destination must not exist')
    with tarfile.open(bundle / 'source.tar.gz') as archive:
        members = archive.getmembers()
        if any(Path(m.name).is_absolute() or '..' in Path(m.name).parts for m in members):
            raise ValueError('Unsafe source archive path')
        destination.mkdir(parents=True)
        archive.extractall(destination, filter='data')
    return destination


def reproduce_bundle(bundle, destination):
    """Run from restored source/environment; never consult the original tracking store."""
    original = verify_bundle(bundle)
    invariants = {'source': original['code_revision'] == code_revision(),
                  'data': original['data_sha256'] == sha256(DATA / 'demand-v1.csv'),
                  'environment': original['environment'] == environment()}
    if not all(invariants.values()):
        raise ValueError(f'Restore the recorded recipe before training: {invariants}')
    if original['evaluation_partition'] != 'validation':
        raise ValueError('Lifecycle recovery requires a selected validation run, not a final observation')
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError('Receiving state must not exist')
    ws = Workspace(destination)
    result = ws.run(Config(**original['config']), name='received-validation', partition='validation')
    invariants.update(config=result['config'] == original['config'],
                      partition=result['evaluation_partition'] == original['evaluation_partition'])
    delta = abs(result['metrics']['rmse_kwh'] - original['metrics']['rmse_kwh'])
    version = register(ws, result['run_id'])
    approve(ws, version, 'Recovered recipe; finite guarded validation acceptance checked; inspect contract tests separately')
    activate(ws, version, 'Receiving run from exported source/configuration/environment')
    output, inference = batch_predict(ws)
    report = {'original_run_id': original['run_id'], 'reproduced_run_id': result['run_id'],
              'invariants': invariants, 'absolute_rmse_delta': delta, 'tolerance': TOLERANCE,
              'config': result['config'], 'version': version, 'inference': inference,
              'passed': all(invariants.values()) and delta <= TOLERANCE
                        and len(output) == 24 and inference['complete_within_60s']}
    write_json(ws.path / 'recovery-check.json', report)
    return report
