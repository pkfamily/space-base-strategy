---
title: Simulator
nav_order: 3
---

# `spacebase2p` simulator

Python package in `src/spacebase2p/`: head-to-head **2p**, base game effects only (gold, income, VP, rockets, arrows, colonies). Excludes charge cubes, You Win, Gordon, swap, and dice-fix.

## Setup modeled

- 5 gold, random level 1 (pay cost), **P2 +1 gold**
- Higher opening sector starts
- Win at **40 VP**, opponent’s **last turn**, higher VP wins (tie = draw)

## Bots

| Bot | Behavior |
| --- | -------- |
| `income` | Buy until **5–8 income**, then colonies |
| `rush` | Cargo/rockets on **1–6**, colonies from **~20 VP** |
| `random` | Uniform legal buy + random allocation |

## CLI

```bash
pip install -e ".[dev]"
python3 -m spacebase2p.cli -n 500 --p0 income --p1 rush --seed 42
python3 -m pytest
```

Output: win rates, average **overspend** per player, average **first colony turn**.

## Tests

- Dice allocation (singles vs sum)
- Doubles
- Income floor after purchase only
- Colony sector lock
- Endgame / final turn

Source lives in the [GitHub repository](https://github.com/pkfamily/space-base-strategy).
