#!/usr/bin/env python3
"""Wykres EDA i znaczników z PRAWDZIWEGO pliku XDF nagranego w LabRecorder.

Użycie (z katalogu głównego repozytorium):
    python3 overlay/plot_xdf.py sample_data/PLIK.xdf --out docs/img/eda_markery.png

Oś X = czas LSL (wspólny zegar obu strumieni) od pierwszej próbki LBK_Sim.
Próbki z quality != ok (noisy/lost/brak) są pokazywane jako przerwy w linii.
"""
import argparse
from pathlib import Path

# kategoria znacznika -> (kolor, styl linii); pozostałe kategorie: szary
STYLE = {
    'exp': ('black', '-'),
    'trial': ('0.6', ':'),
    'stim:onset': ('tab:red', '--'),
    'stim:offset': ('tab:orange', ':'),
    'resp': ('tab:green', '-.'),
}


def channel_index(stream, label, default):
    try:
        names = [c['label'][0] for c in stream['info']['desc'][0]['channels'][0]['channel']]
        return names.index(label)
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def style_for(marker):
    head = marker.split('|')[0]
    if head in STYLE:
        return STYLE[head]
    return STYLE.get(head.split(':')[0], ('0.5', ':'))


def plot_xdf(path, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import pyxdf

    streams, _ = pyxdf.load_xdf(str(path))
    by_name = {s['info']['name'][0]: s for s in streams}
    sim, mk = by_name.get('LBK_Sim'), by_name.get('LBK_Markers')
    if sim is None or mk is None:
        raise SystemExit(f'W XDF muszą być LBK_Sim i LBK_Markers, są: {list(by_name)}')

    data = np.asarray(sim['time_series'], dtype=float)
    t = np.asarray(sim['time_stamps'], dtype=float)
    eda = data[:, channel_index(sim, 'eda_us', 1)].copy()
    quality = data[:, channel_index(sim, 'quality', 4)]
    bad = quality != 0.0                      # NaN != 0 -> też odrzucone
    eda[bad] = np.nan
    t0 = t[0]

    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.plot(t - t0, eda, lw=1.2, color='tab:blue', label='EDA (µS), quality = ok')
    ymax = np.nanmax(eda) if np.isfinite(eda).any() else 1.0

    seen = set()
    markers = []
    for stamp, row in zip(mk['time_stamps'], mk['time_series']):
        value = row[0]
        value = value.decode('utf-8') if isinstance(value, bytes) else str(value)
        markers.append((float(stamp) - t0, value))
        color, ls = style_for(value)
        head = value.split('|')[0]
        ax.axvline(float(stamp) - t0, color=color, ls=ls, lw=1,
                   label=head if head not in seen else None)
        seen.add(head)
        if head.startswith(('exp', 'stim:onset', 'resp')):
            short = value.split('|')[1] if '|' in value and head == 'stim:onset' else head
            ax.text(float(stamp) - t0, ymax, ' ' + short, rotation=90, fontsize=7,
                    va='top', ha='right', color=color)

    ax.set(xlabel='Czas LSL od początku zapisu LBK_Sim (s)', ylabel='EDA (µS)',
           title=f'{Path(path).name}: EDA (LBK_Sim) i znaczniki (LBK_Markers)')
    ax.grid(alpha=0.2)
    ax.legend(loc='upper left', fontsize=7, ncol=3, frameon=False)
    fig.tight_layout()
    fig.savefig(out, dpi=170)
    plt.close(fig)

    dur = t[-1] - t[0]
    print(f'Zapisano {out}; strumienie: {list(by_name)}')
    print(f'LBK_Sim: {len(t)} probek, {dur:.1f} s, odrzucone (quality != ok): {int(bad.sum())}')
    print(f'LBK_Markers: {len(markers)} znacznikow')
    for rel, value in markers:
        print(f'  {rel:8.3f} s  {value}')
    required = ['exp:start', 'trial:start', 'stim:onset', 'resp', 'exp:end']
    missing = [r for r in required if not any(v.startswith(r) for _, v in markers)]
    if missing:
        print('UWAGA: brak wymaganych znacznikow:', ', '.join(missing))
    if dur < 120:
        print('UWAGA: LBK_Sim krocej niz 120 s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('xdf', type=Path)
    parser.add_argument('--out', type=Path, default=Path('docs/img/eda_markery.png'))
    a = parser.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    plot_xdf(a.xdf, a.out)
