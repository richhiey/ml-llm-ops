"""Check the model, source recipe and delivered job selected for a release."""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .lifecycle import MODEL_NAME, write_json, code_revision
from .pipeline import sha256


def _verify(workspace, descriptor):
    required = {'model_name', 'version', 'run_id', 'batch_name'}
    if not isinstance(descriptor, dict) or not required.issubset(descriptor):
        raise ValueError('Release needs model_name, version, run_id and batch_name')
    if descriptor['model_name'] != MODEL_NAME:
        raise ValueError('Release model name differs from this application')
    name = descriptor['batch_name']
    if not isinstance(name, str) or not name or Path(name).name != name or name in {'.', '..'}:
        raise ValueError('Release batch_name must be a simple job name')
    active = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')
    if str(active.version) != str(descriptor['version']) or active.run_id != descriptor['run_id']:
        raise ValueError('Release must name the current active version and its source run')
    if active.tags.get('validation_status') != 'approved':
        raise ValueError('Release active version must be approved')
    run = workspace.client.get_run(active.run_id)
    score = run.data.metrics.get('rmse_kwh', float('nan'))
    if (run.data.params.get('evaluation_partition') != 'validation'
            or run.data.params.get('range_guard') != 'True'
            or not math.isfinite(score) or score > 5):
        raise ValueError('Release needs guarded validation evidence within approval policy')
    config = {'alpha': float(run.data.params['alpha']), 'range_guard': True,
              'autolog': run.data.params['autolog'] == 'True'}
    batch = json.loads((workspace.path / f'{name}.json').read_text())
    output = pd.read_csv(workspace.path / f'{name}.csv')
    if (batch.get('run_id') != active.run_id or str(batch.get('resolved_version')) != str(active.version)
            or batch.get('model') != MODEL_NAME):
        raise ValueError('Release batch was produced by a different model version or run')
    serving_revision = batch.get('serving_code_revision')
    if (serving_revision != run.data.params.get('code_revision')
            or serving_revision != code_revision()):
        raise ValueError('Release needs one current training and serving source revision; '
                         'revalidate the recipe and deliver a fresh batch after source changes')
    inputs = pd.read_csv(batch['input_path'])
    seconds = batch.get('elapsed_seconds', float('nan'))
    if (sha256(batch['input_path']) != batch['input_sha256']
            or list(output.columns) != ['row_id', 'prediction_kwh']
            or output.row_id.tolist() != inputs.row_id.tolist()
            or output.row_id.isna().any() or output.row_id.duplicated().any()
            or not np.isfinite(output.prediction_kwh).all()
            or batch.get('rows') != len(output) or len(output) != 24
            or not batch.get('complete_within_60s') or not math.isfinite(seconds)
            or not 0 < seconds <= 60):
        raise ValueError('Release batch fails input identity, output or delivery acceptance')
    verified = {'schema_version': 1, 'model_name': MODEL_NAME, 'version': str(active.version),
                'run_id': active.run_id, 'batch_name': name, 'config': config,
                'data_sha256': run.data.params['data_sha256'],
                'code_revision': run.data.params['code_revision'],
                'serving_code_revision': batch['serving_code_revision'],
                'batch_input_sha256': batch['input_sha256']}
    for key, expected in verified.items():
        if key in descriptor and descriptor[key] != expected:
            raise ValueError(f'Release {key} differs from observed evidence')
    return verified


def verify_release(workspace, path):
    """Validate a user-authored descriptor against actual registry and job records."""
    return _verify(workspace, json.loads(Path(path).read_text()))


def write_release(workspace, version, batch_name, destination):
    """Write an observed release descriptor once; never replace an existing record."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Release destination must not exist')
    version = workspace.client.get_model_version(MODEL_NAME, str(version))
    result = _verify(workspace, {'model_name': MODEL_NAME, 'version': str(version.version),
                                'run_id': version.run_id, 'batch_name': batch_name})
    destination.parent.mkdir(parents=True, exist_ok=True)
    write_json(destination, result)
    return result
