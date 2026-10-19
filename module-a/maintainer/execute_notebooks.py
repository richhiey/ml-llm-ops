"""Execute each notebook in a new kernel using the selected helper interpreter."""
from pathlib import Path
import json, sys, tempfile, os
import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
root=Path(__file__).resolve().parents[1]/'notebooks'
with tempfile.TemporaryDirectory(prefix='campus-kernel-') as kernel_dir:
    folder=Path(kernel_dir)/'campus-helper'; folder.mkdir()
    (folder/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Campus helper','language':'python'}))
    km=KernelSpecManager(kernel_dirs=[kernel_dir])
    reports=[]
    for path in sorted(root.glob('*.ipynb')):
        nb=nbformat.read(path,as_version=4)
        client=NotebookClient(nb,timeout=180,kernel_name='campus-helper',resources={'metadata':{'path':str(root)}})
        client.kernel_manager_class  # selected kernel uses this interpreter
        from jupyter_client import AsyncKernelManager
        client.km=AsyncKernelManager(kernel_name='campus-helper',kernel_spec_manager=km)
        client.execute()
        nbformat.write(nb,path)
        reports.append({'notebook':path.name,'executed_code_cells':sum(c.cell_type=='code' for c in nb.cells),'errors':0})
        print(path.name,'PASS',flush=True)
    Path(os.environ.get('CAMPUS_NOTEBOOK_REPORT', str(root/'execution-report.json'))).write_text(json.dumps(reports,indent=2)+'\n')
