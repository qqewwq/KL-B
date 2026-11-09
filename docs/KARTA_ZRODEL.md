# KL-B – Karta źródeł (P3)

**Zestawienie:** DK, 2026-11-08 · **Weryfikacja i uzupełnienie:** OS, 2026-11-08.
Każdy wiersz: jakie źródło → co z niego wynika dla **naszego** kodu (plik / ustawienie).

## PsychoPy

| Źródło | Co wynika dla naszego kodu |
|---|---|
| [PsychoPy – Code Component](https://psychopy.org/builder/components/CodeComponent.html) | Kod w *Begin Experiment* wykonuje się raz → tam tworzymy `LBKMonitor` (strumień znaczników i inlet). *Each Frame* wykonuje się co klatkę → tylko szybkie `lbk.poll()` z `pull_chunk(timeout=0.0)`; nic blokującego. *End Routine* → znaczniki `stim:offset`, `resp`, `exp:start`. Kod umieszczony w osobnym module `lsl_runtime.py` importowanym z Code Component. |
| [PsychoPy – Window.callOnFlip](https://psychopy.org/api/visual/window.html) | `win.callOnFlip(lbk.marker, 'stim:onset|…')` wywołuje funkcję tuż po najbliższym `flip()`, czyli w chwili pojawienia się obrazu – dlatego `stim:onset` nie jest wysyłany bezpośrednio w *Begin Routine*. |
| [PsychoPy – Communicating with an Eyetracker](https://docs.psychopy.org/hardware/eyeTracking.html) | Wybór urządzenia w *Experiment settings → Eyetracking*; MouseGaze do testów bez sprzętu; nagrywanie włącza komponent **Eyetracker Record** (u nas `etRecord` w routine `stimulus`, 4 s). Dane trafiają do pliku HDF5 – MouseGaze nie publikuje LSL. |

## LSL

| Źródło | Co wynika dla naszego kodu |
|---|---|
| [LSL – Getting started / Quick start](https://labstreaminglayer.readthedocs.io/info/getting_started.html) | Wszystkie strumienie mają znaczniki czasu wspólnego zegara `local_clock()` → most nadaje próbkom `local_clock()` w chwili odbioru; LabRecorder zapisuje wszystkie strumienie do jednego XDF. Strumień trzeba zaznaczyć w LabRecorder **po** jego utworzeniu → `exp:start` wysyłamy dopiero po spacji (rozdz. 6.7). |
| [pylsl – repozytorium i przykłady](https://github.com/labstreaminglayer/pylsl) | `StreamInfo(name, type, n_channels, nominal_srate, format, source_id)`: `LBK_Sim` = Physio, 10 × float32, 0 Hz (nieregularny); `LBK_Markers` = Markers, 1 × string, 0 Hz. Metadane kanałów (`desc/channels/channel/label,unit`) – wykres szuka `eda_us` po etykiecie. `pull_chunk(timeout=0.0)` nie blokuje; `ContinuousResolver.results()` – nieblokujące wyszukiwanie strumienia. Na macOS pylsl potrzebuje `liblsl` zgodnej z architekturą (zmienna `PYLSL_LIB`). |
| [LabRecorder – wydania](https://github.com/labstreaminglayer/App-LabRecorder/releases) | Instalacja na Windows (archiwum z `LabRecorder.exe`); wersję wpisujemy do metryczki. Przycisk *Update* odświeża listę strumieni. |
| [pyxdf](https://github.com/xdf-modules/pyxdf) | `pyxdf.load_xdf(plik)` zwraca listę strumieni z `time_series` i `time_stamps` (już zsynchronizowanych) → `overlay/plot_xdf.py` rysuje EDA i znaczniki na jednej osi czasu. |

## EyeLogic (stanowisko LBK)

| Źródło | Co wynika dla naszego kodu |
|---|---|
| [psychopy-eyetracker-eyelogic (PyPI)](https://pypi.org/project/psychopy-eyetracker-eyelogic) oraz [katalog wtyczek PsychoPy](https://plugins.psychopy.org/directory.html) | W LBK instalujemy wtyczkę EyeLogic przez *Plugins/Packages Manager* i wybieramy ją w *Eyetracking* zamiast MouseGaze – reszta eksperymentu (Eyetracker Record) bez zmian. Wymaga działającego EyeLogic Server; wersje wtyczki i serwera wpisujemy do metryczki (rozdz. 0, 5). |

## Materiały LBK (dostęp tylko w kursie)

| Źródło | Co wynika |
|---|---|
| Protokół `Badania_EyeTracking.pptx`, slajdy 6, 8, 13, 22 | Obraz 4000 ms → szary ekran 1000 ms (niezmienne), bodźce A–D (slajd 8), SAM (slajd 13). Niespójności: 30 prób vs 4 obrazy, krzyż, SAM po bloku – rozdz. 14. |
| Strona „Badania LBK – pakiety, architektura, wspólny format” | Nazwy i typy strumieni, format znaczników `kategoria:zdarzenie|klucz=wartość`, konwencja nazw plików, pseudonimy. |
