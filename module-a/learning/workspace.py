"""Run learner project edits in new processes, separate from notebook imports."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]


def _execute(arguments, project, expected_returncode=0):
    project = Path(project).resolve()
    if not (project / 'pyproject.toml').is_file():
        raise ValueError('Choose the project folder containing pyproject.toml')
    environment = os.environ.copy()
    environment['PYTHONPATH'] = str(project / 'src')
    result = subprocess.run(arguments, cwd=project, env=environment,
                            text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != expected_returncode:
        raise RuntimeError(f'Expected exit {expected_returncode}; got {result.returncode}.\n{result.stderr}')
    return result


def course_cli(*arguments, project=PACKAGE, expected_returncode=0):
    """Run a noninteractive campus-mlops CLI command; stdout retains its JSON."""
    if arguments and arguments[0] == 'ui':
        raise ValueError('Start the MLflow UI in a local terminal, not a notebook subprocess')
    return _execute([sys.executable, '-m', 'campus_mlops.cli', *map(str, arguments)],
                    project, expected_returncode)


def project_python(project, code, expected_returncode=0):
    """Run Python against this project's src in a fresh process using current dependencies."""
    return _execute([sys.executable, '-c', code], project, expected_returncode)


def project_tests(project, *pytest_arguments, expected_returncode=0):
    """Run project tests with current interpreter; install pytest before use."""
    return _execute([sys.executable, '-m', 'pytest', *pytest_arguments],
                    project, expected_returncode)


def make_project(name='stage-project'):
    """Create the intentionally incomplete stage project, never overwrite learner work."""
    if not name or Path(name).name != name or name in {'.', '..'}:
        raise ValueError('Use a simple project folder name')
    destination = Path(tempfile.mkdtemp(prefix='linden-project-')) / name
    _execute([sys.executable, str(PACKAGE/'exercises/make-stage-lab.py'),
              '--destination', str(destination)], PACKAGE)
    return destination


def prepare_case(case, state, project=PACKAGE):
    """Prepare an unsolved comparison, past-run or incident state."""
    return _execute([sys.executable, str(PACKAGE/'exercises/prepare-practice.py'),
                     case, '--state', str(Path(state).resolve())], project)
