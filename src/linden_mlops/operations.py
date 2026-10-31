"""Bounded local monitoring and response. Signals never change an alias.

Numeric policies produce observations; only an explicit approved action changes service.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import math
import mlflow.sklearn
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

from .pipeline import Config, FEATURES, TARGET, ingest, preprocess, evaluate, sha256
from .lifecycle import MODEL_NAME, Workspace, register, approve, activate, write_json, code_revision


@dataclass(frozen=True)
class Policy:
    min_rows: int = 96
    min_labels: int = 32
    temperature_c: float = 3.0
    hour: float = 3.0
    occupancy: float = 8.0
    prediction_kwh: float = 5.0
    max_rmse_kwh: float = 3.0
    min_improvement_kwh: float = 0.5

    def __post_init__(self):
        for key, value in asdict(self).items():
            if isinstance(value, bool) or not math.isfinite(value) or value <= 0:
                raise ValueError(f'Policy {key} must be finite and positive')
        if any(not isinstance(v, int) for v in [self.min_rows, self.min_labels]):
            raise ValueError('Minimum cohort sizes must be integers')


def read_policy(path):
    return Policy(**json.loads(Path(path).read_text()))


def _now():
    return datetime.now(timezone.utc).isoformat()




def _inputs(path):
    frame = pd.read_csv(path)
    if list(frame.columns) != ['row_id', *FEATURES] or frame.row_id.isna().any() or frame.row_id.duplicated().any():
        raise ValueError('Monitoring inputs need unique complete row_id and exactly the three features')
    preprocess(frame, Config(range_guard=True))
    return frame


def _model(workspace, version):
    workspace.connect()
    return mlflow.sklearn.load_model(f'models:/{MODEL_NAME}/{version}')


def _validation(path):
    frame = ingest(path)
    return frame.loc[frame.partition == 'validation'].copy()


def monitor(workspace, reference_path, current_path, policy_path, destination, feedback_path=None):
    """Pin one active version for both distributions; labels are a separate observation."""
    destination = Path(destination)
    if destination.exists():
        raise ValueError('Monitoring report must not exist; retain each observation')
    policy = read_policy(policy_path)
    reference, current = _inputs(reference_path), _inputs(current_path)
    if set(reference.row_id) & set(current.row_id):
        raise ValueError('Reference and current monitoring IDs must be disjoint')
    mv = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')
    model = _model(workspace, mv.version)
    distances = {column: float(wasserstein_distance(reference[column], current[column])) for column in FEATURES}
    distances['prediction_kwh'] = float(wasserstein_distance(model.predict(reference[FEATURES]), model.predict(current[FEATURES])))
    flags = {key: value >= getattr(policy, key) for key, value in distances.items()}
    enough = min(len(reference), len(current)) >= policy.min_rows
    score, labels = None, 0
    if feedback_path:
        labeled = _validation(feedback_path)
        if set(labeled.row_id) & (set(reference.row_id) | set(current.row_id)):
            raise ValueError('Independent labeled evaluation IDs must not overlap monitoring IDs')
        labels = len(labeled)
        score = evaluate(model, preprocess(labeled, Config(range_guard=True)), labeled[TARGET])['rmse_kwh']
    if not enough:
        action = 'collect_more'
    elif labels >= policy.min_labels and score > policy.max_rmse_kwh:
        action = 'retrain_candidate'
    elif any(flags.values()):
        action = 'investigate'
    else:
        action = 'continue_monitoring'
    result = {'schema_version': 1, 'observed_at': _now(), 'code_revision': code_revision(),
        'model_version': str(mv.version), 'run_id': mv.run_id, 'policy': asdict(policy),
        'reference_sha256': sha256(reference_path), 'current_sha256': sha256(current_path),
        'feedback_sha256': sha256(feedback_path) if feedback_path else None,
        'rows': {'reference': len(reference), 'current': len(current), 'labeled_validation': labels},
        'distances': distances, 'threshold_exceeded': flags, 'sufficient_window': enough,
        'validation_rmse_kwh': score, 'action': action}
    destination.parent.mkdir(parents=True, exist_ok=True)
    write_json(destination, result)
    workspace.client.log_dict(mv.run_id, result, f'operations/monitor/{sha256(destination)}.json')
    return result


def _response_inputs(workspace, report_path, feedback_path):
    report = json.loads(Path(report_path).read_text())
    # Evidence is checked against its retained MLflow observation, not a local action edit.
    from mlflow.exceptions import MlflowException
    try:
        retained = Path(workspace.client.download_artifacts(report['run_id'], f'operations/monitor/{sha256(report_path)}.json'))
    except MlflowException as error:
        raise ValueError('Observed trigger was changed or is missing from MLflow') from error
    if json.loads(retained.read_text()) != report:
        raise ValueError('Observed trigger differs from retained MLflow evidence')
    policy = Policy(**report['policy'])
    if report['action'] != 'retrain_candidate' or report['code_revision'] != code_revision():
        raise ValueError('Response needs an observed retraining trigger from the current source')
    if report['feedback_sha256'] != sha256(feedback_path):
        raise ValueError('Feedback differs from the observed trigger')
    active = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')
    if str(active.version) != report['model_version'] or active.run_id != report['run_id']:
        raise ValueError('Active version changed; re-evaluate the current situation')
    return report, policy


def train_candidate(workspace, report_path, feedback_path, alpha=1.0):
    report, _ = _response_inputs(workspace, report_path, feedback_path)
    result = workspace.run(Config(alpha=alpha, range_guard=True, autolog=True), name='feedback-candidate', data_path=feedback_path)
    workspace.client.set_tag(result['run_id'], 'trigger_report_sha256', sha256(report_path))
    version = register(workspace, result['run_id'])
    return {'run_id': result['run_id'], 'version': version, 'incumbent_version': report['model_version']}


def compare_candidate(workspace, report_path, feedback_path, version, destination):
    report, policy = _response_inputs(workspace, report_path, feedback_path)
    if Path(destination).exists():
        raise ValueError('Comparison must not overwrite earlier evidence')
    mv = workspace.client.get_model_version(MODEL_NAME, str(version))
    run = workspace.client.get_run(mv.run_id)
    if (run.data.params['data_sha256'] != sha256(feedback_path)
            or run.data.params['evaluation_partition'] != 'validation'
            or run.data.tags.get('trigger_report_sha256') != sha256(report_path)):
        raise ValueError('Candidate must use this trigger and feedback snapshot')
    frame = _validation(feedback_path)
    x = preprocess(frame, Config(range_guard=True))
    incumbent = evaluate(_model(workspace, report['model_version']), x, frame[TARGET])['rmse_kwh']
    candidate = evaluate(_model(workspace, version), x, frame[TARGET])['rmse_kwh']
    improvement = incumbent - candidate
    result = {'observed_at': _now(), 'monitor_report': str(Path(report_path).resolve()),
        'monitor_sha256': sha256(report_path), 'feedback_path': str(Path(feedback_path).resolve()),
        'feedback_sha256': sha256(feedback_path), 'evaluation_rows': frame.row_id.tolist(),
        'incumbent_version': report['model_version'], 'candidate_version': str(version), 'candidate_run_id': mv.run_id,
        'incumbent_rmse_kwh': incumbent, 'candidate_rmse_kwh': candidate, 'improvement_kwh': improvement,
        'policy': asdict(policy), 'passed': candidate <= policy.max_rmse_kwh and improvement >= policy.min_improvement_kwh}
    write_json(destination, result)
    workspace.client.log_dict(mv.run_id, result, f'operations/{Path(destination).name}')
    return result


def promote_candidate(workspace, comparison_path, reason):
    if not reason.strip():
        raise ValueError('Explain the promotion decision')
    comparison = json.loads(Path(comparison_path).read_text())
    if sha256(comparison['monitor_report']) != comparison['monitor_sha256']:
        raise ValueError('Observed trigger changed')
    # Re-read raw models, labels, policy and active state; edited passed=true is not permission.
    import tempfile
    with tempfile.TemporaryDirectory() as temporary:
        fresh = compare_candidate(workspace, comparison['monitor_report'], comparison['feedback_path'],
                                  comparison['candidate_version'], Path(temporary) / 'verification.json')
    if not fresh['passed']:
        raise ValueError('Candidate fails response acceptance; retain the incumbent')
    approve(workspace, fresh['candidate_version'], reason)
    return activate(workspace, fresh['candidate_version'], reason)


def write_incident(workspace, report_path, comparison_path, destination, explanation, follow_up, batch_name='response-batch'):
    """Package actual observations plus operator reasoning; no correctness claim for prose."""
    if not explanation.strip() or not follow_up.strip():
        raise ValueError('Incident needs your decision explanation and an owned follow-up')
    if Path(destination).exists():
        raise ValueError('Incident destination must not exist')
    report = json.loads(Path(report_path).read_text())
    comparison = json.loads(Path(comparison_path).read_text())
    if comparison['monitor_sha256'] != sha256(report_path):
        raise ValueError('Incident comparison and trigger do not match')
    active = workspace.client.get_model_version_by_alias(MODEL_NAME, 'active')
    if str(active.version) not in {report['model_version'], comparison['candidate_version']}:
        raise ValueError('Incident must explain the observed incumbent or candidate selection')
    if str(active.version) == comparison['candidate_version'] and not comparison['passed']:
        raise ValueError('Failed candidate is active; contain or recover before closing')
    batch = json.loads((workspace.path / f'{batch_name}.json').read_text())
    rows = pd.read_csv(workspace.path / f'{batch_name}.csv')
    if (batch['resolved_version'] != str(active.version) or batch['run_id'] != active.run_id
            or batch.get('completed_at', '') < comparison['observed_at']
            or not batch['complete_within_60s'] or len(rows) != 24
            or rows.row_id.duplicated().any() or not np.isfinite(rows.prediction_kwh).all()):
        raise ValueError('Incident needs a fresh valid batch from the resulting active version')
    closed_at = _now()
    events = [json.loads(line) for line in (workspace.path / 'audit.jsonl').read_text().splitlines()]
    events = [event for event in events if report['observed_at'] <= event['timestamp_utc'] <= closed_at]
    rolled_back = (str(active.version) == report['model_version'] and any(
        str(event['previous_version']) == comparison['candidate_version']
        and str(event['new_version']) == report['model_version'] for event in events))
    timeline = [{'time': report['observed_at'], 'event': 'labeled trigger observed'},
                {'time': comparison['observed_at'], 'event': 'candidate comparison recorded'},
                *[{'time': event['timestamp_utc'], 'event': 'alias reassigned', 'evidence': event} for event in events],
                {'time': batch['completed_at'], 'event': 'resulting version served a fresh batch'},
                {'time': closed_at, 'event': 'incident record written'}]
    result = {'trigger': report, 'comparison': comparison, 'closed_at': closed_at,
        'timeline': sorted(timeline, key=lambda item: item['time']), 'alias_events': events,
        'affected_version': report['model_version'], 'resulting_version': str(active.version),
        'action': 'rolled_back' if rolled_back else 'promoted' if str(active.version) == comparison['candidate_version'] else 'retained_incumbent',
        'explanation': explanation, 'follow_up': follow_up, 'verification': batch,
        'evidence_sha256': {'monitor': sha256(report_path), 'comparison': sha256(comparison_path),
                            'batch': sha256(workspace.path / f'{batch_name}.csv')}}
    write_json(destination, result)
    return result


def plot_monitoring(report):
    """Actual distances divided by their own declared thresholds; dimensionless ratio."""
    from .visuals import _figure, _style, GREEN, FOREST
    figure = _figure('A changed distribution is a signal to investigate',
        'One pinned model; distance / declared threshold. A ratio of 1 reaches the declared alert boundary.')
    ax = figure.subplots()
    keys = list(report['distances'])
    ratios = [report['distances'][key] / report['policy'][key] for key in keys]
    ax.bar(keys, ratios, color=GREEN)
    ax.axhline(1, color=FOREST, linestyle='--', label='Declared boundary')
    ax.set_ylabel('Distance / threshold (dimensionless)'); ax.legend(); _style(ax)
    figure.linden_data = {'distances': report['distances'], 'ratios': dict(zip(keys, ratios)), 'policy': report['policy']}
    return figure


def plot_candidate(comparison):
    """Two observed errors on one evaluation cohort; no holdout values or model search."""
    from .visuals import _figure, _style, GREEN, FOREST
    figure = _figure('Compare two models on the same labeled rows',
        'Independent feedback validation; lower RMSE is better. This synthetic cohort does not establish production quality.')
    ax = figure.subplots()
    values = [comparison['incumbent_rmse_kwh'], comparison['candidate_rmse_kwh']]
    ax.bar(['Incumbent', 'Candidate'], values, color=[FOREST, GREEN])
    ax.axhline(comparison['policy']['max_rmse_kwh'],color=FOREST,linestyle='--',label='Declared maximum error')
    ax.set_ylabel('Validation RMSE (kWh)'); ax.legend(); _style(ax)
    for index,value in enumerate(values): ax.text(index,value+.15,f'{value:.2f}',ha='center',color=FOREST)
    figure.linden_data = {'rmse_kwh': values, 'evaluation_rows': comparison['evaluation_rows'], 'policy': comparison['policy']}
    return figure
