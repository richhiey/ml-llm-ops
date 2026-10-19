"""Create an editable teaching copy with one intentionally incomplete validation stage."""
from pathlib import Path
import argparse,difflib,json,shutil
parser=argparse.ArgumentParser();parser.add_argument('--destination',default='../project-helper');args=parser.parse_args()
source=Path(__file__).resolve().parents[1];target=Path(args.destination).resolve()
if target.exists():raise SystemExit('Destination already exists; choose a new directory to preserve your work')
target.mkdir(parents=True)
for file in source.rglob('*'):
 relative=file.relative_to(source)
 if file.is_file() and (relative.parts[0] in {'docs','examples','tests','src','exercises'} or str(relative) in {'.gitignore','.gitattributes','README.md','pyproject.toml','uv.lock'}):
  if '__pycache__' in relative.parts:continue
  copied=target/relative;copied.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,copied)
p=target/'src/campus_mlops/pipeline.py';solved=p.read_text();start=solved.index('def validate_ranges(');end=solved.index('\n\ndef preprocess(',start)
starter=solved[:start]+'''def validate_ranges(frame):
    """Starting stage: finite features only; domain ranges are not implemented yet."""
    return validate_features(frame).copy(deep=True)
'''+solved[end:];p.write_text(starter)
(target/'starter-pipeline.py').write_text(starter)
patch=''.join(difflib.unified_diff(starter.splitlines(True),solved.splitlines(True),fromfile='a/src/campus_mlops/pipeline.py',tofile='b/src/campus_mlops/pipeline.py'))
(target/'expert-stage.patch').write_text(patch)
(target/'LAB.md').write_text('Start with the finite-only validate_ranges stage. Implement the declared inclusive ranges and integer-hour check. The expert-stage.patch is an instructor/reference diff: inspect it after attempting the edit. Run the documented contract test before and after. This is a project copy; retain the published reference helper separately.\n')
print(json.dumps({'project_root':str(target),'starting_stage':'finite-only; range checks deliberately absent','reference_patch':str(target/'expert-stage.patch')},indent=2))
