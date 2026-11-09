#!/usr/bin/env python3
"""
Symulator strumienia danych biometrycznych – Komunikacja człowiek–komputer (lab).
Materiał autorski do zajęć. Tylko biblioteka standardowa Pythona 3.8+.

Emituje linie JSON (NDJSON) z częstotliwością --hz:
  {"t": 12.5, "seq": 125, "hr": 78.2, "rr_ms": 767, "eda_us": 3.41,
   "focus": 0.62, "quality": "ok", "scenario": "stres"}
Pola mogą mieć wartość null (utrata sygnału). "quality": ok | noisy | lost.

Tryby:
  python symulator_biosygnalow.py --mode stdout --scenario spokoj
  python symulator_biosygnalow.py --mode tcp --port 5555 --scenario mix
  python symulator_biosygnalow.py --mode file --out nagranie.jsonl --duration 120
Scenariusze: spokoj, stres, skupienie, zmeczenie, mix (sekwencja faz).
Opcje zakłóceń: --noise 0..1 (artefakty), --dropout 0..1 (utrata próbek),
                --latency-ms N (stałe opóźnienie), --jitter-ms N (losowe).
"""
import argparse, json, math, random, socket, sys, time

# Parametry docelowe dla scenariuszy: (HR [bpm], zmienność RR [ms], EDA [uS], focus [0-1])
SCEN = {
    "spokoj":    (68, 55, 2.0, 0.45),
    "stres":     (96, 18, 6.5, 0.35),
    "skupienie": (76, 35, 3.2, 0.80),
    "zmeczenie": (64, 45, 1.6, 0.20),
}
MIX = [("spokoj", 40), ("skupienie", 40), ("stres", 40), ("spokoj", 30), ("zmeczenie", 30)]


def target(scenario, t):
    if scenario != "mix":
        return scenario, SCEN[scenario]
    cycle = sum(d for _, d in MIX)
    x = t % cycle
    for name, d in MIX:
        if x < d:
            return name, SCEN[name]
        x -= d
    return MIX[-1][0], SCEN[MIX[-1][0]]


def generator(args):
    rnd = random.Random(args.seed)
    hr, eda, focus = 70.0, 2.5, 0.5
    seq, t0 = 0, time.time()
    dt = 1.0 / args.hz
    while True:
        t = seq * dt
        if args.duration and t > args.duration:
            return
        name, (hr_t, rrv, eda_t, foc_t) = target(args.scenario, t)
        a = 1 - math.exp(-dt / 8.0)            # wolna adaptacja fizjologii (~8 s)
        hr += a * (hr_t - hr) + rnd.gauss(0, 0.4)
        eda += a * (eda_t - eda) + rnd.gauss(0, 0.02)
        if rnd.random() < 0.01 * dt * 10:      # odpowiedź fazowa EDA (SCR)
            eda += rnd.uniform(0.2, 0.8)
        focus += a * (foc_t - focus) + rnd.gauss(0, 0.03)
        focus = min(1.0, max(0.0, focus))
        rr = 60000.0 / hr + rnd.gauss(0, rrv / 2)
        quality = "ok"
        rec = {"t": round(t, 2), "seq": seq, "hr": round(hr, 1), "rr_ms": int(rr),
               "eda_us": round(eda, 2), "focus": round(focus, 2)}
        if rnd.random() < args.noise * 0.2:    # artefakt ruchowy
            quality = "noisy"
            rec["hr"] = round(hr + rnd.choice([-1, 1]) * rnd.uniform(25, 60), 1)
            rec["eda_us"] = round(eda + rnd.uniform(1.5, 4.0), 2)
        if rnd.random() < args.dropout * 0.2:  # utrata kontaktu z czujnikiem
            quality = "lost"
            rec.update({"hr": None, "rr_ms": None, "eda_us": None, "focus": None})
        rec["quality"] = quality
        rec["scenario"] = name                 # etykieta "prawdy" – do ewaluacji, nie do sterowania!
        delay = args.latency_ms / 1000 + (rnd.uniform(0, args.jitter_ms) / 1000 if args.jitter_ms else 0)
        if args.mode != "file":
            wait = t0 + t + delay - time.time()
            if wait > 0:
                time.sleep(wait)
        seq += 1
        yield json.dumps(rec, ensure_ascii=False)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=["stdout", "tcp", "file"], default="stdout")
    p.add_argument("--scenario", choices=list(SCEN) + ["mix"], default="mix")
    p.add_argument("--hz", type=float, default=4.0)
    p.add_argument("--duration", type=float, default=0, help="sekundy; 0 = bez końca")
    p.add_argument("--noise", type=float, default=0.1)
    p.add_argument("--dropout", type=float, default=0.05)
    p.add_argument("--latency-ms", type=float, default=0)
    p.add_argument("--jitter-ms", type=float, default=0)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--port", type=int, default=5555)
    p.add_argument("--out", default="nagranie.jsonl")
    args = p.parse_args()

    if args.mode == "stdout":
        for line in generator(args):
            print(line, flush=True)
    elif args.mode == "file":
        if not args.duration:
            args.duration = 120
        with open(args.out, "w", encoding="utf-8") as f:
            for line in generator(args):
                f.write(line + "\n")
        print(f"Zapisano {args.out}", file=sys.stderr)
    else:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", args.port))
        srv.listen(1)
        print(f"Czekam na klienta na 127.0.0.1:{args.port} ...", file=sys.stderr)
        while True:
            conn, addr = srv.accept()
            print(f"Połączono: {addr}", file=sys.stderr)
            try:
                for line in generator(args):
                    conn.sendall((line + "\n").encode("utf-8"))
            except (BrokenPipeError, ConnectionResetError):
                print("Klient rozłączony.", file=sys.stderr)
            finally:
                conn.close()


if __name__ == "__main__":
    main()
