---
title: Sim vs guide
nav_order: 3
---

# Simulation analysis vs the 2p guide

This page interprets the latest [simulation batch](simulation.md) and maps numbers to claims in the [two-player normal guide](guide/2p-normal.md). For model limits (stub deck, bots, excluded cards), see [Simulation assumptions](sim-assumptions.md).

<div class="sb-callout">
  <strong>Bottom line:</strong> The model agrees with the guide on <strong>pace (~20 shared rounds)</strong>, <strong>colony closing</strong>, and <strong>gold leak</strong>. It shows <strong>rush-style red tempo</strong> crushing a naive always-buy income bot, while a <strong>chain</strong> bot only matches income today because the stub deck rarely changes buy order.
</div>

## Method (this batch)

| Setting | Value |
| ------- | ----- |
| Games per matchup | **400** ([`summary.json`]({{ '/assets/plots/summary.json' | relative_url }})) |
| Global seed | **42** (each matchup uses its own derived seed) |
| Bots | `income`, `rush`, `chain`, `random` |
| Win condition | 40 VP, opponent last turn |

Charts on [Simulation results](simulation.md) are regenerated on each GitHub Pages deploy from [`scripts/generate_simulation_plots.py`](https://github.com/pkfamily/space-base-strategy/blob/main/scripts/generate_simulation_plots.py).

## Guide claims vs simulation evidence

| Guide claim ([2p normal](guide/2p-normal.md)) | What the sim shows | Confidence |
| --------------------------------------------- | ------------------ | ---------- |
| “~20 of your turns” / ~20 shared rounds in 2p | `rush` vs `rush`: **median 23** shared rounds, mean **23.2** | **Strong** — inside calibration band 14–24 |
| Income on 5–8 compounds in 2p | `income` vs `income` is ~50/50 but **slow** (mean **27.8** turns) with heavy leak on both sides | **Partial** — income plan works only with discipline the bot lacks |
| “Buy vs save” / leak separates strong from average | `income` vs `rush`: income seat leaks **~50** gold/game vs rush **~6**; rush vs income reverses seats | **Strong** — overspend dominates |
| Red rockets on 5–6 are excellent in 2p | `rush` beats `income` **~74%** when rush is P0 (`income` as P0 wins **23.8%**) | **Strong** for this bot pair |
| Blue arrow chains are highest ceiling | `chain` is **slightly better vs rush** than pure `income` (**21%** vs **24%** P0 wins) but still loses badly; stub deck limits chain buys | **Partial** — directionally right, not decisive |
| Closing: colonies at 3g/VP, race math | Rush mirror: **~12 VP** from colonies and **~18 VP** from dice (P0 averages) | **Moderate** — both sources matter; colonies not the whole score |
| Hate-draft arrows / deny finishing colonies | Bots use score-based **deny**; no full market denial | **Weak** — heuristic only |
| Gordon, You Win, swap, dice-fix | **Not in engine** | **Not tested** |

## Pacing and game length

The guide frames 2p as a **~20-turn** race. In the model, two `rush` bots finish in **23** shared rounds (median), with the histogram’s dotted line at 20 as a visual anchor on [Simulation results](simulation.md).

- **Mirror rush** is the right calibration target: both players colony-race and buy low-sector tempo (median **23** shared rounds).
- **Double income** stretches the game (**~27** turns) without improving the income bot’s record against rush — time without conversion is wasted.

`random` vs `random` often runs long (mean **~66** turns, a few hit the 800-turn cap) and is useful only as a sanity check, not strategy insight.

## Overspend and passing

The guide’s “leak” advice is the clearest place where bots diverge from human play and where the sim still teaches:

| Matchup | Avg overspend (gold leaked after buys) |
| ------- | -------------------------------------- |
| `income` (P0) vs `rush` (P1) | P0 **50.1** · P1 **6.3** |
| `rush` (P0) vs `income` (P1) | P0 **5.9** · P1 **54.2** |
| `rush` vs `rush` | P0 **9.6** · P1 **8.7** |

`rush` passes when buys would waste gold; the income bot still **buys too often** even with pass logic. That is a **bot limitation**, but it matches the guide: an income plan that never passes loses to someone who spends efficiently and races.

Average **passes per game** in `income` vs `rush` are **~10** (income) vs **~12** (rush) — both pass sometimes, but income still leaks more because purchases are looser before the endgame.

## VP sources at the table

In `rush` vs `rush`, typical P0 scoring splits roughly **12 VP colonies / 18 VP dice** (batch averages). That supports the guide’s closing chapter: you are not only colony-rushing; **dice rewards and rockets** still supply a large share of the 40.

First colony turn in the income vs rush matchup clusters around **turn 17–18** for both seats — colonies start midgame, not turn 1.

## Bot matchups (headline rates)

P0 win % from the latest `summary.json`:

| P0 | P1 | P0 win % | Notes |
| -- | -- | -------- | ----- |
| `rush` | `income` | **74.0** | Rush seat favored |
| `income` | `rush` | **23.8** | Income leaks ~50 gold/game |
| `rush` | `random` | **92.8** | |
| `income` | `random` | **86.5** | Income still beats noise |
| `rush` | `rush` | **45.0** | Fair mirror |
| `chain` | `rush` | **21.3** | Slightly worse than `income` as P0 |
| `rush` | `chain` | **68.3** | Chain leaks more than income as P1 (**~59** gold) |
| `chain` | `income` | **47.8** | Near even; chain a touch faster |

**`chain` vs `income`:** small sample differences only — expand `ships.json` before treating arrow bots as validated.

## What to do with this

1. **Trust the guide on tempo and leak** — sim pace and overspend align with human advice.
2. **Do not trust “income always wins”** — without passing and deny, income loses badly to rush in the model.
3. **Arrow chains need a richer sim** before they can contradict or confirm “highest ceiling” — expand `ships.json`, then re-run the batch.
4. **Use replay for one-off stories** — `python3 -m spacebase2p.cli replay --p0 chain --p1 rush --seed 42` after `pip install -e ".[dev]"`.

## Related pages

- [Simulation results](simulation.md) — charts and raw table
- [Simulation assumptions](sim-assumptions.md) — engine and bot definitions
- [Two-player normal guide](guide/2p-normal.md) — full human playbook
- [Simulator](simulator.md) — CLI and package layout
