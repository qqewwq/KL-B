"""Test cech z okna (HR, RMSSD, mediana EDA) bez pakietu pylsl."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiment'))
from lsl_runtime import calculate_features

NAN = float('nan')


def test_features():
    # (czas, [hr, eda_us, rr_ms, focus, quality]); quality: 0=ok 1=noisy 2=lost
    records = [
        (1., [60., 2., 800., .5, 0.]),
        (2., [70., 4., 820., .5, 0.]),
        (3., [80., 3., 790., .5, 0.]),
        (4., [90., 100., 950., .5, 1.]),   # noisy -> pomijamy, przerywa ciąg RR
        (5., [NAN, NAN, NAN, NAN, 2.]),     # lost -> pomijamy
        (6., [70., 5., 760., .5, 0.]),      # nowy ciąg RR
        (7., [80., 6., 780., .5, 0.]),
        (8., [75., 7., 700., .5, NAN]),     # brak quality -> pomijamy
    ]
    f = calculate_features(records)
    assert f['valid'] == 5 and f['bad'] == 3
    assert abs(f['mean_hr_bpm'] - 72.) < 1e-9                 # (60+70+80+70+80)/5
    assert f['median_eda_us'] == 4.                           # mediana 2,3,4,5,6
    # różnice tylko między sąsiednimi poprawnymi: 20, -30, 20 (nie 760-790!)
    expected = math.sqrt((20 ** 2 + 30 ** 2 + 20 ** 2) / 3)
    assert abs(f['rmssd_ms'] - expected) < 1e-9

    # za mało próbek do RMSSD -> NaN, program się nie zatrzymuje
    one = calculate_features([(1., [60., 2., 800., .5, 0.])])
    assert math.isnan(one['rmssd_ms'])
    empty = calculate_features([])
    assert math.isnan(empty['mean_hr_bpm']) and empty['valid'] == 0


if __name__ == '__main__':
    test_features()
    print('OK: HR, RMSSD z sasiednich roznic RR, mediana EDA, '
          'odrzucenie noisy/lost/NaN')
