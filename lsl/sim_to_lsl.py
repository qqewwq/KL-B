#!/usr/bin/env python3
"""Most TCP (NDJSON) -> LSL; format kanałów zapisany w README/Build Book."""
import argparse
import json
import math
import socket
import time

# Kolejność kanałów w LBK_Sim (numeryczne float32)
CHANNELS = (
    'hr', 'eda_us', 'rr_ms', 'focus', 'quality',
    'gaze_x', 'gaze_y', 'gaze_valid', 'pupil_mm', 'resp',
)
QUALITY = {'ok': 0.0, 'noisy': 1.0, 'lost': 2.0}
UNITS = ('bpm', 'uS', 'ms', 'a.u.', 'code', 'pix', 'pix', '0/1', 'mm', 'a.u.')


def number(value):
    """Zamienia brak/null i niepoprawne wartości na NaN."""
    if value is None or isinstance(value, bool):
        return math.nan
    try:
        result = float(value)
        return result if math.isfinite(result) else math.nan
    except (ValueError, TypeError):
        return math.nan


def parse_line(line):
    """Wczytuje jeden NDJSON, nie korzysta ze scenario do sterowania."""
    obj = json.loads(line)
    if not isinstance(obj, dict):
        raise ValueError('Rekord JSON musi być obiektem')
    values = []
    for ch in CHANNELS:
        if ch == 'quality':
            quality = obj.get('quality')
            values.append(QUALITY.get(quality, math.nan) if isinstance(quality, str) else number(quality))
        else:
            values.append(number(obj.get(ch)))
    return values


def make_outlet():
    from pylsl import StreamInfo, StreamOutlet
    info = StreamInfo('LBK_Sim', 'Physio', len(CHANNELS), 0, 'float32', 'lbk-p3-sim-v1')
    # Nieregularne odstępy w TCP: używamy czasu odbioru LSL, nie symulowanego pola t.
    chs = info.desc().append_child('channels')
    for label, unit in zip(CHANNELS, UNITS):
        ch = chs.append_child('channel')
        ch.append_child_value('label', label)
        ch.append_child_value('unit', unit)
        ch.append_child_value('type', 'float32')
    info.desc().append_child_value('quality_codes', 'ok=0;noisy=1;lost=2;missing=NaN')
    return StreamOutlet(info)


def serve(host='127.0.0.1', port=5555):
    from pylsl import local_clock
    outlet = make_outlet()
    print('LSL: LBK_Sim (Physio), 10 kanalow; quality 0=ok 1=noisy 2=lost')
    while True:
        try:
            print(f'Laczenie z symulatorem TCP {host}:{port} ...')
            with socket.create_connection((host, port), timeout=5) as conn:
                conn.settimeout(None)
                print(f'Polaczono z symulatorem {host}:{port}; publikuje LBK_Sim')
                with conn.makefile('r', encoding='utf-8') as data:
                    for line in data:
                        try:
                            sample = parse_line(line)
                        except (ValueError, json.JSONDecodeError) as exc:
                            print(f'Pominieto niepoprawna linie: {exc}')
                            continue
                        outlet.push_sample(sample, timestamp=local_clock())
        except (OSError, ConnectionError) as exc:
            print(f'Brak TCP / rozlaczenie: {exc}; kolejna proba za 2 s')
            time.sleep(2)
        except KeyboardInterrupt:
            print('Zatrzymano most.')
            break


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=5555)
    args = p.parse_args()
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        print('Koniec')
