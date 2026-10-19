"""Durable project decisions shared by notebooks, scripts and CLI sessions."""
from pathlib import Path
import json
import os
import tempfile

from .pipeline import Config, DATA, sha256
from .lifecycle import ROOT, code_revision, export_runs, verify_summary


class Project:
    """One working tree, one local tracking directory, explicit saved decisions.

    Run IDs are references into this project's store, never instructions to rerun a
    completed step. Portable handoffs use exported artifacts rather than copying
    this local workspace's absolute MLflow paths.
    """

    def __init__(self, root=ROOT, work_dir=None):
        self.root = Path(root).resolve()
        if not (self.root / 'src/linden_mlops/pipeline.py').is_file():
            raise ValueError('Open the repository containing pyproject.toml and src/linden_mlops')
        self.work = Path(work_dir or os.environ.get('LINDEN_WORK_DIR', self.root / 'work')).resolve()
        self.work.mkdir(parents=True, exist_ok=True)
        self.file = self.work / 'project.json'
        self.tracking = self.work / 'tracking'
        self.data = json.loads(self.file.read_text()) if self.file.exists() else {'schema_version': 1}
        if self.data.get('schema_version') != 1:
            raise ValueError('Unsupported project record version')

    def reload(self):
        if self.file.exists():
            self.data = json.loads(self.file.read_text())
        return self

    def save(self, **changes):
        self.reload()
        self.data.update(changes)
        fd, temporary = tempfile.mkstemp(prefix='.project-', dir=self.work, text=True)
        try:
            with os.fdopen(fd, 'w') as stream:
                json.dump(self.data, stream, indent=2, sort_keys=True)
                stream.write('\n')
            os.replace(temporary, self.file)
        finally:
            Path(temporary).unlink(missing_ok=True)
        return self.data

    def require(self, key):
        self.reload()
        if not self.data.get(key):
            raise ValueError(f'Complete the earlier {key.replace("_", " ")} activity in this project first')
        return self.data[key]

    def plan(self, alphas):
        values = [float(a) for a in alphas]
        if len(values) != 5 or len(set(values)) != 5 or 1.0 not in values:
            raise ValueError('Declare five distinct positive alphas including the comparison anchor 1')
        for alpha in values:
            Config(alpha=alpha)
        if self.data.get('matrix_run_ids') and values != self.data.get('planned_alphas'):
            raise ValueError('A completed matrix exists. Start a new work directory for a deliberate new comparison')
        self.save(planned_alphas=values)
        return values

    def record_matrix(self, workspace, records):
        ids = [record['run_id'] for record in records]
        if len(ids) != 5 or len(set(ids)) != 5:
            raise ValueError('Record the five distinct completed executions')
        rows = export_runs(workspace)
        rows = rows[rows.run_id.isin(ids)].copy()
        verify_summary(rows, ids[0])  # validate comparability, not the proposed choice
        if set(rows.alpha.astype(float)) != set(self.require('planned_alphas')):
            raise ValueError('Executed configurations differ from the declared matrix')
        if not rows.code_revision.eq(code_revision()).all():
            raise ValueError('The matrix does not use the current working source')
        self.save(matrix_run_ids=ids, matrix_source=code_revision(), selection=None,
                  registry=None, final_evaluation=None)
        return rows

    def matrix(self, workspace):
        ids = self.require('matrix_run_ids')
        if self.data['matrix_source'] != code_revision():
            raise ValueError('Source changed after the matrix. Declare and verify a new comparison in a new work directory')
        all_rows = export_runs(workspace)
        if 'run_id' not in all_rows:
            raise ValueError('Saved run IDs are missing from this tracking store')
        rows = all_rows[all_rows.run_id.isin(ids)].copy()
        verify_summary(rows, ids[0])
        if len(rows) != len(ids):
            raise ValueError('Saved run IDs are missing from this tracking store')
        return rows

    def select(self, workspace, run_id):
        rows = self.matrix(workspace)
        result = verify_summary(rows, run_id)
        if not result['recommendation_matches_metric']:
            raise ValueError('Selection must match the declared lowest validation RMSE; inspect controls and raw values')
        run = workspace.client.get_run(run_id)
        config = {'alpha': float(run.data.params['alpha']),
                  'range_guard': run.data.params['range_guard'] == 'True',
                  'autolog': run.data.params['autolog'] == 'True'}
        selection = {'run_id': run_id, 'config': config, 'code_revision': code_revision(),
                     'data_sha256': sha256(DATA / 'demand-v1.csv')}
        if self.data.get('selection') != selection:
            self.save(selection=selection, registry=None, final_evaluation=None)
        return selection

    def selected(self):
        selection = self.require('selection')
        if selection['code_revision'] != code_revision() or selection['data_sha256'] != sha256(DATA / 'demand-v1.csv'):
            raise ValueError('Selected run belongs to different source/data. Revalidate the experiment before promotion')
        return selection
