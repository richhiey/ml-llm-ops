"""Repeatable client incidents for investigation; preparation leaves decisions open."""
from pathlib import Path
import json
from . import Workspace, Config, run_matrix, export_runs, register, approve, activate


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
