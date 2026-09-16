<div align="center">

```
  ┌─────────────────────────────────────────────────────────────┐
  │  ◈  U.E.S.  S T R A T E G Y   &   S I M U L A T I O N  ◈   │
  │     sectors 01 ─ 12  ·  race to 40 VP  ·  deploy or die     │
  └─────────────────────────────────────────────────────────────┘
```

# Space Base strategy

**Table guides for every player count** — plus a **`spacebase2p`** Python package that simulates head-to-head games, runs bot matchups, and backs the stats on the site.

<br>

[![Strategy guides](https://img.shields.io/badge/📖_Strategy_guides-GitHub_Pages-5c6bc0?style=for-the-badge)](https://pkfamily.github.io/space-base-strategy/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)
[![Tests](https://img.shields.io/badge/tests-pytest-0a9396?style=for-the-badge)](tests/)

<br>

| `01` | `02` | `03` | `04` | `05` | `06` | `07` | `08` | `09` | `10` | `11` | `12` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| low frequency · high payoff → → → → → → → → → → → → rare jackpots |

</div>

---

## New: `spacebase2p` simulator

A installable package in **`src/spacebase2p`** models **2-player, base-game** Space Base: dice allocation (singles / sum / doubles), income floor, colonies, rockets, arrows, and spend-all-gold buys. Three bots ship with the CLI — **`income`**, **`rush`**, and **`random`** — so you can batch thousands of games and compare win rates, overspend, and when colonies land.

```bash
git clone https://github.com/pkfamily/space-base-strategy.git
cd space-base-strategy
pip install -e ".[dev]"

# Run 500 games: income plan vs rush plan
python3 -m spacebase2p.cli -n 500 --p0 income --p1 rush --seed 42

python3 -m pytest
```

| | |
| --- | --- |
| **Package docs** | [docs/simulator.md](docs/simulator.md) |
| **Published results** | [Simulation results](https://pkfamily.github.io/space-base-strategy/simulation.html) (rush vs income, overspend, colony timing) |
| **Entry point** | `spacebase2p` console script after install |

> **Headline from the sim:** rush-style play wins heavily in the current bots — mostly **gold overspend** on “buy every turn” income lines, not because income is weak on paper. See the [results page](docs/simulation.md) for tables.

---

## Strategy guides (human players)

Full write-ups live on **GitHub Pages** — engine math, 2p/3p normal, Light Speed, shared tactics, and quick reference.

**→ [pkfamily.github.io/space-base-strategy](https://pkfamily.github.io/space-base-strategy/)**

| Mode | Guide |
|------|--------|
| 2p normal | [Two-player](https://pkfamily.github.io/space-base-strategy/guide/2p-normal.html) |
| 3p normal | [Three-player](https://pkfamily.github.io/space-base-strategy/guide/3p-normal.html) |
| Light Speed | [Overview](https://pkfamily.github.io/space-base-strategy/guide/light-speed.html) · [2p LS](https://pkfamily.github.io/space-base-strategy/guide/2p-light-speed.html) · [3p LS](https://pkfamily.github.io/space-base-strategy/guide/3p-light-speed.html) |
| Engine & tactics | [Engine rules](https://pkfamily.github.io/space-base-strategy/engine.html) · [Shared tactics](https://pkfamily.github.io/space-base-strategy/guide/shared-tactics.html) · [Quick reference](https://pkfamily.github.io/space-base-strategy/guide/quick-reference.html) |

Source markdown is in [`docs/`](docs/) if you prefer reading in-repo.

---

## Repo map

```
space-base-strategy/
├── src/spacebase2p/     ← 2p simulation engine, bots, CLI
├── tests/               ← allocation, doubles, income, colonies, endgame
├── docs/                ← Jekyll site (guides + simulation page)
└── pyproject.toml
```

---

<details>
<summary><strong>Maintainers: GitHub Pages setup</strong></summary>

The static site is built from **`docs/`**, not the repo root (root is the Python package).

1. **Recommended:** **Settings → Pages → Source: GitHub Actions** — uses [`.github/workflows/pages.yml`](.github/workflows/pages.yml) (`source: ./docs`).
2. **Or:** **Deploy from branch** `main` → folder **`/docs`**.

Use one method only. Local preview: `cd docs && bundle install && bundle exec jekyll serve`.

</details>

---

<div align="center">

<sub>Space Base™ is © Alderac Entertainment Group. This repo is an unofficial fan strategy and simulation project.</sub>

</div>
