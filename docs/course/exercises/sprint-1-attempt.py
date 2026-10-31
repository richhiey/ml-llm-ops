"""Copy to work/sprint-1/attempt.py. Write your own predictions before running probes.

Keep explanations and observed corrections in this file or one notes.md beside it.
Run from the clone root: uv run python work/sprint-1/attempt.py review (or supplier).
"""
import argparse
from pathlib import Path
import runpy

import pandas as pd
from linden_mlops.pipeline import validate_ranges


def review_candidate():
    proposed_guard = runpy.run_path('docs/course/exercises/generated-stage-candidate.py')['proposed_guard']
    # Explain each candidate line; predict accepted/rejected, values and object identity.
    # Make fresh inputs, retain one failing assertion, then contrast the correct guard.
    raise NotImplementedError('Write your candidate predictions and probes before opening feedback.')


def check_supplier():
    intake = pd.read_csv('docs/course/exercises/harbor-intake.csv')
    original = intake.copy(deep=True)
    # Classify each row and name its rule before execution. Test single rows and the full intake.
    # Check that original values/index survive, including the rejected complete call.
    # Also inventory harbor-plan-a/b/c.csv; probe your new validate_planned_batch stage,
    # then deliver an accepted complete plan through batch_predict with an explicit fitted model URI.
    raise NotImplementedError('Write your supplier decisions and probes before opening feedback.')


if __name__ == '__main__':
    if not Path('pyproject.toml').is_file():
        raise SystemExit('Run from the clone root containing pyproject.toml.')
    parser = argparse.ArgumentParser()
    parser.add_argument('activity', choices=['review', 'supplier'])
    args = parser.parse_args()
    {'review': review_candidate, 'supplier': check_supplier}[args.activity]()
