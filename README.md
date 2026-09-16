# Space Base strategy

Strategy guides and a **2-player simulator** for Space Base (base game).

**Read the guides on GitHub Pages:** [pkfamily.github.io/space-base-strategy](https://pkfamily.github.io/space-base-strategy/)

### GitHub Pages: use `/docs`, not repo root

The Jekyll site lives in **`docs/`** (`_config.yml`, guides, simulation page). The Python simulator stays at the repo root (`src/spacebase2p`, `pyproject.toml`). Do **not** set Pages to the root `/` folder.

**Recommended:** **Settings → Pages → Source: GitHub Actions**. The workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) runs Jekyll with `source: ./docs` and deploys the built site.

**Alternative:** **Source: Deploy from branch** → branch `main` → folder **`/docs`** (built-in Jekyll on GitHub; no workflow). Pick Actions *or* branch deploy, not both.

## Simulator

```bash
pip install -e ".[dev]"
python3 -m spacebase2p.cli -n 500 --p0 income --p1 rush
python3 -m pytest
```

See [docs/simulator.md](docs/simulator.md) and [simulation results](docs/simulation.md).

## Documentation layout

| Path | Contents |
| ---- | -------- |
| [docs/index.md](docs/index.md) | Site home |
| [docs/engine.md](docs/engine.md) | Dice, income, colonies, player-count table |
| [docs/guide/](docs/guide/) | 2p/3p and Light Speed playbooks |
| [docs/simulation.md](docs/simulation.md) | Bot matchup statistics |
| [docs/simulator.md](docs/simulator.md) | Package and CLI |

Local preview (optional):

```bash
cd docs && bundle install && bundle exec jekyll serve
```
