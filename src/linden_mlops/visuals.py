"""Figures derived from retained local records; no fitting or state changes.

Every plot returns a Figure and exposes its plotted evidence in `linden_data`.
Figures use no global pyplot state or backend setting. Callers choose where to
save them; displaying a figure never updates published lesson assets.
"""
from pathlib import Path
import math
import textwrap

import numpy as np
from matplotlib import rc_context
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

from .lifecycle import verify_summary
from .pipeline import FEATURES, validate_ranges


CREAM = '#ECEBE4'
FOREST = '#17482E'
GREEN = '#27784C'
LIME = '#D7FF94'
FAILURE = '#B91C1C'


def _figure(title, subtitle, width=11, height=5):
    fig = Figure(figsize=(width, height), facecolor=CREAM)
    fig.suptitle(title, x=.07, y=.97, ha='left', color=FOREST,
                 fontsize=17, fontweight='bold')
    fig.text(.07, .885, subtitle, ha='left', va='top', fontsize=9, color=FOREST)
    fig.subplots_adjust(left=.09, right=.96, bottom=.16, top=.77, wspace=.4)
    return fig


def _style(ax):
    ax.set_facecolor(CREAM)
    for name, spine in ax.spines.items():
        spine.set_visible(name in {'left', 'bottom'})
        spine.set_color(FOREST)
    ax.tick_params(colors=FOREST)
    ax.xaxis.label.set_color(FOREST)
    ax.yaxis.label.set_color(FOREST)
    ax.title.set_color(FOREST)


def plot_contract(frame):
    """Show partition counts and actual validator outcomes for five hour probes.

    Only partition labels and a feature-row copy are read. No target column,
    including the final partition's targets, is inspected.
    """
    partitions = ['train', 'validation', 'final']
    if frame.empty or set(frame['partition'].unique()) != set(partitions):
        raise ValueError('Expected nonempty train, validation and final partitions')
    counts = {name: int(frame['partition'].eq(name).sum()) for name in partitions}
    base = frame.loc[frame['partition'].eq('train'), FEATURES].iloc[[0]].copy(deep=True)
    validate_ranges(base)
    probes = []
    for hour in [-1, 0, 1.5, 23, 24]:
        sample = base.copy(deep=True)
        sample['hour'] = float(hour)
        try:
            validate_ranges(sample)
            accepted = True
        except ValueError:
            accepted = False
        probes.append({'hour': hour, 'accepted': accepted})
    fig = _figure('Read the split; test the input contract',
                  'Derived from local input labels and executed validator probes. Final partition: counts only; targets stay closed.')
    counts_ax, probes_ax = fig.subplots(1, 2)
    for ax in fig.axes:
        _style(ax)
    bars = counts_ax.bar(partitions, list(counts.values()), color=[FOREST, GREEN, LIME], edgecolor=FOREST)
    counts_ax.bar_label(bars, padding=4, color=FOREST)
    counts_ax.set_ylim(0, max(counts.values()) * 1.2)
    counts_ax.set_ylabel('Rows (count)')
    counts_ax.set_xlabel('Fixed partition')
    counts_ax.set_title('Actual partition sizes', loc='left', fontsize=11)
    for accepted, marker, color, label in [(True, 'o', GREEN, 'Accepted'), (False, 'X', FAILURE, 'Rejected')]:
        positions = [index for index, probe in enumerate(probes) if probe['accepted'] == accepted]
        probes_ax.scatter(positions, [int(accepted)] * len(positions),
                          s=90, marker=marker, color=color, label=label, zorder=3)
    probes_ax.set_yticks([0, 1], ['Rejected', 'Accepted'])
    probes_ax.set_xticks(range(len(probes)), ['−1', '0', '1.5', '23', '24'])
    probes_ax.set_ylim(-.5, 1.7)
    probes_ax.set_xlim(-.5, 4.5)
    probes_ax.set_xlabel('Hour probe (hours; discrete cases)')
    probes_ax.set_ylabel('Executed exercise outcome')
    probes_ax.set_title('Integer and boundary probes', loc='left', fontsize=11)
    probes_ax.legend(frameon=False, loc='upper center', ncols=2, fontsize=8)
    fig.linden_data = {'partition_counts': counts, 'hour_probes': probes}
    return fig


def plot_experiments(rows):
    """Plot precisely five comparable validation records as discrete points."""
    if len(rows) != 5:
        raise ValueError('Supply exactly the five saved matrix records')
    result = verify_summary(rows, rows.iloc[0]['run_id'])
    values = rows.copy().sort_values('alpha', key=lambda series: series.astype(float))
    alpha = values['alpha'].astype(float).to_numpy()
    if not np.isfinite(alpha).all() or not (alpha > 0).all():
        raise ValueError('Alpha must be finite and positive for a logarithmic axis')
    mae = values['mae_kwh'].astype(float).to_numpy()
    if not np.isfinite(mae).all() or (mae < 0).any():
        raise ValueError('Validation MAE must be finite and nonnegative')
    winner = result['best_run_id']
    is_winner = values['run_id'].eq(winner).to_numpy()
    fig = _figure('Compare the declared validation runs',
                  'Discrete observations under the supplied fixed conditions. RMSE selects the run; MAE is diagnostic. No training or final scores.')
    for ax, metric, title in zip(fig.subplots(1, 2), ['rmse_kwh', 'mae_kwh'],
                                 ['Primary: validation RMSE', 'Diagnostic: validation MAE']):
        _style(ax)
        y = values[metric].astype(float).to_numpy()
        ax.scatter(alpha[~is_winner], y[~is_winner], s=55, color=FOREST, marker='o', label='Other declared runs')
        ax.scatter(alpha[is_winner], y[is_winner], s=160, color=GREEN, marker='*', edgecolor=FOREST,
                   label='Lowest validation RMSE')
        ax.set_xscale('log')
        ax.set_xticks(alpha, [f'{number:g}' for number in alpha])
        ax.set_xlabel('Ridge alpha (log scale)')
        ax.set_ylabel(f'Validation {"RMSE" if metric == "rmse_kwh" else "MAE"} (kWh)')
        ax.set_title(title, loc='left', fontsize=11)
        ax.margins(x=.15, y=.25)
        selected = values.loc[values.run_id.eq(winner)].iloc[0]
        ax.annotate(f'α={float(selected.alpha):g}; {float(selected[metric]):.6g} kWh',
                    (float(selected.alpha), float(selected[metric])), xytext=(7, 12),
                    textcoords='offset points', color=GREEN, fontsize=8)
    fig.axes[0].legend(frameon=False, loc='upper left', fontsize=8)
    fig.linden_data = {'winner_run_id': winner, 'records': [
        {'run_id': row.run_id, 'alpha': float(row.alpha), 'rmse_kwh': float(row.rmse_kwh),
         'mae_kwh': float(row.mae_kwh)} for row in values.itertuples()]}
    return fig


def plot_identity(run_id, model_version, registered_run_id, inference):
    """Connect matching recorded identities; reject an inconsistent chain."""
    version = str(model_version)
    if (not run_id or model_version is None or not version
            or inference.get('resolved_version') is None or registered_run_id != run_id
            or inference.get('run_id') != run_id
            or str(inference.get('resolved_version')) != version):
        raise ValueError('Selected, registered and batch-resolved run/version identities must agree')
    wrap = lambda value: '\n'.join(textwrap.wrap(str(value), width=16))
    fig = _figure('Trace one selected model into the batch',
                  'Derived diagram from local selection, registry and inference records; this is not an MLflow UI capture.', height=4.7)
    ax = fig.subplots()
    ax.set_axis_off()
    ax.set_xlim(-.03, 1.03)
    ax.set_ylim(0, 1)
    cards = [
        ('Selected training run', f'Run ID\n{wrap(run_id)}'),
        ('Registered artifact', f'Version {version}\nSource run ID\n{wrap(registered_run_id)}'),
        ('Batch resolved identity', f'Version {inference["resolved_version"]}\nRun ID\n{wrap(inference["run_id"])}'),
    ]
    for number, (title, text) in enumerate(cards):
        left = number * .35
        box = FancyBboxPatch((left, .15), .29, .8, boxstyle='round,pad=0.012',
                             edgecolor=FOREST, facecolor=LIME if number == 2 else CREAM,
                             linewidth=1.6)
        ax.add_patch(box)
        ax.text(left + .145, .84, title, ha='center', va='top', fontsize=10, color=FOREST, weight='bold')
        ax.text(left + .145, .62, text, ha='center', va='top', fontsize=10, color=FOREST,
                fontfamily='monospace', linespacing=1.5)
        if number < 2:
            ax.annotate('', xy=(left + .338, .55), xytext=(left + .302, .55),
                        arrowprops={'arrowstyle': '->', 'color': FOREST, 'lw': 1.5})
    actual = []
    if 'rows' in inference:
        actual.append(f'Observed batch: {inference["rows"]} rows')
    if 'elapsed_seconds' in inference:
        actual.append(f'elapsed {float(inference["elapsed_seconds"]):.4g} seconds')
    fig.text(.09, .07, '; '.join(actual) + '. Identity agreement alone does not establish readiness.', fontsize=9, color=FOREST)
    fig.linden_data = {'selected_run_id': run_id, 'registered_run_id': registered_run_id,
                       'registered_version': version, 'inference': dict(inference), 'chain_matches': True}
    return fig


def plot_recovery(report, planned, predictions):
    """Show declared invariants, actual output checks and measured RMSE delta."""
    invariants = report['invariants']
    required = {'source', 'data', 'environment', 'config', 'partition'}
    if (not required.issubset(invariants)
            or any(not isinstance(value, (bool, np.bool_)) for value in invariants.values())):
        raise ValueError('Recovery needs explicit boolean source/data/environment/config/partition invariants')
    inference = report['inference']
    if (not isinstance(report.get('passed'), (bool, np.bool_))
            or not isinstance(inference.get('complete_within_60s'), (bool, np.bool_))):
        raise ValueError('Recovery and batch acceptance must be explicit boolean results')
    if (not report.get('reproduced_run_id') or not inference.get('run_id')
            or report.get('version') is None or inference.get('resolved_version') is None
            or not str(report['version']) or not str(inference['resolved_version'])):
        raise ValueError('Recovery needs reproduced run ID, version and batch-resolved run/version evidence')
    if not isinstance(inference.get('rows'), (int, np.integer)) or isinstance(inference['rows'], bool):
        raise ValueError('Recovery needs an explicit recorded batch row count')
    delta, tolerance = float(report['absolute_rmse_delta']), float(report['tolerance'])
    if not math.isfinite(delta) or delta < 0 or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('Recovery delta must be nonnegative and tolerance must be positive; both must be finite')
    if 'row_id' not in planned or 'row_id' not in predictions or 'prediction_kwh' not in predictions:
        raise ValueError('Planned and prediction rows need row_id; predictions need prediction_kwh')
    row_alignment = (planned['row_id'].tolist() == predictions['row_id'].tolist()
                     and planned['row_id'].notna().all() and predictions['row_id'].notna().all()
                     and not planned['row_id'].duplicated().any()
                     and not predictions['row_id'].duplicated().any())
    try:
        finite = bool(np.isfinite(predictions['prediction_kwh'].to_numpy(dtype=float)).all())
    except (ValueError, TypeError):
        finite = False
    elapsed = float(inference['elapsed_seconds'])
    deadline = math.isfinite(elapsed) and 0 <= elapsed <= 60
    checks = {f'Recipe: {key}': bool(value) for key, value in invariants.items()}
    checks.update({'Report: overall recovery accepted': bool(report['passed']),
                   'Report: batch deadline accepted': bool(inference['complete_within_60s']),
                   'Lineage: batch uses reproduced run': inference['run_id'] == report['reproduced_run_id'],
                   'Lineage: batch resolves recovered version': str(inference['resolved_version']) == str(report['version']),
                   'Output: recorded row count matches returned rows': inference['rows'] == len(predictions),
                   'Output: row ID order and uniqueness': bool(row_alignment),
                   'Output: 24 planned and 24 returned rows': len(planned) == len(predictions) == 24,
                   'Output: finite predictions (kWh)': finite,
                   f'Batch: {elapsed:.4g} seconds ≤ 60 seconds': deadline,
                   'Validation: RMSE delta within tolerance': delta <= tolerance})
    fig = _figure('Check the receiving evidence',
                  'Actual local recovery checks and output rows. Final targets are not used. PASS applies only to these displayed checks.',
                  width=12, height=max(5.8, 2.6 + len(checks) * .28))
    table_ax, delta_ax = fig.subplots(1, 2, gridspec_kw={'width_ratios': [1.65, 1]})
    table_ax.set_axis_off()
    table = table_ax.table(cellText=[[label, 'PASS' if passed else 'FAIL'] for label, passed in checks.items()],
                           colLabels=['Observed check', 'Result'], colWidths=[.84, .16],
                           cellLoc='left', loc='center', bbox=[-.04, 0, 1.08, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(CREAM)
        cell.set_facecolor(FOREST if row == 0 else CREAM)
        cell.get_text().set_color(CREAM if row == 0 else FOREST)
        if col == 1 and row > 0:
            passed = list(checks.values())[row - 1]
            cell.set_facecolor(LIME if passed else FAILURE)
            cell.get_text().set_color(FOREST if passed else 'white')
    _style(delta_ax)
    delta_ax.axvspan(0, tolerance, color=LIME, alpha=.8, label='Within declared tolerance')
    delta_ax.axvline(tolerance, color=FOREST, linestyle='--', linewidth=1.4, label='Declared tolerance')
    delta_ax.scatter([delta], [.5], color=GREEN if delta <= tolerance else FAILURE,
                     marker='o' if delta <= tolerance else 'X', s=110, zorder=3)
    delta_ax.text(.04, .8, f'Observed Δ = {delta:.6g} kWh', transform=delta_ax.transAxes,
                  ha='left', fontsize=9, color=FOREST)
    right = max(tolerance, delta) * 1.28
    delta_ax.set_xlim(-right * .06, right)
    delta_ax.set_ylim(0, 1)
    delta_ax.set_yticks([])
    ticks = sorted({0., tolerance, delta})
    delta_ax.set_xticks(ticks)
    delta_ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: '0' if value == 0 else f'{value:.1e}'))
    delta_ax.tick_params(axis='x', labelrotation=25)
    delta_ax.set_xlabel('Absolute validation RMSE delta (kWh)')
    delta_ax.set_title('Measured delta against the contract', loc='left', fontsize=11)
    delta_ax.legend(frameon=False, fontsize=8, loc='lower left')
    fig.linden_data = {'checks': checks, 'passed': all(checks.values()),
                       'absolute_rmse_delta': delta, 'tolerance': tolerance,
                       'planned_rows': len(planned), 'prediction_rows': len(predictions)}
    return fig


def save_figure(fig, destination_base):
    """Save one unchanged layout as SVG and PNG (180 dpi) at a caller's path."""
    base = Path(destination_base)
    if base.suffix.lower() in {'.svg', '.png'}:
        base = base.with_suffix('')
    base.parent.mkdir(parents=True, exist_ok=True)
    paths = {'svg': Path(str(base) + '.svg'), 'png': Path(str(base) + '.png')}
    # Keep labels editable in the SVG without changing the caller's global
    # Matplotlib settings or the PNG rendering of the same figure geometry.
    with rc_context({'svg.fonttype': 'none'}):
        fig.savefig(paths['svg'], facecolor=fig.get_facecolor())
    fig.savefig(paths['png'], dpi=180, facecolor=fig.get_facecolor())
    return paths
