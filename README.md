<p align="center">
  <img src="docs/assets/readme-banner.png" alt="Space Base strategy and simulation — rockets, sectors, race to 40 VP" width="100%" />
</p>

<p align="center">
  <a href="https://pkfamily.github.io/space-base-strategy/"><img src="https://img.shields.io/badge/Strategy_guides-GitHub_Pages-2d6a9f?style=for-the-badge" alt="Strategy guides on GitHub Pages" /></a>
  <a href="https://pkfamily.github.io/space-base-strategy/simulation.html"><img src="https://img.shields.io/badge/Sim_results-charts_&_JSON-e85d04?style=for-the-badge" alt="Simulation results" /></a>
  <a href="docs/simulator.md"><img src="https://img.shields.io/badge/spacebase2p-Python_simulator-0a9396?style=for-the-badge&logo=python&logoColor=white" alt="spacebase2p Python simulator" /></a>
</p>

<p align="center">
  Unofficial fan project — table guides for 2p–5p Space Base, plus a <strong>2-player simulation package</strong> you can run from the CLI.
</p>

---

## `spacebase2p` — 2-player simulation

Python package (`src/spacebase2p`) for head-to-head **base game** 2p: dice allocation, doubles, income floor, colonies, rockets, arrows, spend-all-gold buys. Setup matches normal start (5g, random L1, **+1 gold to whoever rolls second** in round 1).

**Bots:** `income`, `rush`, `snowball`, `chain`, `random` — see [simulator](docs/simulator.md) and [assumptions](docs/sim-assumptions.md).

```bash
git clone https://github.com/pkfamily/space-base-strategy.git
cd space-base-strategy
pip install -e ".[dev]"

python3 -m spacebase2p.cli simulate -n 500 --p0 snowball --p1 rush
python3 -m spacebase2p.cli replay --p0 snowball --p1 rush --seed 42
python3 scripts/generate_simulation_plots.py   # refresh docs/assets/plots/
python3 -m pytest
```

| | |
| --- | --- |
| Package & CLI | [docs/simulator.md](docs/simulator.md) |
| Charts & batch table | [Simulation results](https://pkfamily.github.io/space-base-strategy/simulation.html) |
| Sim vs strategy guide | [Sim analysis](https://pkfamily.github.io/space-base-strategy/sim-analysis.html) |
| `summary.json` | [docs/assets/plots/summary.json](docs/assets/plots/summary.json) |

**Takeaway from current bots:** `rush` still beats naive `income` (overspend). **`snowball`** (tempo income + rush close) is **competitive with `rush`** in batch sims. Charts and tables regenerate on each [Pages deploy](.github/workflows/pages.yml).

---

## Strategy guides

Full playbooks on **GitHub Pages**:

### [pkfamily.github.io/space-base-strategy](https://pkfamily.github.io/space-base-strategy/)

- [Engine](https://pkfamily.github.io/space-base-strategy/engine.html) · [2p](https://pkfamily.github.io/space-base-strategy/guide/2p-normal.html) · [3p](https://pkfamily.github.io/space-base-strategy/guide/3p-normal.html) · [Light Speed](https://pkfamily.github.io/space-base-strategy/guide/light-speed.html) · [Quick reference](https://pkfamily.github.io/space-base-strategy/guide/quick-reference.html)

Source: [`docs/`](docs/)

---

## Repo layout

```
src/spacebase2p/   engine, bots, CLI, card JSON
tests/             pytest (rules, calibration, bots)
docs/              Jekyll site, guides, plot assets
scripts/           generate_simulation_plots.py
```

<details>
<summary><strong>Maintainers: GitHub Pages</strong></summary>

Use **Settings → Pages → Build and deployment → GitHub Actions** ([workflow](.github/workflows/pages.yml)). The workflow runs the plot script, then builds Jekyll from `docs/`. Bump `plots_version` in `docs/_config.yml` when you need browsers to reload chart PNGs.

</details>

<p align="center">
  <sub>Space Base™ is © Alderac Entertainment Group. This repository is unofficial fan content.</sub>
</p>
