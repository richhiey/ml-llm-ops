"""Data and failure behavior behind the local teaching figures.

Experiment and identity fixtures below are test records, never published results.
"""
import numpy as np
import pandas as pd
import pytest

from linden_mlops.pipeline import ingest
from linden_mlops.visuals import (plot_contract, plot_experiments, plot_identity,
                                  plot_recovery, save_figure)


def experiment_records():
    return pd.DataFrame([{
        'run_id': f'test-{index}', 'alpha': str(alpha), 'rmse_kwh': score,
        'mae_kwh': score * .8, 'comparison_group': 'demand-v1-validation',
        'data_sha256': 'test-snapshot', 'code_revision': 'test-source',
        'range_guard': 'True', 'evaluation_partition': 'validation',
    } for index, (alpha, score) in enumerate(zip([.01, .1, 1, 10, 100], [1.5, 1.4, 1.6, 2, 3]))])


def recovery_inputs(delta=0.):
    planned = pd.DataFrame({'row_id': range(24)})
    predictions = pd.DataFrame({'row_id': range(24), 'prediction_kwh': np.linspace(5, 10, 24)})
    report = {'invariants': {'source': True, 'data': True, 'environment': True, 'config': True, 'partition': True},
              'absolute_rmse_delta': delta, 'tolerance': 1e-6,
              'reproduced_run_id': 'test-recovered-run', 'version': '3',
              'inference': {'elapsed_seconds': .2, 'rows': 24, 'complete_within_60s': True,
                            'run_id': 'test-recovered-run', 'resolved_version': '3'}, 'passed': True}
    return report, planned, predictions


def test_contract_counts_probes_and_closed_targets():
    # Omit targets entirely: plotting may read only partition and features.
    frame = ingest().drop(columns=['demand_kwh'])
    original = frame.copy(deep=True)
    fig = plot_contract(frame)
    assert fig.linden_data['partition_counts'] == {'train': 168, 'validation': 48, 'final': 24}
    assert [probe['accepted'] for probe in fig.linden_data['hour_probes']] == [False, True, False, True, False]
    assert [bar.get_height() for bar in fig.axes[0].patches] == [168, 48, 24]
    assert fig.axes[0].get_ylabel() == 'Rows (count)'
    assert 'hours' in fig.axes[1].get_xlabel()
    assert len(fig.axes[1].lines) == 0, 'Categorical probe outcomes must not be interpolated'
    assert sum(len(collection.get_offsets()) for collection in fig.axes[1].collections) == 5
    pd.testing.assert_frame_equal(frame, original)


def test_experiments_plot_only_validated_raw_values():
    records = experiment_records()
    fig = plot_experiments(records.sample(frac=1, random_state=2))
    assert fig.linden_data['winner_run_id'] == 'test-1'
    assert fig.linden_data['records'] == records[['run_id', 'alpha', 'rmse_kwh', 'mae_kwh']].assign(alpha=lambda r: r.alpha.astype(float)).to_dict('records')
    for ax, metric in zip(fig.axes, ['rmse_kwh', 'mae_kwh']):
        assert ax.get_xscale() == 'log'
        assert '(kWh)' in ax.get_ylabel()
        assert len(ax.lines) == 0, 'Five tested configurations do not define a continuous curve'
        plotted = np.concatenate([collection.get_offsets() for collection in ax.collections])
        expected = list(zip(records.alpha.astype(float), records[metric]))
        assert sorted(map(tuple, plotted)) == sorted(expected)
    with pytest.raises(ValueError, match='exactly'):
        plot_experiments(records.iloc[:4])
    with pytest.raises(ValueError, match='guarded validation'):
        plot_experiments(records.assign(evaluation_partition='final'))
    changed = records.copy()
    changed.loc[0, 'code_revision'] = 'other-test-source'
    with pytest.raises(ValueError, match='share data and code'):
        plot_experiments(changed)
    with pytest.raises(ValueError, match='MAE'):
        plot_experiments(records.assign(mae_kwh=np.nan))


def test_identity_uses_full_recorded_ids_and_rejects_mismatch():
    run_id = '0123456789abcdef0123456789abcdef'
    inference = {'run_id': run_id, 'resolved_version': '7', 'rows': 24, 'elapsed_seconds': .21}
    fig = plot_identity(run_id, '7', run_id, inference)
    assert fig.linden_data['chain_matches']
    visible = '\n'.join(item.get_text() for item in fig.axes[0].texts)
    assert visible.count('0123456789abcdef\n0123456789abcdef') == 3
    assert 'Version 7' in visible
    ax = fig.axes[0]
    for card in ax.patches:
        bounds = card.get_path().get_extents()
        assert ax.get_xlim()[0] < bounds.xmin < bounds.xmax < ax.get_xlim()[1]
        assert ax.get_ylim()[0] < bounds.ymin < bounds.ymax < ax.get_ylim()[1]
    for registered, batch in [('other-test-run', inference),
                              (run_id, dict(inference, run_id='other-test-run')),
                              (run_id, dict(inference, resolved_version='8'))]:
        with pytest.raises(ValueError, match='identities must agree'):
            plot_identity(run_id, '7', registered, batch)
    with pytest.raises(ValueError, match='identities must agree'):
        plot_identity(run_id, None, run_id, {'run_id': run_id})


@pytest.mark.parametrize('delta', [0., 5e-7, 3e-6])
def test_recovery_delta_and_checks_match_observed_data(delta):
    report, planned, predictions = recovery_inputs(delta)
    fig = plot_recovery(report, planned, predictions)
    assert fig.linden_data['absolute_rmse_delta'] == delta
    assert fig.linden_data['passed'] == (delta <= report['tolerance'])
    delta_ax = fig.axes[1]
    np.testing.assert_allclose(delta_ax.collections[0].get_offsets(), [[delta, .5]])
    assert 0 in delta_ax.get_xticks()
    assert report['tolerance'] in delta_ax.get_xticks()
    assert delta_ax.get_xlim()[1] > max(delta, report['tolerance'])
    assert 'kWh' in delta_ax.get_xlabel()


def test_recovery_exposes_actual_failures_even_if_report_claims_pass():
    report, planned, predictions = recovery_inputs()
    predictions = predictions.iloc[::-1].copy()
    predictions.loc[0, 'prediction_kwh'] = np.nan
    report['invariants']['source'] = False
    report['inference']['elapsed_seconds'] = 61
    fig = plot_recovery(report, planned, predictions)
    checks = fig.linden_data['checks']
    assert not fig.linden_data['passed']
    assert not checks['Output: row ID order and uniqueness']
    assert not checks['Output: finite predictions (kWh)']
    assert not checks['Recipe: source']
    assert not checks['Batch: 61 seconds ≤ 60 seconds']
    visible = [cell.get_text().get_text() for cell in fig.axes[0].tables[0].get_celld().values()]
    assert visible.count('FAIL') == 4
    with pytest.raises(ValueError, match='explicit boolean'):
        plot_recovery(dict(report, invariants={'source': 'True'}), planned, predictions)


def test_recovery_requires_complete_proof_and_retains_reported_failures():
    report, planned, predictions = recovery_inputs()
    for invariant in report['invariants']:
        changed = dict(report, invariants={key: value for key, value in report['invariants'].items() if key != invariant})
        with pytest.raises(ValueError, match='source/data/environment/config/partition'):
            plot_recovery(changed, planned, predictions)
    for missing in ['passed', 'reproduced_run_id', 'version']:
        changed = dict(report)
        del changed[missing]
        with pytest.raises(ValueError):
            plot_recovery(changed, planned, predictions)
    for missing in ['run_id', 'resolved_version', 'rows', 'complete_within_60s']:
        changed_inference = dict(report['inference'])
        del changed_inference[missing]
        with pytest.raises(ValueError):
            plot_recovery(dict(report, inference=changed_inference), planned, predictions)
    changed = dict(report, passed=False, inference=dict(report['inference'], complete_within_60s=False,
                                                       run_id='other-test-run', resolved_version='4', rows=25))
    fig = plot_recovery(changed, planned, predictions)
    assert not fig.linden_data['passed']
    checks = fig.linden_data['checks']
    assert not checks['Report: overall recovery accepted']
    assert not checks['Report: batch deadline accepted']
    assert not checks['Lineage: batch uses reproduced run']
    assert not checks['Lineage: batch resolves recovered version']
    assert not checks['Output: recorded row count matches returned rows']
    assert checks['Batch: 0.2 seconds ≤ 60 seconds']


def test_save_same_layout_to_caller_selected_directory(tmp_path):
    report, planned, predictions = recovery_inputs()
    fig = plot_recovery(report, planned, predictions)
    positions = [ax.get_position().bounds for ax in fig.axes]
    files = save_figure(fig, tmp_path / 'state/figures/recovery')
    assert set(files) == {'svg', 'png'}
    assert files['svg'].read_text().startswith('<?xml')
    assert files['png'].read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    assert positions == [ax.get_position().bounds for ax in fig.axes]
    from PIL import Image
    with Image.open(files['png']) as image:
        assert abs(image.info['dpi'][0] - 180) < .1


def test_svg_retains_editable_labels_without_changing_global_font_policy(tmp_path):
    import matplotlib
    from xml.etree import ElementTree
    report, planned, predictions = recovery_inputs()
    fig = plot_recovery(report, planned, predictions)
    original = matplotlib.rcParams['svg.fonttype']
    with matplotlib.rc_context({'svg.fonttype': 'path'}):
        files = save_figure(fig, tmp_path / 'editable-recovery')
        assert matplotlib.rcParams['svg.fonttype'] == 'path'
    assert matplotlib.rcParams['svg.fonttype'] == original
    document = ElementTree.fromstring(files['svg'].read_text())
    labels = [''.join(node.itertext()) for node in document.iter('{http://www.w3.org/2000/svg}text')]
    assert 'Check the receiving evidence' in labels
    assert 'Absolute validation RMSE delta (kWh)' in labels
    assert 'PASS' in labels
