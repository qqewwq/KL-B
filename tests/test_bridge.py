"""Test dwóch linii JSON bez uruchamiania LSL."""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'lsl'))
from sim_to_lsl import parse_line, CHANNELS


def test_two_lines():
    lines = (Path(__file__).parent / 'two_lines.jsonl').read_text(encoding='utf-8').splitlines()
    assert len(lines) == 2
    a, b = [parse_line(x) for x in lines]
    assert len(a) == len(b) == len(CHANNELS) == 10
    assert a[0] == 70.0 and a[4] == 0.0
    assert a[5] == 400.0 and a[8] == 3.1 and a[9] == 0.4
    assert b[0] == 74.0 and b[4] == 2.0
    assert all(math.isnan(b[i]) for i in range(5,10))
    assert json.loads(lines[1])['quality'] == 'lost'


if __name__ == '__main__':
    test_two_lines()
    print('OK: 2 linie, brakujace pola = NaN, quality zakodowane poprawnie')
