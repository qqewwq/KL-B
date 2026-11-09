# BUILD BOOK – P3 „Obraz, ocena, pobudzenie”

**Etap:** KL-A + KL-B · **Ostatnia aktualizacja:** 2026-11-08 · **Tag repozytorium:** `KL-B`
**Rozdziały w tej wersji:** 0, 1 (KL-A), **3, 4, 6 (KL-B)**, 14, 15.

**Czytelnik docelowy:** osoba znająca Pythona, ale nie PsychoPy, LSL ani tego projektu, przy czystym komputerze z Windows (stanowisko LBK). Polecenia podajemy w dwóch wariantach: **Windows** (`py -3 …`, PowerShell) i **macOS** (`python3 …`, Terminal). Wszystkie polecenia uruchamiamy **z katalogu głównego repozytorium** (tam, gdzie leży ten plik).

**Oznaczenia autorów:** DK – Diana Kalinina, OS – Oleksandr Shamak. Przy każdym kroku: **wykonanie** – kto zrobił dany krok na komputerze; **opis** – kto napisał i zredagował opis kroku w Build Booku; data.

---

## 0. Metryczka

| Pole | Wartość |
|---|---|
| Pakiet | P3 – Obraz, ocena, pobudzenie |
| Badanie budowane w KL-B | główne: „Qualia, barwa i subiektywne doświadczenie” |
| Badanie drugie | „Reklama spod ręki człowieka czy algorytmu?” (poza KL-B) |
| Protokół | `Badania_EyeTracking.pptx` z folderu kursu „Pakiet P3 – materiały badań LBK” (pobrany 2026-11-08; slajdy 6, 8, 13, 22). Plik **nie** jest w repozytorium – pobiera się go z kursu. |
| Zespół | DK – Diana Kalinina, OS – Oleksandr Shamak |
| Repozytorium | [adres prywatnego repozytorium] · tagi `KL-A`, `KL-B` |
| Komputer testowy | MacBook Air, Apple Silicon, macOS 27 (najnowsza wersja, listopad 2026) |
| PsychoPy | Standalone **2025.2.4** (okno pokazuje `v2025.2.4beta`), Python 3.10.11, uruchamiany przez Rosetta 2 |
| Python poza PsychoPy | `.venv` z Pythonem 3.9 (most, testy, wykres) |
| pylsl / liblsl | pylsl **1.18.2** w `.venv`; universal liblsl x86_64/arm64 w `/Library/Frameworks/lsl.framework/Versions/A/lsl` dla PsychoPy (zmienna `PYLSL_LIB`) |
| LabRecorder | **1.18.0** (macOS, Homebrew) |
| pyxdf, matplotlib | w `.venv` (wersje: `.venv/bin/python -m pip show pyxdf matplotlib`) |
| Ekran w eksperymencie | okno 1920×1080 px, jednostki `pix`, monitor `testMonitor` (tymczasowo); częstotliwość odświeżania i wymiary monitora LBK – do wpisania na stanowisku |
| Aparatura LBK | EyeLogic (wzrok), GSR/EDA; wersje sterowników i nazwy strumieni – do wpisania na sesji w LBK (pyt. 14.4) |

**Jak sprawdzić:** PsychoPy → *Help → About* pokazuje tę samą wersję; w repozytorium istnieje tag `KL-B`.

---

## 1. Instalacja od zera

> Rozdział z KL-A (instalacja PsychoPy, demo, symulator). Instalacja pylsl i LabRecorder potrzebna w KL-B jest w kroku **6.1**.

### Krok 1.1 – Instalacja PsychoPy · autor: DK · 2026-10-12

- **Cel:** zainstalować PsychoPy w wersji uzgodnionej w zespole.
- **Gdzie:** https://www.psychopy.org/download.html → wersja Standalone **2025.2.4**. Windows: instalator `.exe`, domyślna ścieżka. macOS: `StandalonePsychoPy-2025.2.4-macOS-3.10.dmg` → przeciągnąć do `/Applications`; przy pierwszym uruchomieniu zgodzić się na instalację Rosetta 2.
- **Jak sprawdzić:** PsychoPy otwiera okna Builder, Coder i Runner bez komunikatu o błędzie; *Help → About* pokazuje 2025.2.4.
- **Typowe problemy:** wersja 2026.x na macOS zgłaszała `wx._core.wxAssertionError` (locale) – zainstalować 2025.2.4. Przy `Launch error (py2app)` sprawdzić `~/.psychopy3/last_app_load.log`.
- **Zrzut:** `docs/img/1-1-psychopy.png`

### Krok 1.2 – Test demo · autor: DK · 2026-10-12

- **Cel:** sprawdzić, że PsychoPy wyświetla bodźce.
- **Gdzie:** Coder → *Demos → basic → hello_world.py* → **Run**.
- **Jak sprawdzić:** otwiera się okno z napisami `Hello world!` i `¡Hola mundo!`.
- **Zrzut:** `docs/img/1-2-demo.png`

### Krok 1.3 – Symulator biosygnałów · autor: DK · 2026-10-12

- **Cel:** sprawdzić symulator, który na własnym komputerze zastępuje czujniki LBK.
- **Gdzie:** `simulator/symulator_biosygnalow.py` (z archiwum kursu „Kod do laboratorium – symulator i klient startowy”; tylko biblioteka standardowa Pythona 3.8+).
- **Polecenie testowe:** Windows `py -3 simulator/symulator_biosygnalow.py --mode stdout --scenario stres --duration 5` · macOS `python3 simulator/symulator_biosygnalow.py --mode stdout --scenario stres --duration 5`
- **Jak sprawdzić:** w konsoli pojawiają się linie JSON co 0,25 s (4 Hz) z polami `t, seq, hr, rr_ms, eda_us, focus, quality, scenario`; część linii ma `quality="noisy"` lub `"lost"` (przy `lost` pola sygnałów mają wartość `null`).

| Pole | Znaczenie | Jednostka |
|---|---|---|
| `t` | czas od startu symulacji | s |
| `seq` | numer próbki | – |
| `hr` | tętno | bpm |
| `rr_ms` | odstęp R–R | ms |
| `eda_us` | przewodnictwo skóry | µS |
| `focus` | umowny wskaźnik „skupienia” (nie jest pomiarem wzroku) | 0–1 |
| `quality` | jakość próbki | `ok` / `noisy` / `lost` |
| `scenario` | etykieta „prawdy” symulatora – **nie wolno** jej używać do sterowania | tekst |

Symulator **nie** wysyła `gaze_x`, `gaze_y`, `gaze_valid`, `pupil_mm`, `resp`.

---

## 3. Budowa eksperymentu krok po kroku (KL-B)

**Wynik końcowy rozdziału:** plik `experiment/P3_KL_B.psyexp` – instrukcja → pętla 4 prób z pliku CSV (krzyż 0,5 s → obraz 4 s → szary ekran 1 s) → jedno pytanie 1–9 → koniec, z MouseGaze, Eyetracker Record i integracją LSL.
**Gotowy plik jest w repozytorium** – wystarczy go otworzyć (krok 3.1). Kroki 3.2–3.12 opisują każde ustawienie tak, żeby dało się go odtworzyć ręcznie w pustym Builderze albo sprawdzić, czy nic się nie zmieniło.

**Przebieg czasowy jednej próby** (przy 60 Hz):

| Element | Czas | Klatki przy 60 Hz | Źródło |
|---|---|---|---|
| krzyż fiksacyjny | 500 ms | 30 | **roboczo** – protokół go nie określa (pyt. 14.6) |
| obraz | 4000 ms | 240 | protokół P3 (niezmienny) |
| szary ekran | 1000 ms | 60 | protokół P3 (niezmienny) |

Czasy w Builderze są ustawione w sekundach (`duration (s)`); pomiar dokładności w klatkach – rozdział 9 (KL-E).

### Krok 3.1 – Otwarcie eksperymentu i Flow · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** otworzyć szkielet badania i zobaczyć kolejność ekranów.
- **Gdzie:** PsychoPy → Builder → *File → Open* → `experiment/P3_KL_B.psyexp`.
- **Ustawienia (Flow, od lewej):** `intro` → pętla `trials` wokół `fixation` → `stimulus` → `gray` → `rating` → `end`. Pętla obejmuje **tylko** trzy środkowe routines; `rating` jest **po** pętli (jedno pytanie po bloku).
- **Zrzut:** `docs/img/3-1-flow.png`
- **Jak sprawdzić:** widać 6 zakładek routines (`intro, fixation, stimulus, gray, rating, end`) i pętlę `trials` z czasami 0.50 s, 4.00 s, 1.00 s.
- **Typowe problemy:** ostrzeżenie o innej wersji pliku – plik zapisano w formacie 2025.x; otwierać w PsychoPy 2025.2.4.

### Krok 3.2 – Ustawienia eksperymentu (Basic, Screen, Data) · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** ustawić okno, jednostki i dane wyjściowe zgodnie z konwencją LBK.
- **Gdzie:** Builder → ikona zębatki (*Experiment settings*).
- **Ustawienia:**

| Zakładka | Pole | Wartość |
|---|---|---|
| Basic | Experiment name | `P3_KL_B` |
| Basic | Experiment info | `{'participant':'TEST-01','session':'S001'}` – **tylko pseudonim**, nigdy imię i nazwisko |
| Basic | Show info dialog | włączone |
| Screen | Window size | `[1920, 1080]` |
| Screen | Full-screen | wyłączone na komputerze testowym; **na stanowisku LBK włączyć** |
| Screen | Units | `pix` |
| Screen | Monitor | `testMonitor` (tymczasowo; na LBK – profil z Monitor Center) |
| Screen | Background | `black` |
| Data | Data filename | `u'data' + os.sep + 'P3_glowne_%s_%s_%s' % (expInfo['participant'], expInfo['session'], data.getDateStr(format='%Y-%m-%d_%H%M'))` |
| Data | Save csv / excel / psydat / log / hdf5 | włączone |

- **Zrzut:** — (wszystkie wartości w tabeli powyżej; zakładka *Eyetracking* – `docs/img/3-3-mousegaze.png`).
- **Jak sprawdzić:** po przebiegu w `experiment/data/` powstaje m.in. `P3_glowne_TEST-01_S001_2026-11-08_1720.csv` (format `{pakiet}_{badanie}_{kod}_{sesja}_{RRRR-MM-DD_GGMM}`).
- **Typowe problemy:** na laptopie z ekranem mniejszym niż 1920×1080 okno wychodzi poza ekran i PsychoPy pokazuje `dropped frames` – to dopuszczalne w teście technicznym, nie na stanowisku LBK.

### Krok 3.3 – Eyetracking: MouseGaze · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** symulować wzrok myszą; w LBK zmienia się tylko to jedno ustawienie na EyeLogic.
- **Gdzie:** Experiment settings → zakładka **Eyetracking**.
- **Ustawienia:** `Eyetracker device = MouseGaze`; `Move button = CONTINUOUS`; `Blink button = MIDDLE_BUTTON`; `Saccade threshold = 0.5`.
- **Zrzut:** `docs/img/3-3-mousegaze.png`
- **Jak sprawdzić:** po przebiegu w `experiment/data/` jest plik `.hdf5` z próbkami pozycji myszy z czasu wyświetlania obrazów.
- **Typowe problemy:** MouseGaze zapisuje dane lokalnie (HDF5) i **nie tworzy strumienia LSL** – w LabRecorder są tylko 2 strumienie.

### Krok 3.4 – Routine `intro` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** instrukcja; uruchomienie LSL; znacznik `exp:start` po naciśnięciu spacji.
- **Gdzie:** zakładka routine `intro`. Komponenty (kolejność od góry): `lsl_intro` (Code), `instrukcja` (Text), `start_key` (Keyboard).
- **Ustawienia:**
  - `instrukcja`: start 0 s, czas pusty (do końca routine), wysokość 38 px, wrap 1500 px, font Arial, kolor white. Tekst (Enter = nowa linia):
    *Za chwilę zobaczysz kilka obrazów. / Oglądaj je swobodnie. / Po obejrzeniu wszystkich obrazów ocenisz, jak silne pobudzenie odczuwałaś/odczuwałeś (skala 1–9). / Naciśnij SPACJĘ, aby rozpocząć.*
  - `start_key`: Allowed keys `'space'`, Force end of Routine ✔, Store `last key`.
  - `lsl_intro` (Code Type `Py`):

```python
# --- Begin Experiment ---
# Importuje moduł z experiment/lsl_runtime.py (ten sam katalog co .psyexp).
# Tworzy strumień LBK_Markers i łączy się z LBK_Sim (most musi już działać).
from lsl_runtime import LBKMonitor
lbk = LBKMonitor(window_seconds=5.0)

# --- Each Frame ---
lbk.poll()          # odbiór LBK_Sim bez blokowania + raport co 1 s w konsoli

# --- End Routine ---
# exp:start dopiero po spacji – eksperymentator zdąży włączyć LabRecorder na ekranie instrukcji
lbk.marker('exp:start|study=P3|list=L1_LBK_4obrazy_test|session=' + str(expInfo['session']))
```

- **Zrzut:** `docs/img/3-1-flow.png` (widok routine `intro`).
- **Jak sprawdzić:** w konsoli Runnera najpierw `LBK_Sim: polaczony`, a po spacji `MARKER exp:start|study=P3|…`.
- **Typowe problemy:** `LBK_Sim: BRAK - uruchom symulator i most przed PsychoPy` – patrz 6.4. `ModuleNotFoundError: lsl_runtime` – plik `lsl_runtime.py` musi leżeć obok `.psyexp`. **Instrukcja pokazuje dosłowne `\n`** – w polu tekstu nowe linie wpisuje się Enterem, nie znakami `\n` (błąd z wersji z 2026-11-08, poprawiony – rozdz. 15).

### Krok 3.5 – Pętla `trials` z pliku warunków · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** jedna pętla prezentuje wszystkie próby bloku w kolejności z pliku CSV.
- **Gdzie:** Flow → *Insert Loop* – początek przed `fixation`, koniec za `gray`.
- **Ustawienia:** Name `trials`; loopType `sequential`; nReps `1`; Conditions `conditions/L1_LBK_4obrazy_test.csv` (ścieżka względem `.psyexp`); Selected rows – puste; random seed – puste; Is trials ✔.
- **Zrzut:** `docs/img/3-1-flow.png` (pętla `trials` na Flow; ustawienia pętli – lista powyżej).
- **Jak sprawdzić:** okno pętli pokazuje *4 conditions, with 7 parameters [trial_id, stimulus_id, image_file, block, condition, stim_width, stim_height]*; wynikowy CSV ma 4 wiersze prób, `stimulus_id` w kolejności A, B, C, D.
- **Typowe problemy:** „Could not find conditions file” – ścieżka liczona od katalogu `experiment/`.

### Krok 3.6 – Routine `fixation` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** krzyż przed obrazem i znacznik początku próby.
- **Gdzie:** routine `fixation`: `lsl_fix` (Code), `krzyzyk` (Text).
- **Ustawienia:** `krzyzyk`: tekst `+`, start 0 s, czas **0.5 s**, wysokość 80 px, pos (0,0), white.

```python
# lsl_fix – Begin Routine: początek próby (trial_id z pliku warunków)
lbk.marker('trial:start|trial=' + str(trial_id))
# lsl_fix – Each Frame
lbk.poll()
```

- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w konsoli `MARKER trial:start|trial=1` … `trial=4`.

### Krok 3.7 – Routine `stimulus`: obraz, Eyetracker Record, `stim:onset` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** pokazać obraz z protokołu przez 4 s, nagrywać wzrok i wysłać znacznik dokładnie w chwili pojawienia się obrazu.
- **Gdzie:** routine `stimulus`: `lsl_stim` (Code), `obraz` (Image), `etRecord` (Eyetracker Record – w panelu *Components → Eyetracking*).
- **Ustawienia:**
  - `obraz`: Image `$image_file` (*set every repeat*); Size `$[stim_width, stim_height]` (*set every repeat*) – obrazy w natywnym rozmiarze, bez skalowania; pos (0,0); start 0 s; czas **4.0 s**.
  - `etRecord`: Action `Start and Stop`; start 0 s; czas **4.0 s**.
  - `lsl_stim`:

```python
# --- Begin Routine ---
# callOnFlip: znacznik zostanie wysłany w chwili odświeżenia ekranu,
# na którym obraz pojawia się po raz pierwszy (nie w chwili wejścia w routine).
win.callOnFlip(lbk.marker, 'stim:onset|stim=' + str(stimulus_id))
# --- Each Frame ---
lbk.poll()
# --- End Routine ---
lbk.marker('stim:offset|stim=' + str(stimulus_id))
```

- **Zrzut:** `docs/img/3-7-stimulus.png`
- **Jak sprawdzić:** każdy z 4 obrazów widać ok. 4 s; w XDF odstęp `stim:onset` → `stim:offset` wynosi ok. 3,96–3,98 s (zmierzone 2026-11-08: 3,957 / 3,973 / 3,976 / 3,979 s; ~40 ms różnicy względem 4,000 s to moment wysłania `stim:offset` w End Routine – dokładny pomiar w KL-E).
- **Typowe problemy:** `Could not find image` – ścieżki w CSV są względne względem `experiment/`, nazwy plików zawierają spację (`Bodziec A.PNG`) i wielkie litery rozszerzenia – na Windows bez znaczenia, na macOS/Linux wielkość liter musi się zgadzać.

### Krok 3.8 – Routine `gray` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** szary ekran 1 s po obrazie (z protokołu).
- **Gdzie:** routine `gray` → *Routine settings*: kolor tła `0` (rgb, szary); komponent `szary_ekran` (Text, tekst = spacja, start 0 s, czas **1.0 s** – wyznacza długość routine); `lsl_gray` (Each Frame: `lbk.poll()`).
- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w XDF odstęp `stim:offset` → następny `trial:start` = 1,00 s.
- **Uwaga:** to jest miejsce na przyszłą adaptację (KL-D: dłuższa przerwa / ekran neutralny). Czasów obrazu i szarego ekranu nie wolno zmieniać.

### Krok 3.9 – Routine `rating`: jedno pytanie po bloku · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** jedna odpowiedź uczestnika (robocza ocena pobudzenia 1–9).
- **Gdzie:** routine `rating`: `lsl_rating` (Code), `pytanie` (Text), `rating_resp` (Keyboard).
- **Ustawienia:** `pytanie`: wysokość 37 px, tekst *Jak silne pobudzenie odczuwałaś/odczuwałeś podczas oglądania obrazów? / 1 = bardzo słabe … 9 = bardzo silne / Naciśnij klawisz od 1 do 9.*; `rating_resp`: Allowed keys `'1','2','3','4','5','6','7','8','9'`, Force end ✔, Store `last key`.

```python
# lsl_rating – Each Frame
lbk.poll()
# lsl_rating – End Routine: znacznik odpowiedzi z klawiszem i czasem reakcji [s]
if rating_resp.keys:
    rt_value = rating_resp.rt if rating_resp.rt is not None else -1.0
    lbk.marker('resp|q=SAM_AROUSAL_ROBOCZE|key=' + str(rating_resp.keys)
               + '|rt=' + str(round(float(rt_value), 3)))
```

- **Zrzut:** — (widok w `docs/img/3-1-flow.png`).
- **Jak sprawdzić:** w CSV kolumny `rating_resp.keys` i `rating_resp.rt`; w XDF `resp|q=SAM_AROUSAL_ROBOCZE|key=…|rt=…`.
- **Odstępstwo:** to **nie** jest pełna ankieta SAM (walencja, pobudzenie, dominacja, slajd 13). Wersja robocza do czasu decyzji LBK (pyt. 14.6).

### Krok 3.10 – Routine `end` · wykonanie: DK · opis: OS · 2026-11-08

- **Gdzie:** routine `end`: `koniec` (Text „Dziękujemy! To już koniec.”, 42 px, start 0 s, czas **2 s**), `lsl_end` (Code).

```python
# lsl_end – Begin Routine
lbk.marker('exp:end')
# lsl_end – Each Frame
lbk.poll()
# lsl_end – End Experiment: podsumowanie odebranych i odrzuconych próbek
lbk.summary()
```

- **Jak sprawdzić:** ostatnie linie konsoli: `MARKER exp:end` i `LBK_Sim: odebrano N probek, odrzucono (quality != ok) M`.

### Krok 3.11 – Moduł `experiment/lsl_runtime.py` · kod: DK, poprawki: OS · opis: OS · 2026-11-08

- **Cel:** cała logika LSL w jednym pliku Pythona zamiast w polach Code Components.
- **Gdzie:** `experiment/lsl_runtime.py` (obok `.psyexp`; Builder importuje go w kroku 3.4).
- **Zawartość:**

| Element | Co robi |
|---|---|
| `LBKMonitor.__init__` | tworzy `LBK_Markers` (Markers, 1 kanał string, 0 Hz); szuka `LBK_Sim` przez 0,5 s; uruchamia `ContinuousResolver` do nieblokującego ponownego połączenia |
| `marker(tekst)` | `push_sample([tekst], local_clock())` + wydruk `MARKER …` |
| `poll()` | w każdej klatce: `pull_chunk(timeout=0.0, max_samples=128)`, dopisanie próbek do okna, usunięcie starszych niż 5 s (zegar LSL), co 1 s wydruk cech |
| `calculate_features()` | średnie HR, RMSSD, mediana EDA z próbek `quality = ok`; liczba poprawnych i odrzuconych |
| `summary()` | podsumowanie na końcu |

- **Jak sprawdzić:** test jednostkowy (bez LSL i PsychoPy): Windows `py -3 tests/test_features.py` · macOS `python3 tests/test_features.py` → `OK: HR, RMSSD z sasiednich roznic RR, mediana EDA, odrzucenie noisy/lost/NaN`.

### Krok 3.12 – Dane wyjściowe PsychoPy · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** wiedzieć, jakie pliki powstają po jednym przebiegu.
- **Gdzie:** `experiment/data/` (katalog jest w `.gitignore` – danych z sesji nie wrzucamy do repozytorium).
- **Pliki:** `P3_glowne_<kod>_<sesja>_<data>.csv` (jedna linia = jedna próba + wiersz odpowiedzi), `.xlsx`, `.psydat`, `.log`, `.hdf5` (MouseGaze). Kluczowe kolumny CSV: `trial_id`, `stimulus_id`, `image_file`, `condition`, `obraz.started`, `obraz.stopped`, `rating_resp.keys`, `rating_resp.rt`, `participant`, `session`.
- **Zrzut:** — (lista plików powyżej).
- **Jak sprawdzić:** CSV ma 4 wiersze z `trial_id` = 1–4 i jeden wiersz z `rating_resp.keys`.

**Sprawdzenie rozdziału 3 (jak poznać, że działa):** przy działającym symulatorze i moście (6.4) uruchom eksperyment z `participant=TEST-01`, `session=S001`. Oczekiwane: 4 obrazy A–D po 4 s z szarym ekranem 1 s, jedno pytanie 1–9, ekran końcowy; w konsoli co ~1 s linia `5s | HR= … bpm | RMSSD= … ms | EDA med= … uS | valid= … bad_window= … bad_total= …` oraz kolejno znaczniki: `exp:start`, 4 × (`trial:start`, `stim:onset`, `stim:offset`), `resp`, `exp:end`; w `experiment/data/` pliki z kroku 3.12.

---

## 4. Pliki warunków, listy, randomizacja (KL-B)

### Krok 4.1 – Plik warunków bloku testowego · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** oddzielić listę bodźców i ich parametry od konfiguracji Buildera.
- **Gdzie:** `experiment/conditions/L1_LBK_4obrazy_test.csv` (UTF-8, separator przecinek, pierwszy wiersz = nagłówki); czyta go pętla `trials` (krok 3.5).
- **Kolumny:**

| Kolumna | Typ | Znaczenie | Przykład |
|---|---|---|---|
| `trial_id` | int | numer próby w bloku (trafia do znacznika `trial:start`) | `1` |
| `stimulus_id` | tekst | kod bodźca (trafia do `stim:onset`/`stim:offset`) | `BODZIEC_A` |
| `image_file` | tekst | ścieżka do obrazu względem `experiment/` | `stimuli/Bodziec A.PNG` |
| `block` | int | numer bloku | `1` |
| `condition` | tekst | kategoria obrazu (treść × barwa) – roboczy opis zespołu | `pejzaz_ciepla` |
| `stim_width` | int, px | szerokość wyświetlania = natywna szerokość pliku | `716` |
| `stim_height` | int, px | wysokość wyświetlania = natywna wysokość pliku | `476` |

- **Pełna zawartość pliku:**

```csv
trial_id,stimulus_id,image_file,block,condition,stim_width,stim_height
1,BODZIEC_A,stimuli/Bodziec A.PNG,1,pejzaz_ciepla,716,476
2,BODZIEC_B,stimuli/Bodziec B.PNG,1,pejzaz_zimna,715,477
3,BODZIEC_C,stimuli/Bodziec C.PNG,1,twarz_ciepla,594,476
4,BODZIEC_D,stimuli/Bodziec D.PNG,1,twarz_zimna,595,476
```

- **Zrzut:** — (pełna zawartość pliku powyżej).
- **Jak sprawdzić:** patrz 4.3.
- **Typowe problemy:** Excel przy zapisie potrafi zmienić separator na średnik i kodowanie – edytować w edytorze tekstu albo zapisać jako „CSV UTF-8 (rozdzielany przecinkami)”.

### Krok 4.2 – Bodźce · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** użyć oryginalnych obrazów z pakietu P3.
- **Gdzie:** `experiment/stimuli/Bodziec A.PNG` … `Bodziec D.PNG` – skopiowane 1:1 z folderu kursu „Pakiet P3 – materiały badań LBK” (slajd 8 protokołu). PNG RGBA: A 716×476, B 715×477, C 594×476, D 595×476 px.
- **Zasada:** materiały LBK tylko w **prywatnym** repozytorium. Jeśli repozytorium miałoby być publiczne – usunąć `experiment/stimuli/Bodziec*.PNG` i pobrać je z kursu do tego samego folderu.
- **Jak sprawdzić:** 4.3.

### Krok 4.3 – Kontrola spójności pliku warunków · wykonanie i opis: OS · 2026-11-08

- **Cel:** przed uruchomieniem sprawdzić, że każdy plik istnieje i ma rozmiar zgodny z CSV.
- **Polecenie** (wymaga Pillow: `py -3 -m pip install pillow` / `python3 -m pip install pillow`):

```bash
python3 -c "import csv;from PIL import Image;r=list(csv.DictReader(open('experiment/conditions/L1_LBK_4obrazy_test.csv',encoding='utf-8')));[print(x['trial_id'],x['image_file'],Image.open('experiment/'+x['image_file']).size==(int(x['stim_width']),int(x['stim_height']))) for x in r];print(len(r),'wierszy')"
```

  (Windows: zamienić `python3` na `py -3`.)
- **Jak sprawdzić:** 4 linie zakończone `True` i `4 wierszy`.

### Krok 4.4 – Wybór listy, kolejność, ziarno · wykonanie: DK · opis: OS · 2026-11-08

- **Stan KL-B:** jedna lista `L1_LBK_4obrazy_test`, kolejność **stała** A → B → C → D (`sequential`), **bez losowania i bez ziarna**. To kolejność techniczna, nie zatwierdzony plan badania.
- **Dlaczego nie więcej:** protokół (slajd 6) wspomina 30 prób, a w materiałach są 4 obrazy; liczby prób i kontrbalansowania nie ustalamy sami (pyt. 14.1). Prowadzący (e-mail) potwierdził, że w KL-B wystarcza jeden blok z oryginalnymi bodźcami.
- **Plan po decyzji LBK (M2):** pliki `L1…Ln` w `experiment/conditions/`, wybór listy w oknie startowym (pole `list` w *Experiment info*, Conditions = `$'conditions/' + expInfo['list'] + '.csv'`), skrypt generujący listy z zapisanym ziarnem w rozdziale 4.
- **Jak sprawdzić:** znacznik `exp:start` zawiera `list=L1_LBK_4obrazy_test`.

**Sprawdzenie rozdziału 4:** polecenie z 4.3 zwraca 4 × `True`; po przebiegu kolumna `stimulus_id` w CSV wyników ma kolejność BODZIEC_A, B, C, D.

---

## 6. LSL i GSR (KL-B)

**Architektura na własnym komputerze:** `symulator (TCP 127.0.0.1:5555, NDJSON 4 Hz)` → `lsl/sim_to_lsl.py` → strumień **LBK_Sim** → PsychoPy (odbiór, okno 5 s) + PsychoPy wysyła **LBK_Markers** → **LabRecorder** zapisuje oba do jednego XDF. W LBK zamiast symulatora i mostu jest strumień urządzenia GSR/EDA (krok 6.10).

### Krok 6.1 – Instalacja pylsl i LabRecorder · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** biblioteka LSL w dwóch środowiskach (Python terminalowy dla mostu i Python wbudowany w PsychoPy) oraz program do nagrywania.
- **Ustawienia / czynności:**
  1. **Python terminalowy (most, testy, wykres).** Windows: `py -3 -m pip install pylsl pyxdf matplotlib`. macOS (zalecane środowisko wirtualne):
     ```bash
     python3 -m venv .venv
     .venv/bin/python -m pip install pylsl -r overlay/requirements.txt
     ```
  2. **PsychoPy:** *Tools → Plugins/Packages Manager → zakładka Packages* → wpisać `pylsl` → *Install* → zrestartować PsychoPy. Sprawdzenie: Coder → *Shell* → `import pylsl; print(pylsl.__version__)`.
  3. **LabRecorder:** Windows – pobrać archiwum z https://github.com/labstreaminglayer/App-LabRecorder/releases, rozpakować, uruchomić `LabRecorder.exe`. macOS – `brew install labstreaminglayer/tap/labrecorder` (zainstalowano 1.18.0). Wersję wpisać do metryczki.
- **macOS + PsychoPy przez Rosetta (tylko Mac):** pylsl w PsychoPy (x86_64) potrzebuje universal `liblsl`. Zainstalowano `lsl.framework` w `/Library/Frameworks/` i uruchamiano PsychoPy z Terminala ze zmienną:
  ```bash
  PYLSL_LIB=/Library/Frameworks/lsl.framework/Versions/A/lsl /Applications/PsychoPy.app/Contents/MacOS/PsychoPy
  ```
  (`open -a` nie przekazuje zmiennych środowiskowych – trzeba uruchomić plik binarny jak wyżej.)
- **Jak sprawdzić:** `import pylsl` działa w obu środowiskach bez błędu; LabRecorder się otwiera.
- **Typowe problemy:** `RuntimeError: LSL binary library file was not found` – brak lub zła architektura `liblsl` (patrz wyżej). Menedżer pakietów PsychoPy na macOS zgłaszał `TypeError: NoneType`, mimo że pakiet był już dostępny – sprawdzać przez `import pylsl` w Shell.

### Krok 6.2 – Strumienie LSL · wykonanie: DK · opis: OS · 2026-11-08

| Strumień | Typ | Kanały | Format | Częstotliwość | source_id | Kto wysyła |
|---|---|---|---|---|---|---|
| `LBK_Sim` | `Physio` | 10 (tabela niżej) | float32 | 0 (nieregularny; faktycznie ~4 Hz) | `lbk-p3-sim-v1` | `lsl/sim_to_lsl.py` |
| `LBK_Markers` | `Markers` | 1 | string | 0 (nieregularny) | `lbk-p3-markers-v1` | PsychoPy (`lsl_runtime.py`) |
| GSR/EDA LBK | [do odczytu w LabRecorder w LBK] | | | | | urządzenie LBK |
| EyeLogic (jeśli jest) | [do odczytu w LBK] | | | | | EyeLogic Server |

**Kanały `LBK_Sim` (kolejność stała, zapisana też w metadanych strumienia):**

| # | Kanał | Jednostka | Uwagi |
|---|---|---|---|
| 0 | `hr` | bpm | |
| 1 | `eda_us` | µS | |
| 2 | `rr_ms` | ms | |
| 3 | `focus` | a.u. 0–1 | sztuczny wskaźnik symulatora |
| 4 | `quality` | kod | `0=ok`, `1=noisy`, `2=lost`, brak pola = `NaN` |
| 5–6 | `gaze_x`, `gaze_y` | px | symulator ich nie wysyła → zawsze `NaN` |
| 7 | `gaze_valid` | 0/1 | → `NaN` |
| 8 | `pupil_mm` | mm | → `NaN` |
| 9 | `resp` | a.u. | → `NaN` |

- **Znacznik czasu:** most nadaje każdej próbce `local_clock()` w chwili odebrania linii z TCP (pole `t` symulatora nie jest używane jako czas).
- **Jak sprawdzić:** LabRecorder → *Update* pokazuje `LBK_Sim (<nazwa komputera>)` i – po starcie PsychoPy – `LBK_Markers (<nazwa komputera>)`.

### Krok 6.3 – Słownik znaczników · wykonanie: DK · opis: OS · 2026-11-08

Format LBK: `kategoria:zdarzenie|klucz=wartość|…`

| Znacznik | Kiedy jest wysyłany | Gdzie w kodzie |
|---|---|---|
| `exp:start\|study=P3\|list=L1_LBK_4obrazy_test\|session=S001` | naciśnięcie spacji na ekranie instrukcji (początek części właściwej) | `lsl_intro`, End Routine |
| `trial:start\|trial=N` | początek routine `fixation` (N = `trial_id`) | `lsl_fix`, Begin Routine |
| `stim:onset\|stim=ID` | pierwsze odświeżenie ekranu z obrazem (`win.callOnFlip`) | `lsl_stim`, Begin Routine |
| `stim:offset\|stim=ID` | koniec routine `stimulus` | `lsl_stim`, End Routine |
| `resp\|q=SAM_AROUSAL_ROBOCZE\|key=K\|rt=S` | po naciśnięciu klawisza 1–9 (`rt` w sekundach, 3 miejsca) | `lsl_rating`, End Routine |
| `exp:end` | początek ekranu końcowego | `lsl_end`, Begin Routine |

Zarezerwowane na kolejne karty (nie są jeszcze wysyłane): `block:start|block=N`, `state:…`, `adaptation:…|rule=…`, `artifact:tracking_loss`, `calib:end|err_deg=…`.

- **Jak sprawdzić:** po wczytaniu XDF (6.8) lista znaczników zawiera wszystkie 6 typów w kolejności z tabeli; skrypt wykresu wypisze `UWAGA: brak wymaganych znacznikow`, jeśli któregoś z `exp:start, trial:start, stim:onset, resp, exp:end` brakuje.

### Krok 6.4 – Symulator i most `sim_to_lsl.py` · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** publikować dane symulatora jako `LBK_Sim`.
- **Gdzie:** dwa osobne okna terminala (PowerShell / Terminal), oba w katalogu głównym repozytorium. Kolejność: **najpierw symulator, potem most, na końcu PsychoPy.**
- **Okno 1 – symulator** (zostawić otwarte):
  ```bash
  py -3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --port 5555        # Windows
  python3 simulator/symulator_biosygnalow.py --mode tcp --scenario mix --port 5555      # macOS
  ```
  Oczekiwane: `Czekam na klienta na 127.0.0.1:5555 ...`
- **Okno 2 – most** (zostawić otwarte):
  ```bash
  py -3 lsl/sim_to_lsl.py            # Windows
  .venv/bin/python lsl/sim_to_lsl.py # macOS
  ```
  Opcje: `--host 127.0.0.1 --port 5555` (domyślne).
- **Jak działa (najważniejsze w kodzie):**
  - czyta TCP linia po linii, każda linia to jeden obiekt JSON (`parse_line`);
  - dla każdego z 10 kanałów: brak pola, `null`, wartość nieliczbowa lub nieskończona → `NaN` (`number()`); `quality` tekstowe → kod 0/1/2, nieznane → `NaN`;
  - linia, która nie jest poprawnym JSON-em, jest **pomijana** z komunikatem `Pominieto niepoprawna linie` – most działa dalej;
  - po rozłączeniu TCP czeka 2 s i łączy się ponownie; strumień LSL pozostaje ten sam;
  - pole `scenario` jest ignorowane.
- **Zrzut:** `docs/img/6-4-bridge.png`
- **Jak sprawdzić:** w oknie 2 kolejno: `LSL: LBK_Sim (Physio), 10 kanalow; quality 0=ok 1=noisy 2=lost`, `Laczenie z symulatorem TCP 127.0.0.1:5555 ...`, `Polaczono z symulatorem 127.0.0.1:5555; publikuje LBK_Sim`.
- **Typowe problemy:** `Brak TCP / rozlaczenie … kolejna proba za 2 s` w kółko – symulator nie działa albo port jest inny. Symulator obsługuje **jednego** klienta: nie uruchamiać jednocześnie `klient_startowy.py`.

### Krok 6.5 – Test mostu na dwóch liniach · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** udowodnić, że brakujące pola dają `NaN`, a nie zatrzymanie programu.
- **Gdzie:** `tests/two_lines.jsonl`, `tests/test_bridge.py`.
- **Linie testowe:**
  ```json
  {"t":0,"hr":70,"eda_us":2.4,"rr_ms":850,"focus":0.6,"quality":"ok","gaze_x":400,"gaze_y":300,"gaze_valid":1,"pupil_mm":3.1,"resp":0.4}
  {"t":0.25,"hr":74,"eda_us":null,"rr_ms":810,"focus":0.5,"quality":"lost"}
  ```
  Linia 1 ma pola wzroku i oddechu; linia 2 ich nie ma, a `eda_us` = `null`.
- **Polecenie:** `py -3 tests/test_bridge.py` / `python3 tests/test_bridge.py` (nie wymaga pylsl).
- **Zrzut:** `docs/img/6-5-test.png`
- **Jak sprawdzić:** `OK: 2 linie, brakujace pola = NaN, quality zakodowane poprawnie`. Test sprawdza: linia 1 → 10 liczb, `quality=0`, `gaze_x=400`, `pupil_mm=3.1`, `resp=0.4`; linia 2 → `hr=74`, `quality=2`, kanały 5–9 = `NaN`.

### Krok 6.6 – Odbiór w PsychoPy i cechy w oknie 5 s · wykonanie: DK, poprawka RMSSD: OS · opis: OS · 2026-11-08

- **Cel:** w trakcie eksperymentu liczyć podstawowe cechy, bez blokowania klatek i bez pokazywania ich uczestnikowi.
- **Gdzie:** `experiment/lsl_runtime.py` (`poll`, `calculate_features`), wywoływane w Each Frame każdej routine (krok 3.4–3.10).
- **Ustawienia:**
  - odbiór: `pull_chunk(timeout=0.0, max_samples=128)` w każdej klatce (przy 60 Hz co 16,7 ms) – `timeout=0.0` oznacza „weź to, co już przyszło, nie czekaj”;
  - okno: próbki z ostatnich **5,0 s** czasu LSL; raport: co **1,0 s** przez `print` → konsola Runnera (eksperymentator), nie ekran;
  - **odrzucanie:** próbka liczy się tylko, gdy `quality == 0` (ok). `noisy`, `lost` i brak `quality` (`NaN`) są pomijane i liczone: `bad_window` (w bieżącym oknie) i `bad_total` (od początku);
  - `NaN` w poszczególnych kanałach poprawnej próbki są pomijane.
- **Wzory:**
  - `HR [bpm] = mean(hr)`
  - `RMSSD [ms] = sqrt( mean( (RR[i+1] − RR[i])² ) )` – różnice **tylko między sąsiednimi poprawnymi próbkami**; próbka odrzucona przerywa ciąg (nie liczymy różnicy „ponad” artefaktem). Mniej niż 2 kolejne RR → `NA`.
  - `EDA [µS] = median(eda_us)`
- **Jak sprawdzić:**
  1. Test: `py -3 tests/test_features.py` / `python3 tests/test_features.py` → `OK: HR, RMSSD z sasiednich roznic RR, mediana EDA, odrzucenie noisy/lost/NaN`. Test zawiera przypadek z artefaktem: RR 800, 820, 790, *noisy*, *lost*, 760, 780 → różnice 20, −30, 20 → RMSSD = 23,8 ms.
  2. Na żywo (eksperyment + most): w konsoli co ok. 1 s np. `5s | HR= 71.03 bpm | RMSSD= 48.00 ms | EDA med= 2.43 uS | valid= 18 bad_window= 2 bad_total= 3`. Przy 4 Hz `valid + bad_window` ≈ 20.
- **Zrzut:** — (przykładowa linia konsoli w „Jak sprawdzić”).
- **Ograniczenie:** RR z symulatora to wartości syntetyczne (1 RR na próbkę 4 Hz, a nie na uderzenie serca) – RMSSD sprawdza poprawność obliczeń, nie jest fizjologiczną miarą HRV.

### Krok 6.7 – Nagranie 2 min w LabRecorder · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** zapisać `LBK_Sim` i `LBK_Markers` w jednym pliku XDF na wspólnej osi czasu.
- **Kolejność (ważna – inaczej `exp:start` nie trafi do pliku):**
  1. Uruchomić symulator i most (6.4).
  2. Uruchomić eksperyment w PsychoPy, wpisać `participant = TEST-01`, `session = S001`. **Zatrzymać się na ekranie instrukcji – nie naciskać spacji.** (Strumień `LBK_Markers` powstaje dopiero przy starcie eksperymentu.)
  3. W LabRecorder: *Update* → zaznaczyć `LBK_Sim` i `LBK_Markers`. Study Root: `<repozytorium>/sample_data`; File Name/Template: `P3_KL-B_TEST-01_S001.xdf`. Kliknąć **Start**.
  4. Odczekać ok. 70 s na ekranie instrukcji (blok trwa tylko ok. 22 s + odpowiedź, a nagranie musi mieć ≥ 120 s; czasów bodźców nie zmieniamy).
  5. Nacisnąć spację → 4 obrazy → odpowiedź 1–9 → ekran końcowy.
  6. Zatrzymać nagranie (**Stop**), gdy od Start minęło ≥ 125 s.
- **Zasady:** w `sample_data/` wyłącznie nagrania z symulatora i MouseGaze; nigdy nagrania z aparatury LBK. Tylko pseudonim.
- **Zrzut:** `docs/img/6-7-labrecorder.png`
- **Jak sprawdzić:** LabRecorder pokazuje oba strumienie zaznaczone na zielono; po Stop w `sample_data/` jest plik `.xdf` (ok. 35–40 kB na 2 min).
- **Typowe problemy:** brak `LBK_Markers` na liście – PsychoPy jeszcze nie wystartował albo trzeba kliknąć *Update*. Zaznaczenie strumieni i Start **po** spacji → w pliku brak `exp:start` (tak było w nagraniu z 2026-11-08, wersja z `exp:start` w Begin Routine – rozdz. 15).

### Krok 6.8 – Wczytanie XDF i wykres EDA ze znacznikami · wykonanie: DK · opis: OS · 2026-11-08

- **Cel:** dowód wspólnej osi czasu.
- **Polecenie:**
  ```bash
  py -3 overlay/plot_xdf.py sample_data/P3_KL-B_TEST-01_S001.xdf --out docs/img/eda_markery.png              # Windows
  .venv/bin/python overlay/plot_xdf.py sample_data/P3_KL-B_TEST-01_S001.xdf --out docs/img/eda_markery.png   # macOS
  ```
- **Co robi skrypt:** `pyxdf.load_xdf` → wybiera strumienie po nazwie → kanał `eda_us` po etykiecie z metadanych → próbki `quality ≠ ok` jako przerwy w linii → pionowe linie dla wszystkich znaczników (kolor wg kategorii) → wypisuje listę znaczników z czasem i ostrzeżenia (brak wymaganych znaczników, nagranie < 120 s).
- **Zrzut / wynik:** `docs/img/eda_markery.png`
- **Jak sprawdzić:** w konsoli `strumienie: ['LBK_Sim', 'LBK_Markers']`, `LBK_Sim: ~500 probek, ≥120 s`, lista 15 znaczników (`exp:start`, 4 × 3 dla prób, `resp`, `exp:end`) i **brak** linii `UWAGA`. Na wykresie: linia EDA przez ≥ 120 s, czerwone przerywane linie `stim:onset` co ok. 5,5 s, czarne linie `exp:start` i `exp:end`.
- **Wynik nagrania z 2026-11-08 (wersja przed poprawką `exp:start`):** `LBK_Sim` 504 próbki, 125,8 s (488 ok, 9 noisy, 7 lost); `LBK_Markers` 14 znaczników; skrypt zgłasza `UWAGA: brak wymaganych znacznikow: exp:start`. **Nagranie należy powtórzyć według 6.7** i podmienić plik oraz wykres.

### Krok 6.9 – Schemat pętli biofeedbacku · schemat: DK, OS · opis: OS · 2026-11-08

- **Cel:** pokazać drogę sygnału i miejsca opóźnień.
- **Gdzie:** `docs/img/petla_biofeedback.png` (generowany skryptem `docs/petla_biofeedback.py`: `python3 docs/petla_biofeedback.py`), wersja tekstowa `docs/PETLA_BIOFEEDBACK.mmd` (Mermaid).
- **Treść:** bodziec → uczestnik → czujnik → most/LSL → PsychoPy (odbiór) → okno 5 s → decyzja → zmiana (tylko między próbami) → następny bodziec. Opóźnienia Δ1–Δ8: percepcja ~0,1–0,3 s; latencja odpowiedzi EDA ~1–3 s; próbkowanie 4 Hz ≤ 250 ms; LSL lokalnie < 10 ms; odbiór ≤ 1 klatka (16,7 ms); okno 5 s (średnia opóźniona ~2,5 s) i raport co 1 s; czekanie na koniec obrazu do 5 s.
- **Wniosek dla P3:** łączne opóźnienie to kilka sekund, więc adaptacja może zadziałać dopiero w przerwie po szarym ekranie – zgodnie z zasadą nienaruszalności (nie zmieniamy 4000 ms obrazu, 1000 ms szarości ani kolejności).
- **Jak sprawdzić:** schemat zawiera wszystkie 7 elementów z polecenia i zamyka się strzałką do bodźca.

### Krok 6.10 – Urządzenie GSR/EDA w LBK · odpowiedzialna osoba: OS · do uzupełnienia na sesji w LBK

- **Cel:** zamienić symulator i most na strumień z aparatury.
- **Do wpisania po sesji:** nazwa i typ strumienia (z LabRecorder), liczba kanałów, częstotliwość, jednostki, wersja sterownika, nazwa komputera. W `lsl_runtime.py` zmienić nazwę wyszukiwanego strumienia z `LBK_Sim` na odczytaną nazwę (oraz indeksy kanałów, jeśli inne).
- **Jak sprawdzić:** w LabRecorder w LBK widać strumień GSR i `LBK_Markers`; konsola PsychoPy pokazuje `… polaczony`.

**Sprawdzenie rozdziału 6 (jak poznać, że działa):** `tests/test_bridge.py` i `tests/test_features.py` → `OK`; w LabRecorder widać 2 strumienie: `LBK_Sim` i `LBK_Markers`; skrypt z 6.8 wypisuje oba strumienie, ≥ 120 s, 15 znaczników i brak ostrzeżeń.

**Karta źródeł** (dokumentacje i wnioski dla kodu): `docs/KARTA_ZRODEL.md`.

---

## 14. Odstępstwa i pytania do LBK

Zasada: niespójności zgłaszamy w forum „Pytania do projektu”, decyzję prowadzącego wpisujemy tutaj z datą.

### 14.1 – Liczba prób i kontrbalansowanie · DK · 2026-10-12 · otwarte
Slajd 6 protokołu: 30 prób; w materiałach 4 obrazy A–D. Ile prób, ile powtórzeń obrazu i jaka kolejność / kontrbalansowanie?
**Decyzja częściowa (e-mail prowadzącego, 2026-11-08):** w KL-B wystarczy jeden blok z oryginalnymi bodźcami; liczbę prób i kontrbalansowanie potwierdzić. **Decyzja końcowa:** [brak].

### 14.2 – Powrót EDA do linii bazowej · OS · 2026-10-12 · otwarte
Jak wyznaczać linię bazową EDA, jaki próg „powrotu” i jaki maksymalny czas czekania przed kolejnym bodźcem? **Decyzja:** [brak].

### 14.3 – Utrata śledzenia wzroku · DK · 2026-10-12 · otwarte
Jaki czas utraty sygnału ma wywoływać pauzę? Czy pauza wyłącznie między próbami (żeby zachować 4000 ms)? **Decyzja:** [brak].

### 14.4 – Aparatura i synchronizacja · OS · 2026-10-12 · otwarte
Nazwy, typy i częstotliwości strumieni LSL dla GSR/EDA i EyeLogic na stanowisku; wymagania kalibracji. **Decyzja:** [brak].

### 14.5 – Wersja PsychoPy · DK · 2026-10-12 · otwarte
Instalator 2025.2.4, aplikacja pokazuje „2025.2.4beta”. Jaka wspólna wersja na stanowisku LBK? **Decyzja:** [brak].

### 14.6 – Krzyż fiksacyjny i ankieta SAM · DK · 2026-11-08 · otwarte
Opis P3: obraz 4000 ms → szary ekran 1000 ms; protokół nie wspomina krzyża. W szkielecie jest roboczy krzyż 500 ms. Ocena: w szkielecie jedna skala pobudzenia 1–9 **po bloku**; slajd 13 – SAM (walencja, pobudzenie, dominacja). Czy krzyż ma zostać? Czy SAM po każdym obrazie, czy po bloku? **Decyzja:** [brak].

### 14.7 – Rozdzielczość i monitor · DK · 2026-11-08 · otwarte
1920×1080 px przyjęto roboczo (protokół P3 nie podaje rozdzielczości dla obrazów 594–716 px szerokości). Jaki monitor, odświeżanie i odległość w LBK? **Decyzja:** [brak].

---

## 15. Dziennik zmian

| Data | Kto | Co | Dlaczego |
|---|---|---|---|
| 2026-10-12 | DK | Instalacja PsychoPy, demo, symulator (rozdz. 1) | KL-A |
| 2026-11-08 | DK | Szkielet P3: `.psyexp`, bodźce A–D, plik warunków, `sim_to_lsl.py`, `lsl_runtime.py`, testy | KL-B |
| 2026-11-08 | DK | Uruchomienie z MouseGaze; pylsl/liblsl, LabRecorder 1.18.0; nagranie XDF (125,8 s, 14 znaczników, brak `exp:start`); wykres | KL-B – wspólna oś czasu |
| 2026-11-08 | OS | **Przegląd i poprawki:** (1) `exp:start` przeniesiony z Begin Routine na End Routine `intro` (po spacji) – wcześniej był wysyłany zanim LabRecorder mógł zasubskrybować `LBK_Markers`; (2) teksty instrukcji/pytania: zamiast dosłownych `\n` prawdziwe nowe linie, polskie znaki; (3) nazwa pliku danych wg konwencji LBK `P3_glowne_{kod}_{sesja}_{RRRR-MM-DD_GGMM}`, sesja `S001`; (4) RMSSD tylko z sąsiednich poprawnych RR + rozszerzony test; (5) ponowne łączenie z `LBK_Sim` przez nieblokujący `ContinuousResolver`; `summary()` na końcu; (6) most wypisuje potwierdzenie połączenia TCP; (7) wykres pomija próbki `quality ≠ ok`, pokazuje wszystkie znaczniki i sprawdza wymagane; (8) nowy schemat pętli z zamkniętą pętlą i Δ1–Δ8; (9) usunięto nieużywane pliki (DEMO, szablony, notatki robocze); (10) przepisane rozdz. 3, 4, 6 | Kryteria KL-B: wymagany `exp:start`, poprawny RMSSD, dane wyjściowe, odtwarzalność |
