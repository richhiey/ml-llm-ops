"""Authoring utility; notebooks only call the public helper API."""
from pathlib import Path
import json, subprocess, argparse
import nbformat as n
from campus_mlops import __version__
from campus_mlops.lifecycle import code_revision
M=Path(__file__).resolve().parents[1]; N=M/'notebooks'
parser=argparse.ArgumentParser(); parser.add_argument('--source-commit', default='HEAD'); args=parser.parse_args()
source_commit=subprocess.check_output(['git','rev-parse',args.source_commit],cwd=M,text=True).strip()
subprocess.run(['git','diff','--exit-code',source_commit,'--','module-a/src','module-a/pyproject.toml','module-a/uv.lock'],cwd=M.parent,check=True)
pin={'package':'campus-mlops','version':__version__,'code_revision':code_revision(),
     'repository':'https://github.com/richhiey/ml-llm-ops.git',
     'source_commit':source_commit,'package_path':'module-a'}
(N/'helper-pin.json').write_text(json.dumps(pin,indent=2)+'\n')
setup='''from pathlib import Path
import json, tempfile, sys, subprocess
PIN = PIN_LITERAL
assert sys.version_info[:2] == (3, 12), 'Use Python 3.12; see the linked setup guide.'
if 'google.colab' in sys.modules:
    # Start before importing numerical packages: installed files cannot replace live modules.
    expected = {'numpy':'2.3.3', 'pandas':'2.3.3', 'sklearn':'1.7.2', 'mlflow':'3.5.1'}
    for name, version in expected.items():
        if name in sys.modules and getattr(sys.modules[name], '__version__', None) != version:
            raise RuntimeError(f'{name} is already loaded at another version. Delete/reconnect the runtime, then run setup first.')
    checkout = Path('/content') / ('ml-llm-ops-' + PIN['source_commit'][:12])
    if not checkout.exists():
        subprocess.run(['git', 'clone', '--no-checkout', PIN['repository'], str(checkout)], check=True)
    subprocess.run(['git', '-C', str(checkout), 'checkout', '--detach', PIN['source_commit']], check=True)
    actual = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'], text=True).strip()
    assert actual == PIN['source_commit']
    package = checkout / PIN['package_path']
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', str(package/'requirements-colab.txt')], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--no-deps', '-e', str(package)], check=True)
    # A running kernel does not reload newly installed editable .pth files.
    sys.path.insert(0, str(package / 'src'))
import campus_mlops
from campus_mlops import *
from campus_mlops.lifecycle import code_revision, MODEL_NAME
assert campus_mlops.__version__ == PIN['version'] == '0.1.1'
assert code_revision() == PIN['code_revision'], 'Helper changed: restore the pinned reference source.'
state = Path(tempfile.mkdtemp(prefix='campus-module-a-'))
print('Helper', campus_mlops.__version__, 'source commit:', PIN['source_commit'], 'state:', state)
'''.replace('PIN_LITERAL', repr(pin))

def save(name,title,intro,parts):
 nb=n.v4.new_notebook(); nb.cells=[n.v4.new_markdown_cell('# '+title+'\n\n'+intro+'\n\nRun all cells top to bottom. **Colab:** connect a fresh CPU / Python 3.12 runtime; the first cell clones the pinned GitHub source and installs its locked runtime dependencies. **Local:** run `uv sync --locked` from `module-a` and select that `.venv` interpreter. See [Colab and environment guidance](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/colab.md). Every run creates a new temporary tracking directory and prints its path; download evidence before ending a hosted runtime. No API key is needed. These are complete worked references; independent practices have separate starting states. IDs and timing vary.'),n.v4.new_code_cell(setup)]
 for text,code in parts:
  nb.cells.extend([n.v4.new_markdown_cell(text),n.v4.new_code_cell(code)])
 nb.metadata.colab={'name':name,'provenance':[]}; nb.metadata.kernelspec={'display_name':'Campus helper Python 3.12','language':'python','name':'python3'}
 n.write(nb,N/name)
save('01-pipeline-and-extension.ipynb','Trace and validate the pipeline','Linden Facilities needs 24 hourly estimates. Follow the five stage contracts before making a bounded validation change.',[
('## Inspect the stage boundaries\n`ingest` reads the fixed snapshot. Features exclude target and partition. Expect 168 train, 48 validation and 24 final rows.',"frame=ingest()\nprint(frame.groupby('partition').size())\ndisplay(frame.head())"),
('## Trace preparation, fitting and evaluation\nThe scaler belongs to the fitted model, so it sees training rows only. RMSE measures larger errors more strongly; MAE is diagnostic. Expect baseline validation RMSE about 1.443003925 kWh.',"from campus_mlops.pipeline import TARGET\nconfig=Config()\nfeatures=preprocess(frame,config)\ntrain_rows=frame.partition=='train'\nvalid_rows=frame.partition=='validation'\nmodel=train(features.loc[train_rows],frame.loc[train_rows,TARGET],config)\nmetrics=evaluate(model,features.loc[valid_rows],frame.loc[valid_rows,TARGET])\nprint(features.columns.tolist(), metrics)\nassert abs(metrics['rmse_kwh']-1.4430039250255964)<1e-6"),
('## Read the extension, then test both branches\nThis is the worked reference. Explain every line before using it. It rejects invalid values and copies valid inputs. Enabling it must preserve valid outputs.',"import inspect\nprint(inspect.getsource(validate_ranges))\nimport pandas as pd\npd.testing.assert_frame_equal(validate_ranges(frame),frame)\nbroken=frame.copy(); broken.loc[0,'hour']=24\ntry:\n    validate_ranges(broken)\nexcept ValueError as error:\n    print('Expected rejection:', error)\nelse:\n    raise AssertionError('Invalid hour was accepted')\nassert run_pipeline(Config(range_guard=True))[1]==metrics"),
('## Complete the inference stage\nThe prepared bootstrap uses the same pipeline, logs it, registers and activates an approved model. Expect 24 finite output rows tied to the resolved registry version. Timing is observed, not a fixed benchmark.',"ws=Workspace(state/'tracking')\nrecord=ws.run(Config(range_guard=True),name='guarded-baseline')\nversion=register(ws,record['run_id'])\napprove(ws,version,'Valid/rejected input checks and RMSE <= 5')\nactivate(ws,version,'Baseline for batch demonstration')\npredictions,evidence=batch_predict(ws)\ndisplay(predictions.head()); print(evidence)\nassert len(predictions)==24 and evidence['resolved_version']==version\nassert evidence['complete_within_60s']")])
save('02-tracking-and-evidence.ipynb','Compare controlled runs and check recommendations','Linden needs a defensible choice rather than five unrelated scores. The fixture holds data, split, scaling, solver and guard fixed while changing alpha.',[
('## Run the declared matrix\nAutologging hooks model fitting. We disable automatic model logging inside the helper so the explicit named model remains unambiguous. The helper still logs the primary held-out metric itself.',"ws=Workspace(state/'tracking')\nrecords=run_matrix(ws,autolog=True)\nselected_ids=[record['run_id'] for record in records]\n(ws.path/'matrix-run-ids.json').write_text(json.dumps(selected_ids,indent=2))\nall_rows=export_runs(ws)\nrows=all_rows[all_rows.run_id.isin(selected_ids)].copy()\nrows.to_csv(ws.path/'runs.csv',index=False)\ndisplay(rows[['run_id','alpha','range_guard','evaluation_partition','rmse_kwh','mae_kwh']].sort_values('rmse_kwh'))\nassert len(rows)==5"),
('## Inspect raw MLflow evidence\nAuto-generated training metrics are useful diagnostics, not the declared decision metric. Inspect a raw run and artifact list instead of trusting a summary.',"best=rows.sort_values('rmse_kwh').iloc[0]\nraw=ws.client.get_run(best.run_id)\nprint('alpha:',best.alpha,'validation RMSE:',best.rmse_kwh)\nprint('Autolog parameter:',raw.data.params['ridge__alpha'])\nprint('Training metric:',raw.data.metrics['training_mean_squared_error'])\nprint([a.path for a in ws.client.list_artifacts(best.run_id,'reproduction')])\nassert float(best.alpha)==0.01"),
('## Validate an assistant recommendation\nExport `runs.csv` to your institution-approved assistant only if its data policy permits. Ask it to name run IDs, metric direction, controls and caveats. Paste the actual response into your evidence sheet. The following intentionally wrong recommendation is a deterministic test case, not a claimed live assistant call.',"wrong=rows.sort_values('rmse_kwh').iloc[-1]\nprint(verify_summary(rows,wrong.run_id))\nprint(verify_summary(rows,best.run_id))\nassert not verify_summary(rows,wrong.run_id)['recommendation_matches_metric']\nassert verify_summary(rows,best.run_id)['recommendation_matches_metric']"),
('## Prepare a UI comparison\nFor this UI task, use the local setup: run the printed command in a module-a terminal and open localhost:5050. In hosted Colab, prepare a local matrix instead; a hosted localhost address is not a browser connection. In `linden-demand`, select the five rows, compare parameters and validation metrics, and sort RMSE ascending. Confirm the displayed run ID matches the raw export. API evidence does not substitute for doing this UI task.',"print('campus-mlops ui --state',ws.path)\nprint('Best source run:',best.run_id)\nprint('Raw CSV:',ws.path/'runs.csv')")])
save('03-registry-and-reproduction.ipynb','Promote, roll back and reproduce','Linden must separate a model artifact from the version currently used by the next batch job. This worked reference demonstrates aliases, validation tags and explicit application audit events.',[
('## Register and approve a baseline\nA new version begins pending. Approval checks guard and the 5-kWh teaching gate. Tags describe evidence; active is a mutable name pointing to a version.',"ws=Workspace(state/'tracking')\napproved=ws.run(Config(alpha=1,range_guard=True),name='approved')\nv1=register(ws,approved['run_id'])\napprove(ws,v1,'Guard contracts and baseline validation RMSE checked')\nprint(activate(ws,v1,'Initial approved version'))\nprint(ws.client.get_model_version(MODEL_NAME,v1))"),
('## Exercise a rollback scenario\nA trial passes the original 5-kWh gate. A new acceptance brief tightens validation RMSE to 1.6 kWh; the alpha=10 trial fails it while the original alpha=1 passes. Record this reason and roll back the alias without deleting either model.',"trial=ws.run(Config(alpha=10,range_guard=True),name='trial')\nv2=register(ws,trial['run_id'])\napprove(ws,v2,'Passed original 5-kWh teaching gate')\nactivate(ws,v2,'Trial before stricter acceptance review')\nassert trial['metrics']['rmse_kwh']>1.6 and approved['metrics']['rmse_kwh']<1.6\nws.client.set_model_version_tag(MODEL_NAME,v2,'incident','Fails revised 1.6-kWh gate')\nevent=activate(ws,v1,'Rollback: trial fails revised 1.6-kWh acceptance')\nprint(event)\nassert event['previous_version']==v2 and event['new_version']==v1"),
('## Verify the next inference job\nA rollback is only useful if inference uses it. The helper resolves the alias once and pins its version for this batch.',"output,inference=batch_predict(ws)\nprint(inference)\nprint((ws.path/'audit.jsonl').read_text())\nassert inference['resolved_version']==v1\nassert ws.client.get_model_version(MODEL_NAME,v1).run_id==approved['run_id']"),
('## Reproduce the approved run\nThis checks source, data, config and environment before comparing RMSE. A new store is sufficient for a state replay; the clean-environment procedure additionally restores a source archive and a new venv.',"report=reproduce(ws,approved['run_id'],state/'reproduced')\nprint(report)\nassert report['passed'] and report['rmse_delta']<=1e-6\nmanifest=json.loads((ws.path/'evidence'/approved['run_id']/'manifest.json').read_text())\nprint({k:manifest[k] for k in ['run_id','code_revision','data_sha256','config','model_uri']})\nprint('Recorded installed distributions:',len(manifest['environment']['packages']))")])
save('04-cumulative-handoff.ipynb','Prove the cumulative handoff','Use the selected alpha, validated stage and active batch path together. The reference alpha=0.01 is selected from the fixed validation matrix; it is not a universal hyperparameter recommendation.',[
('## Integrate an end-to-end run\nBuild from a new state with guard, explicit metrics, autologging and registry evidence. No orchestration framework is needed for this sequence.',"ws=Workspace(state/'handoff')\nrecord=ws.run(Config(alpha=0.01,range_guard=True,autolog=True),name='handoff')\nversion=register(ws,record['run_id'])\napprove(ws,version,'Controlled alpha comparison and range guard checks')\nprint(activate(ws,version,'Final validated selection'))\noutput,inference=batch_predict(ws)\nprint(record); print(inference)\nassert inference['rows']==24 and inference['complete_within_60s']"),
('## Reproduce before handoff\nThe recorded source/data/environment must match. Replaying to a new store tests absence of hidden registry and notebook dependencies.',"report=reproduce(ws,record['run_id'],state/'fresh-reproduction')\nprint(report)\nassert report['passed'] and report['lineage_matched']"),
('## Evaluate the reserved final holdout once\nAfter selection, measure final rows without tuning against their result. Keep this run out of the validation comparison group.',"final=ws.run(Config(alpha=0.01,range_guard=True,autolog=True),name='final-holdout',partition='final')\nprint(final['metrics'])\nassert final['evaluation_partition']=='final'"),
('## Write a verifiable handoff index\nThe complete submission also includes your explained extension diff and setup instructions. Check each named file exists; an index is a locator, not proof by itself.',"handoff={'version':version,'run_id':record['run_id'],'code_revision':record['code_revision'],\n'data_sha256':record['data_sha256'],'config':record['config'],'environment':record['environment'],\n'model_uri':record['model_uri'],'inference':inference,'reproduction':report,\n'exact_training_command':record['command'],'tolerance_rmse_kwh':1e-6}\n(state/'handoff.json').write_text(json.dumps(handoff,indent=2))\nprint(json.dumps(handoff,indent=2))\nassert (ws.path/'batch.csv').exists() and (ws.path/'audit.jsonl').exists()")])

# Keep learning routes and the unsolved start synchronized with the Campus manifest.
from enrich_notebooks import enrich
enrich(M,pin,setup)
