"""Validate synchronization contracts, not instructional quality by word count."""
from pathlib import Path
import ast
import json
import re
from urllib.parse import unquote, urlparse
import nbformat

MODULE=Path(__file__).resolve().parents[1]
REPO=MODULE.parent
GITHUB='https://github.com/richhiey/ml-llm-ops/blob/main/'
COLAB='https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/'


def verify():
    rows=json.loads((MODULE/'maintainer/learning-path.json').read_text())
    assert len(rows)==26 and len({r['id'] for r in rows})==26
    errors=[];observations=[]
    for row in rows:
        lesson=MODULE/row['public_path'];body=lesson.read_text()
        assert row['outcome'] in body,(row['id'],'exact outcome missing')
        assert body.rsplit('## ',1)[-1].startswith('Summary\n')
        assert not re.search(r'TODO|\[VISUAL:|SCREENSHOT SUGGESTION',body)
        nb=nbformat.read(MODULE/'notebooks'/row['notebook'],as_version=4)
        anchors={c.metadata.get('id',c.id) for c in nb.cells}
        assert row['notebook_anchor'] in anchors,(row['id'],'missing notebook section')
        expected=COLAB+'module-a/notebooks/'+row['notebook']+'#scrollTo='+row['notebook_anchor']
        assert expected in body,(row['id'],'notebook link differs from manifest')
        observations.append({'id':row['id'],'type':row['type'],'words':len(body.split()),'exact_outcome':True,'notebook_section':row['notebook_anchor']})
    md_files=[*MODULE.glob('lessons/**/*.md'),*MODULE.glob('docs/*.md'),*MODULE.glob('maintainer/*.md'),MODULE/'README.md',REPO/'README.md',MODULE/'notebooks/README.md']
    for file in md_files:
        for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            parsed=urlparse(target)
            if target.startswith(GITHUB):path=REPO/unquote(parsed.path.split('/blob/main/',1)[1])
            elif target.startswith(COLAB):path=REPO/unquote(parsed.path.split('/blob/main/',1)[1])
            elif parsed.scheme or target.startswith('#'):continue
            else:path=file.parent/unquote(parsed.path)
            if not path.exists():errors.append({'file':str(file.relative_to(REPO)),'missing':target})
    notebook_files=sorted((MODULE/'notebooks').glob('*.ipynb'))
    assert len(notebook_files)==4 and len(set(row['notebook'] for row in rows))==4
    assert not any('00-learner-workspace' in file.read_text() for file in md_files)
    notebooks=[]
    for file in sorted((MODULE/'notebooks').glob('*.ipynb')):
        nb=nbformat.read(file,as_version=4);nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type=='code':ast.parse(cell.source)
        setup=[c for c in nb.cells if c.cell_type=='code' and 'setup' in c.metadata.get('tags',[])]
        assert len(setup)==1 and 'code_revision()' in setup[0].source
        pin=json.loads((MODULE/'maintainer/helper-pin.json').read_text())
        assert pin['source_commit'] in setup[0].source
        cells=[c for c in nb.cells if c.cell_type=='code']
        assert all(c.execution_count is not None for c in cells)
        assert not any(o.output_type=='error' for c in cells for o in c.outputs)
        notebooks.append({'name':file.name,'executed_code_cells':len(cells),'errors':0})
    assert not errors,errors
    return {'passed':True,'lessons':observations,'notebooks':notebooks,'markdown_files_checked':len(md_files),'broken_resource_links':errors,'quality_gate':'Source/route/execution synchronization only; lesson-specific instructional review is separate.'}


if __name__=='__main__':
    result=verify()
    (MODULE/'maintainer/learning-path-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='lessons'},indent=2))
