"""Odbiór strumienia LBK_Sim, okno kroczące 5 s i znaczniki LBK_Markers.

Moduł importowany przez Code Component `lsl_intro` (Begin Experiment) w
experiment/P3_KL_B.psyexp. Kolejność kanałów musi być identyczna jak w
lsl/sim_to_lsl.py (CHANNELS).
"""
from collections import deque
import math
import statistics

# Indeksy kanałów LBK_Sim (patrz lsl/sim_to_lsl.py)
HR, EDA, RR, FOCUS, QUALITY = 0, 1, 2, 3, 4
QUALITY_OK = 0.0  # ok=0, noisy=1, lost=2, brak pola=NaN


def _finite(sample, ch):
    """Wartość kanału jako float albo None (NaN, brak, zły typ)."""
    try:
        x = float(sample[ch])
    except (IndexError, TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def is_ok(sample):
    """True tylko dla quality == 0 (ok). NaN/noisy/lost -> False."""
    return _finite(sample, QUALITY) == QUALITY_OK


def calculate_features(records):
    """records: lista (czas_LSL, sample) w kolejności czasu.

    Zwraca średnie HR [bpm], RMSSD [ms] i medianę EDA [µS] z próbek quality=ok
    oraz liczbę próbek poprawnych i odrzuconych.

    RMSSD = sqrt(mean((RR[i+1] - RR[i])^2)) liczone WYŁĄCZNIE z kolejnych
    (sąsiednich) poprawnych próbek: próbka odrzucona (noisy/lost/NaN) przerywa
    ciąg, więc nie liczymy różnicy „ponad” artefaktem.
    """
    hr, eda, diffs = [], [], []
    valid = bad = 0
    prev_rr = None
    for _, sample in records:
        if not is_ok(sample):
            bad += 1
            prev_rr = None            # artefakt przerywa ciąg RR
            continue
        valid += 1
        h, e, rr = _finite(sample, HR), _finite(sample, EDA), _finite(sample, RR)
        if h is not None:
            hr.append(h)
        if e is not None:
            eda.append(e)
        if rr is None:
            prev_rr = None
            continue
        if prev_rr is not None:
            diffs.append(rr - prev_rr)
        prev_rr = rr
    rmssd = math.sqrt(sum(d * d for d in diffs) / len(diffs)) if diffs else math.nan
    return {
        'mean_hr_bpm': statistics.mean(hr) if hr else math.nan,
        'rmssd_ms': rmssd,
        'median_eda_us': statistics.median(eda) if eda else math.nan,
        'valid': valid,
        'bad': bad,
    }


class LBKMonitor:
    """Tworzy LBK_Markers i odbiera LBK_Sim bez blokowania pętli klatek."""

    def __init__(self, window_seconds=5.0, report_every=1.0):
        from pylsl import (StreamInfo, StreamOutlet, StreamInlet,
                           ContinuousResolver, resolve_byprop, local_clock)
        self._clock = local_clock
        self._Inlet = StreamInlet
        self.window_seconds = window_seconds
        self.report_every = report_every
        self.records = deque()
        self.n_total = 0
        self.bad_total = 0
        self.inlet = None
        self.last_report = local_clock()

        # Strumień znaczników: 1 kanał tekstowy, nieregularny (0 Hz)
        info = StreamInfo('LBK_Markers', 'Markers', 1, 0, 'string', 'lbk-p3-markers-v1')
        self.markers = StreamOutlet(info)

        # Jednorazowe krótkie wyszukanie przed pierwszym ekranem (0,5 s)
        found = resolve_byprop('name', 'LBK_Sim', timeout=0.5)
        if found:
            self.inlet = StreamInlet(found[0], max_buflen=60)
        # Resolver w tle – sprawdzanie results() nie blokuje
        self._resolver = ContinuousResolver(prop='name', value='LBK_Sim')
        print('LBK_Sim:', 'polaczony' if self.inlet else
              'BRAK - uruchom symulator i most przed PsychoPy')

    def marker(self, value):
        """Wysyła znacznik z bieżącym czasem LSL (też przez win.callOnFlip)."""
        self.markers.push_sample([str(value)], self._clock())
        print('MARKER', value)

    def poll(self):
        """Wywoływać w Each Frame. pull_chunk(timeout=0.0) nie czeka na dane."""
        now = self._clock()
        if self.inlet is None:
            if now - self.last_report >= self.report_every:
                self.last_report = now
                found = self._resolver.results()      # nieblokujące
                if found:
                    self.inlet = self._Inlet(found[0], max_buflen=60)
                    print('LBK_Sim: polaczony')
                else:
                    print('LBK_Sim: brak strumienia')
            return

        chunk, stamps = self.inlet.pull_chunk(timeout=0.0, max_samples=128)
        for sample, stamp in zip(chunk, stamps):
            self.records.append((stamp, sample))
            self.n_total += 1
            if not is_ok(sample):
                self.bad_total += 1
        # okno kroczące: zostają próbki z ostatnich window_seconds (zegar LSL)
        while self.records and self.records[0][0] < now - self.window_seconds:
            self.records.popleft()

        if now - self.last_report >= self.report_every:
            self.last_report = now
            f = calculate_features(self.records)
            fmt = lambda v: 'NA' if not math.isfinite(v) else f'{v:.2f}'
            # Tylko konsola eksperymentatora (Runner/stdout), nie ekran uczestnika
            print(f"{self.window_seconds:.0f}s | HR= {fmt(f['mean_hr_bpm'])} bpm"
                  f" | RMSSD= {fmt(f['rmssd_ms'])} ms"
                  f" | EDA med= {fmt(f['median_eda_us'])} uS"
                  f" | valid= {f['valid']} bad_window= {f['bad']}"
                  f" bad_total= {self.bad_total}")

    def summary(self):
        """Podsumowanie na koniec eksperymentu (End Experiment)."""
        print(f'LBK_Sim: odebrano {self.n_total} probek, odrzucono '
              f'(quality != ok) {self.bad_total}')
