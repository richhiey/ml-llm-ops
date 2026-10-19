"""Prepare observable starting states without doing the learner's target operation."""
from pathlib import Path
import argparse,json
from campus_mlops import Workspace,Config,run_matrix,export_runs,register,approve,activate
parser=argparse.ArgumentParser();parser.add_argument('case',choices=['matrix','rollback','registry-assessment','past-run']);parser.add_argument('--state',required=True);args=parser.parse_args()
path=Path(args.state).resolve()
if path.exists():raise SystemExit('Use a new state path; existing evidence is preserved')
ws=Workspace(path);index={'case':args.case,'state':str(path)}
if args.case=='matrix':
 records=run_matrix(ws,autolog=True);ids=[r['run_id'] for r in records]
 (path/'matrix-run-ids.json').write_text(json.dumps(ids,indent=2)+'\n')
 rows=export_runs(ws);rows[rows.run_id.isin(ids)].to_csv(path/'runs.csv',index=False);index['run_ids']=ids
else:
 alphas=[1,10] if args.case=='rollback' else [.1,10,100] if args.case=='registry-assessment' else [1]
 versions=[]
 for i,a in enumerate(alphas):
  record=ws.run(Config(alpha=a,range_guard=True,autolog=True),name=f'intake-{i+1}')
  version=register(ws,record['run_id']);versions.append(version)
  if a!=100:
   approve(ws,version,'Contract tests and original finite validation RMSE<=5 gate; inspect raw evidence')
   activate(ws,version,'Initial client selection' if i==0 else 'Client trial before revised acceptance')
 index['registered_versions']=versions
 if args.case=='registry-assessment':index['incident']='Client now requires validation RMSE<=1.45 kWh; retain all versions and restore a suitable previously approved version.'
 elif args.case=='rollback':index['incident']='Client now requires validation RMSE<=1.6 kWh; inspect the current trial and the earlier approved version.'
 else:index['past_run_id']=record['run_id']
(path/'case.json').write_text(json.dumps(index,indent=2)+'\n');print(json.dumps(index,indent=2))
