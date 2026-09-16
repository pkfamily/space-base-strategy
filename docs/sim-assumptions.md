---
title: Simulation assumptions
nav_order: 5
---

# Simulation vs strategy guide

The [strategy guides](guide/) describe how **humans** should play Space Base at the table. The [`spacebase2p`](../simulator.md) package is a **model** with explicit limits. Use this page to see what the sim proves and what it does not.

## What we model

| Topic | Assumption |
| ----- | ---------- |
| Mode | **2-player**, base game, normal start (5 gold, random L1, P2 +1) |
| Win | **40 VP**, opponent’s last turn |
| Effects | Gold, income, VP, rockets (VP on red), left/right arrows, colonies |
| Excluded | Charge cubes, You Win, Gordon, swap, dice-fix, green sum-shifters |
| Cards | JSON deck in `src/spacebase2p/data/` (expanded stub, not full 132 ships) |
| Colonies | Sector VP 1–6 at **3 gold** (see `colonies.json`) |
| Buying | Spend **all** gold on purchase; income refill **only after** a buy |

## Bots

| Bot | Intent |
| --- | ------ |
| `rush` | 1–6 cargo/rockets, colony race, pass on leak, deny, arrow-smart rolls |
| `income` | Income to 5–7, then colonies; pass; deny; arrow-smart rolls |
| `chain` | Like income but **buys arrows on 7–11** and values chain targets |
| `snowball` | **Tempo** buys (mid-sector income + low rockets/cargo), arrows while building, then **rush** close |
| `random` | Uniform legal moves (sanity check only) |

**Arrow-aware rolls:** singles vs sum and left vs right use `arrow_ai` (greedy VP/gold/income scoring).

**Deny:** When opponent is near **40**, bots may take the best affordable **colony**; may hate-draft **arrows on 7–11** that feed a strong opponent sector.

## `snowball` vs `rush`

The **`snowball`** bot implements the guide’s blended plan (efficient **5–8 income** plus **1–6 tempo**, deny, arrow-aware rolls). In batch sims it lands **near 50%** against `rush` — unlike naive `income`, which still collapses. Pure rush is no longer the only viable bot; it is the baseline to beat.

## Early `chain` vs `rush` signal

With deny + arrow-aware rolls, **`chain` still loses most games to `rush`** (~**76%** rush wins when rush is P0 in the latest batch) — same ballpark as **`income` vs `rush`** because the stub deck rarely changes `chain` buys. That supports the guide’s split: **low-sector red tempo** is strong in 2p, while **blue arrow plans** need a richer pool and tighter play to overtake a rush race—not “buy income forever.” See [Sim vs guide](sim-analysis.md).

## What corroborates the guide

- **~20 shared rounds** when both race (`rush` vs `rush`, calibration test 14–22).
- **Colonies + dice** both matter; closing is ~half of VP in rush mirrors.
- **Gold leak** decides many games; passing is required for income to compete.
- **Red on low sectors** helps rush lines in 2p.

## What the guide claims but the sim does not fully test

- Full **arrow chains** with sum manipulation and multi-card setups.
- **Hate-draft** of specific finishing colonies the opponent needs (only score-based deny).
- **3p / Light Speed** player counts and drafts.
- **Psychology / tempo** and face-up market denial beyond simple heuristics.

## Commands

```bash
python3 -m spacebase2p.cli simulate -n 300 --p0 chain --p1 rush
python3 -m spacebase2p.cli replay --p0 chain --p1 rush --seed 42
```

Regression: `tests/test_calibration.py` (rush mirror pace), plus allocation/colony/endgame tests.
