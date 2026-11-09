import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(15, 6.4)); ax.set_xlim(0, 15); ax.set_ylim(0, 6.4); ax.axis('off')
W, H = 2.9, 1.2
nodes = {
 'A': (1.7, 4.6, 'Bodziec\nobraz 4000 ms + szary 1000 ms\n(PsychoPy, flip)'),
 'B': (5.6, 4.6, 'Uczestnik\nswobodne oglądanie'),
 'C': (9.5, 4.6, 'Czujnik EDA / HR\n(LBK: GSR; dom: symulator\n4 Hz, TCP :5555)'),
 'D': (13.4, 4.6, 'Most sim_to_lsl.py\nNDJSON → LSL LBK_Sim\n(czas local_clock)'),
 'E': (13.4, 1.6, 'PsychoPy – odbiór\npull_chunk(timeout=0.0)\nw każdej klatce'),
 'F': (9.5, 1.6, 'Okno 5 s → cechy\nHR, RMSSD, mediana EDA\nraport co 1 s (konsola)'),
 'G': (5.6, 1.6, 'Decyzja (reguła, KL-D)\nnp. EDA > próg?\n+ znacznik adaptation:*'),
 'H': (1.7, 1.6, 'Zmiana – TYLKO między próbami\ndłuższa przerwa / ekran\nneutralny (limit czasu)'),
}
for k,(x,y,t) in nodes.items():
    fc = '#fdecea' if k=='H' else '#eef3fb'
    ax.add_patch(FancyBboxPatch((x-W/2, y-H/2), W, H, boxstyle='round,pad=0.05,rounding_size=0.15', fc=fc, ec='#34495e', lw=1.5))
    ax.text(x, y, t, ha='center', va='center', fontsize=9.5)
def arrow(a, b, label, side='top', curve=0):
    xa, ya, _ = nodes[a]; xb, yb, _ = nodes[b]
    if ya == yb:
        s = 1 if xb > xa else -1
        p1, p2 = (xa + s*W/2+0.05, ya), (xb - s*W/2-0.05, yb); lx, ly = (xa+xb)/2, ya + (0.85 if side=='top' else 1.15)
    else:
        s = 1 if yb > ya else -1
        p1, p2 = (xa, ya + s*H/2+0.05), (xb, yb - s*H/2-0.05); lx, ly = xa + (0.45 if a=='D' else -0.45), (ya+yb)/2
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=18, lw=1.6, color='#34495e'))
    ax.text(lx, ly, label, ha='left' if a=='D' else ('right' if a=='H' else 'center'), va='center', fontsize=8.3, color='#b03a2e')
arrow('A','B','Δ1 percepcja\n~0,1–0,3 s')
arrow('B','C','Δ2 latencja SCR\n~1–3 s (szczyt do ~5 s)')
arrow('C','D','Δ3 próbkowanie 4 Hz ≤ 250 ms\n+ TCP lokalnie ~ms')
arrow('D','E','Δ4 LSL\nlokalnie\n< 10 ms')
arrow('E','F','Δ5 ≤ 1 klatka\n(16,7 ms przy 60 Hz)', side='bottom')
arrow('F','G','Δ6 okno 5 s: średnia\nopóźniona ~2,5 s;\nraport co 1 s (≤ 1 s)', side='bottom')
arrow('G','H','Δ7 czekanie na koniec\nobrazu: do 5 s\n(4 s obraz + 1 s szary)', side='bottom')
arrow('H','A','Δ8 następna próba\npo przerwie')
ax.text(7.5, 6.15, 'P3 – pętla biofeedbacku (KL-B): bodziec → uczestnik → czujnik → LSL → PsychoPy → decyzja → zmiana', ha='center', fontsize=12, weight='bold')
ax.text(7.5, 0.35, 'Zasada nienaruszalności: decyzja nie zmienia czasu ekspozycji (4000 ms), szarego ekranu (1000 ms) ani kolejności obrazów. '
        'Łączne opóźnienie bodziec → zmiana: kilka sekund,\nwięc adaptacja działa dopiero w następnej przerwie. Czerwone Δ = miejsca opóźnień (wartości orientacyjne; pomiar opóźnień – KL-E).',
        ha='center', fontsize=8.6, color='#333')
fig.savefig('docs/img/petla_biofeedback.png', dpi=160, bbox_inches='tight'); print('ok')
