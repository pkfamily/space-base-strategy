---
title: Simulator
nav_order: 4
---

# `spacebase2p` simulator

Python package in `src/spacebase2p/`: head-to-head **2p**, base game effects only (gold, income, VP, rockets, arrows, colonies). Excludes charge cubes, You Win, Gordon, swap, and dice-fix.

## Setup modeled

- 5 gold, random level 1 (pay cost), **Player 2 +1 gold** (CLI `--p1`; see [seat labels](simulation.md#player-seats-not-turn-order))
- Higher opening sector starts
- Win at **40 VP**, opponent’s **last turn**, higher VP wins (tie = draw)

## Bots

| Bot | Behavior |
| --- | -------- |
| `income` | Income to **5–7**, colonies, pass/deny, smart arrows |
| `rush` | **1–6** engines, colony race, pass/deny, smart arrows |
| `chain` | Income + **arrows 7–11**, deny, smart arrows (tests guide “blue chain”) |
| `snowball` | **Tempo** scoring (5–8 income + rush lines), then pure rush close; competes with `rush` |
| `random` | Uniform legal buy + random allocation |

## CLI

```bash
pip install -e ".[dev]"
python3 -m spacebase2p.cli simulate -n 500 --p0 chain --p1 rush --seed 42
python3 -m spacebase2p.cli replay --p0 chain --p1 rush --seed 42
python3 -m pytest
```

Output: win rates, average **overspend** per player, average **first colony turn**.

## Card data

Ships and colonies load from `src/spacebase2p/data/ships.json` and `colonies.json` (sector VP on colonies, expanded L1–L3 pool). Edit JSON and re-run sims — no charge / You Win / Gordon / swap / dice-fix cards.

## Telemetry

Each finished game tracks **rounds**, **VP from colonies vs dice (blue/red)**, **passes**, and **overspend**. Calibration test: rush vs rush median rounds in **14–22** (`tests/test_calibration.py`).

## Tests

- Dice allocation (singles vs sum)
- Doubles
- Income floor after purchase only
- Colony sector lock
- Endgame / final turn
- Rush mirror pace calibration

Source lives in the [GitHub repository](https://github.com/pkfamily/space-base-strategy).
