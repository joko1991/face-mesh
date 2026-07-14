# face-mesh

Wizualizacja geometrii twarzy (468 punktów, MediaPipe Face Mesh) — narzędzie edukacyjne pokazujące, **jak działa technologia stojąca za deepfake'ami** i gdzie szukać śladów manipulacji.

Projekt powstał jako materiał do treści o cyfrowej samoobronie i wykrywaniu dezinformacji (FIMI). Celem nie jest tworzenie deepfake'ów, lecz **zrozumienie i demaskowanie** mechanizmu podmiany twarzy.

## Po co to jest

Deepfaki oparte na podmianie twarzy działają w trzech krokach: model uczy się geometrii twarzy z wielu zdjęć, mapuje ją na twarz w nagraniu źródłowym i renderuje klatka po klatce. Ten skrypt wizualizuje **pierwszy krok** — siatkę geometrii — dzięki czemu widać, jak maszyna "widzi" twarz. To punkt wyjścia do rozmowy o tym, dlaczego syntetyczne twarze wyglądają realnie i gdzie mimo wszystko się sypią (dłonie, krawędzie, drobne przedmioty).

## Instalacja

Wymaga Pythona 3.11 (MediaPipe nie wspiera 3.13+).

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Użycie

```bash
python src/face_mesh_reel.py input.mp4 output/out.mp4 --style mesh
```

Style wizualizacji:

| Styl       | Opis                                              |
|------------|---------------------------------------------------|
| `mesh`     | pełna siatka trójkątów — najbardziej "techniczny" look |
| `dots`     | same punkty — minimalistycznie, dobre na jasnym tle   |
| `contours` | kontury twarzy, oczu, ust — czytelne, mniej gęste     |

Plik wyjściowy jest bez dźwięku (ścieżkę audio dokładasz w edytorze wideo).

## Struktura

```
face-mesh-demo/
├── src/
│   └── face_mesh_reel.py     # wizualizacja face mesh na wideo
├── examples/                 # krótkie klipy demonstracyjne
├── output/                   # wyniki działania (ignorowane przez git)
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Wizualizacja geometrii twarzy (mesh / dots / contours)
- [ ] Moduł "artifact spotter" — podświetlanie obszarów typowych dla artefaktów deepfake (dłonie, krawędzie twarzy, migotanie temporalne)
- [ ] Prosty wskaźnik pewności na podstawie spójności geometrii między klatkami

## Kontekst

Część szerszej pracy nad wykrywaniem manipulacji informacyjnej. Powiązane: [info-resilience](https://github.com/) — detektor clickbaitu i manipulacji.

## Uwaga etyczna

Narzędzie służy edukacji i wykrywaniu manipulacji. Nie zawiera funkcji generowania deepfake'ów ani podmiany twarzy realnych osób. Od 2 sierpnia 2026 r. treści generowane przez AI podlegają w UE obowiązkom oznaczania (art. 50 rozporządzenia 2024/1689).

## Licencja

MIT
