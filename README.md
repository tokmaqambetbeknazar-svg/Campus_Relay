# Campus Relay 3D

A small delivery rover carries a replacement power relay across a campus. A noisy gate sensor can make a short route more expensive than a detour. The player can drive manually or follow the suggested action.

**AI Fundamentals · Arlan Mustafin and Beknazar Tokmagambet**

## Play locally

Download or clone this repository. Open `index.html` in Chrome or Edge. All game assets are embedded. Use **WASD** or **arrow keys** to drive, **Q** to scan, or **Follow route** to advance one tile. Drag to orbit, scroll to zoom, or choose **Follow rover**. Open **Mission settings, algorithm trace & project files** for the sensor input, route strategy and calculations.

| District | Grid | Challenge |
| --- | --- | --- |
| Relay Courtyard | 5 × 5 | Two walls and a gate with a noisy sensor. Original course scenario. |
| Freight Depot | 6 × 6 | Containers block lanes. A grate costs two turns to enter. |
| Flooded Gardens | 7 × 7 | Deep water blocks movement. Shallow water costs two turns. |
| Midnight Rail Yard | 8 × 8 | Barricades block lanes. A red crossing forces a one-turn wait. |

## Reproduce the course demonstration

Run these commands from the repository root. Python 3.8+ is sufficient for the first two. The browser-logic test uses Node.js 18+. Neither requires extra packages.

```sh
python campus_demo.py
python -m unittest discover -s tests -v
node tests/game.cjs
```

The Python reference covers the **first district**. The HTML contains the full game for all four districts.

| Opening signal and route | Posterior blockage risk | Result |
| --- | --- | --- |
| CLEAR, A* | 9.68% | MOVE, 4 steps, weighted cost 4.39 |
| ALERT, A* | 63.16% | MOVE on a detour, 6 steps, weighted cost 6.00 |
| ALERT, direct corridor | 63.16% | WAIT at the depot. The next scripted CLEAR reading permits movement. |

Bayes estimates blockage. A* adds the expected gate delay to its route cost. The one-step MDP compares MOVE and WAIT for the next cell on the chosen route.

## Project materials

- [Technical report](docs/technical-report.md) — assumptions, algorithm calculations, results and limitations.
- [Presentation](docs/Campus-Relay.pptx) — six slides for the project defense.
- [AI usage declaration](docs/ai-usage.md).
- [Team contribution statement](docs/team-contribution.md) — team confirmation required before submission.
- [Demo recording script](docs/demo-script.md) — timing and actions for the required 2–3 minute video.

