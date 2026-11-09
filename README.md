# KL-B – P3 „Obraz, ocena, pobudzenie” (PsychoPy + LSL)

Szkielet badania głównego „Qualia, barwa i subiektywne doświadczenie” z integracją LSL.
**Pełna instrukcja odtworzenia: [`BUILD_BOOK.md`](BUILD_BOOK.md)** (rozdziały 3, 4, 6).
Repozytorium **prywatne** – zawiera materiały LBK (obrazy A–D).

## Zawartość (co oddajemy w KL-B)

| Ścieżka | Co to jest |
|---|---|
| `experiment/P3_KL_B.psyexp` | eksperyment PsychoPy Builder (instrukcja → 4 próby z CSV → pytanie → koniec; MouseGaze + Eyetracker Record) |
| `experiment/lsl_runtime.py` | kod Code Components: `LBK_Markers`, odbiór `LBK_Sim`, okno 5 s (HR, RMSSD, EDA) |
| `experiment/conditions/L1_LBK_4obrazy_test.csv` | plik warunków |
| `experiment/stimuli/Bodziec A–D.PNG` | bodźce z pakietu P3 |
| `lsl/sim_to_lsl.py` | most symulator (TCP) → LSL `LBK_Sim` |
| `simulator/symulator_biosygnalow.py` | symulator z kursu (potrzebny do uruchomienia) |
| `tests/two_lines.jsonl`, `tests/test_bridge.py`, `tests/test_features.py` | linie testowe i testy |
| `sample_data/*.xdf` | nagranie 2 min (symulator + MouseGaze) |
| `overlay/plot_xdf.py`, `overlay/requirements.txt` | wykres EDA + znaczniki z XDF |
| `docs/img/eda_markery.png` | wykres – dowód wspólnej osi czasu |
| `docs/img/petla_biofeedback.png`, `docs/petla_biofeedback.py`, `docs/PETLA_BIOFEEDBACK.mmd` | schemat pętli biofeedbacku |
| `docs/KARTA_ZRODEL.md` | karta źródeł |

## Szybki start (szczegóły: Build Book 6.4–6.8)

```bash
# okno 1
python3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --port 5555
# okno 2
python3 lsl/sim_to_lsl.py
# PsychoPy Builder → experiment/P3_KL_B.psyexp → Run
# LabRecorder → Update → LBK_Sim + LBK_Markers → Start (na ekranie instrukcji, przed spacją)
python3 overlay/plot_xdf.py sample_data/P3_KL-B_TEST-01_S001.xdf --out docs/img/eda_markery.png
```

Windows: `py -3` zamiast `python3`. Testy bez LSL: `python3 tests/test_bridge.py`, `python3 tests/test_features.py`.
