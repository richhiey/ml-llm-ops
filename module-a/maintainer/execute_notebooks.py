"""Execute each notebook in a new kernel using the selected helper interpreter."""
from pathlib import Path
import argparse, json, sys, tempfile, os
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
root=Path(__file__).resolve().parents[1]/'notebooks'
parser=argparse.ArgumentParser()
parser.add_argument('--sprint',type=int,choices=range(1,5))
args=parser.parse_args()
with tempfile.TemporaryDirectory(prefix='campus-kernel-') as kernel_dir:
    folder=Path(kernel_dir)/'campus-helper'; folder.mkdir()
    (folder/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Campus helper','language':'python'}))
    km=KernelSpecManager(kernel_dirs=[kernel_dir])
    reports=[]
    for path in sorted(root.glob('*.ipynb')):
        if args.sprint and not path.name.startswith(f'{args.sprint:02}-'):continue
        nb=nbformat.read(path,as_version=4)
        client=NotebookClient(nb,timeout=180,kernel_name='campus-helper',resources={'metadata':{'path':str(root)}})
        client.kernel_manager_class  # selected kernel uses this interpreter
        from jupyter_client import AsyncKernelManager
        client.km=AsyncKernelManager(kernel_name='campus-helper',kernel_spec_manager=km)
        client.execute()
        nbformat.write(nb,path)
        templates=sum(c.cell_type=='code' and 'student-work' in c.metadata.get('tags',[]) for c in nb.cells)
        count=sum(c.cell_type=='code' for c in nb.cells)
        reports.append({'notebook':path.name,'executed_code_cells':count,
                        'guided_code_cells':count-templates,'student_work_templates':templates,'errors':0})
        print(path.name,'PASS',flush=True)
    Path(os.environ.get('CAMPUS_NOTEBOOK_REPORT', str(root/'execution-report.json'))).write_text(json.dumps(reports,indent=2)+'\n')
