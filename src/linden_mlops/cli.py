"""Command-line entry point for the local demand-model lifecycle."""
import argparse
import json
from pathlib import Path
import subprocess

from . import Config, Workspace, register, approve, activate, batch_predict, export_runs, reproduce
from .lifecycle import MODEL_NAME
from .project import Project
from .recovery import export_run, restore_source, reproduce_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['status', 'plan', 'train', 'matrix', 'compare', 'select',
        'register', 'approve', 'activate', 'inspect', 'batch', 'bootstrap', 'handoff', 'final',
        'reproduce', 'ui', 'export', 'restore-source', 'reproduce-export', 'prepare'])
    parser.add_argument('--work-dir', help='Project decisions directory (default: work, or LINDEN_WORK_DIR)')
    parser.add_argument('--state', help='Override tracking store for a separate investigation')
    parser.add_argument('--alpha', type=float, default=1.0)
    parser.add_argument('--range-guard', action='store_true')
    parser.add_argument('--autolog', action='store_true')
    parser.add_argument('--partition', choices=['validation', 'final'], default='validation')
    parser.add_argument('--run-id')
    parser.add_argument('--version')
    parser.add_argument('--reason', default='')
    parser.add_argument('--config', help='Configuration JSON; takes precedence over model flags')
    parser.add_argument('--bundle', help='Portable export directory')
    parser.add_argument('--destination', help='New destination directory')
    parser.add_argument('--input', help='Batch CSV; default is the bundled 24-row file')
    parser.add_argument('--output-name', default='batch')
    parser.add_argument('--case', choices=['matrix', 'rollback', 'registry-assessment', 'past-run'])
    args = parser.parse_args(argv)

    def required(name):
        value = getattr(args, name.replace('-', '_'))
        if value is None:
            parser.error(f'--{name} is required')
        return value

    try:
        if args.command == 'restore-source':
            result = str(restore_source(required('bundle'), required('destination')))
        elif args.command == 'reproduce-export':
            result = reproduce_bundle(required('bundle'), required('destination'))
        elif args.command == 'prepare':
            from .scenarios import prepare_case
            result = prepare_case(required('case'), required('state'))
        else:
            project = Project(work_dir=args.work_dir)
            if args.command == 'status':
                result = {'work_dir': str(project.work), 'tracking': str(project.tracking), **project.data}
            elif args.command == 'plan':
                config = json.loads(Path(required('config')).read_text())
                if (config.get('primary_metric'), config.get('direction'), config.get('partition')) != ('rmse_kwh', 'minimize', 'validation'):
                    raise ValueError('This comparison declares lowest validation rmse_kwh')
                result = {'planned_alphas': project.plan(config['alphas'])}
            else:
                ws = Workspace(args.state or project.tracking)
                primary = ws.path == project.tracking
                if args.command in {'matrix', 'compare', 'select', 'final'} and not primary:
                    raise ValueError('Use --work-dir for a cumulative project; --state is for separate investigations')
                if args.command == 'ui':
                    subprocess.run(['mlflow', 'server', '--backend-store-uri', ws.uri, '--host', '127.0.0.1', '--port', '5050'], check=True)
                    return
                if args.command == 'matrix':
                    if not project.data.get('matrix_run_ids'):
                        records = [ws.run(Config(alpha=a, range_guard=True, autolog=True), name=f'alpha-{a}')
                                   for a in project.require('planned_alphas')]
                        project.record_matrix(ws, records)
                    rows = project.matrix(ws)
                    rows.to_csv(project.work / 'runs.csv', index=False)
                    result = {'run_ids': rows.run_id.tolist(), 'csv': str(project.work / 'runs.csv')}
                elif args.command == 'compare':
                    rows = project.matrix(ws).sort_values('rmse_kwh')
                    print(rows.to_string(index=False)); return
                elif args.command == 'select':
                    result = project.select(ws, required('run-id'))
                    (project.work / 'selected-config.json').write_text(json.dumps(result['config'], indent=2) + '\n')
                elif args.command == 'register':
                    run_id = args.run_id or project.selected()['run_id']
                    existing = project.data.get('registry') if primary else None
                    version = existing['version'] if existing and existing['run_id'] == run_id else register(ws, run_id)
                    result = {'run_id': run_id, 'version': version}
                    if primary and (project.data.get('selection') or {}).get('run_id') == run_id:
                        project.save(registry=result)
                elif args.command in {'approve', 'activate'}:
                    version = args.version or (project.require('registry')['version'] if primary else required('version'))
                    if args.command == 'approve':
                        approve(ws, version, args.reason)
                        result = {'version': version, 'validation_status': 'approved'}
                    else:
                        result = activate(ws, version, args.reason)
                elif args.command == 'inspect':
                    rows = export_runs(ws)
                    print(rows.to_string(index=False))
                    for version in ws.client.search_model_versions(f"name='{MODEL_NAME}'"):
                        print(json.dumps({'version': version.version, 'run_id': version.run_id, 'tags': version.tags, 'aliases': version.aliases}, default=str))
                    return
                elif args.command == 'batch':
                    _, result = batch_predict(ws, args.input, args.output_name)
                elif args.command == 'export':
                    result = str(export_run(ws, args.run_id or project.selected()['run_id'], required('destination')))
                elif args.command == 'reproduce':
                    result = reproduce(ws, args.run_id or project.selected()['run_id'], required('destination'))
                elif args.command == 'final':
                    selection = project.selected()
                    if not project.data.get('final_evaluation'):
                        project.save(final_evaluation=ws.run(Config(**selection['config']), name='fixed-selection-final', partition='final'))
                    result = project.require('final_evaluation')
                else:
                    config = Config(**json.loads(Path(args.config).read_text())) if args.config else Config(
                        args.alpha, args.range_guard or args.command in {'bootstrap', 'handoff'}, args.autolog)
                    result = ws.run(config, partition=args.partition)
                    if args.command in {'bootstrap', 'handoff'}:
                        version = register(ws, result['run_id'])
                        approve(ws, version, 'Finite guarded validation RMSE <= 5; inspect contract tests separately')
                        event = activate(ws, version, 'Local baseline demonstration')
                        _, inference = batch_predict(ws)
                        result = {'training': result, 'version': version, 'audit': event, 'inference': inference}
        print(json.dumps(result, indent=2))
    except (ValueError, FileNotFoundError, KeyError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    main()
