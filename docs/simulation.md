---
title: Simulation results
nav_order: 2
---

# 2-player simulation results

Batch runs use the [`spacebase2p`](../simulator.md) package: base game only, simplified card pool, three bots (`income`, `rush`, `random`). Each matchup below is **800 games** (seed 42, up to 800 turns per game).

## Head-to-head win rates

| P0 | P1 | P0 wins | Draws | Unfinished |
| -- | -- | ------- | ----- | ---------- |
| income | rush | **6.4%** | 0 | 0 |
| rush | income | **86.8%** | 1 | 0 |
| income | income | **46.0%** | 2 | 0 |
| rush | rush | **44.0%** | 2 | 0 |
| income | random | **92.4%** | 1 | 1 |
| rush | random | **99.9%** | 0 | 0 |
| random | random | **52.4%** | 2 | 2 |

**Takeaway:** In this model, **rush crushes income**. Mirrors are roughly fair (small first-player edge in rush–rush; see below).

## Overspend (gold leaked on “spend all credits” buys)

| Matchup | Avg overspend P0 | Avg overspend P1 |
| ------- | ---------------- | ---------------- |
| income vs rush | **45.0** | **7.7** |
| rush vs income | **7.4** | **57.4** |
| income mirror | **29.1** | **44.3** |
| rush mirror | **12.4** | **13.2** |
| income vs random | **71.8** | **4.5** |
| rush vs random | **10.0** | **3.4** |

The income bot **buys whenever it can** (including stacking income). That matches “buy most turns” in theory but **bleeds 30–50+ gold per game** vs rush’s ~8. The simulator treats overspend as a first-order skill gap — aligned with the written guide’s “don’t leak gold” advice.

## Pace and colonies

| Matchup | Avg turns | 1st colony P0 | 1st colony P1 | Avg VP margin |
| ------- | --------- | ------------- | ------------- | ------------- |
| income vs rush | 24.2 | 15.9 | 17.8 | 27.4 |
| rush vs income | 25.9 | 19.1 | 14.9 | 25.2 |
| income mirror | 28.5 | 16.6 | 15.6 | 20.9 |
| rush mirror | 23.5 | 18.8 | 17.7 | 23.3 |
| income vs random | 37.4 | 19.8 | 4.9 | 32.5 |
| rush vs random | 26.4 | 20.1 | 4.5 | 37.0 |
| random mirror | 68.5 | 11.4 | 5.7 | 24.8 |

Income **starts colonizing earlier** than rush in income vs rush, but still loses — rockets/red VP and low overspend close the game first. **Random** rarely buys colonies (late or missing first-colony turn). Random mirrors are **very long** (~69 turns) and occasionally hit the engine turn cap.

## Seat (rush mirror, 2000 games)

| Starter wins | Second seat wins |
| ------------ | ---------------- |
| **53.1%** | **46.7%** |

P2’s +1 gold helps but does not flip rush mirrors in this sample.

## Caveats

- **Simplified deck**, not the full 132-card ship list.
- Bots are **heuristic**, not optimal (income does not yet “pass” to avoid overspend).
- CLI default **500-turn** cap can crash `random` vs `random`; long runs need a higher cap (analysis used 800).

Reproduce or extend:

```bash
pip install -e ".[dev]"
python3 -m spacebase2p.cli -n 500 --p0 income --p1 rush
```
