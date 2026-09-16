#!/usr/bin/env python3
"""Regenerate simulation plots and summary JSON for the docs site."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np

from spacebase2p.benchmark import run_all_matchups

OUT = ROOT / "docs" / "assets" / "plots"
GAMES = 400  # balance CI time vs stability; scale labels note seed
SEED = 42

# Space Base–inspired palette (original, not official assets)
BG = "#0d1b2a"
PANEL = "#1b2838"
TEAL = "#2ec4b6"
ORANGE = "#e85d04"
GOLD = "#e9c46a"
SKY = "#4cc9f0"
MUTED = "#8ba3b8"
GRID = "#2a3f55"


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "axes.edgecolor": GRID,
            "axes.labelcolor": MUTED,
            "text.color": "#e6edf3",
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": GRID,
            "grid.alpha": 0.35,
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
        }
    )


def _label(r) -> str:
    return f"{r.p0} vs {r.p1}"


def plot_win_rates(results) -> None:
    labels = [_label(r) for r in results]
    rates = [r.p0_win_rate for r in results]
    y = np.arange(len(labels))
    colors = [ORANGE if "income" in r.p0 and "rush" in r.p1 else TEAL if "rush" in r.p0 else SKY for r in results]

    fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
    bars = ax.barh(y, rates, color=colors, height=0.65, edgecolor=GRID)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 105)
    ax.set_xlabel("P0 win rate (%)")
    ax.set_title("Head-to-head win rates", color=GOLD, fontsize=14, fontweight="bold")
    ax.axvline(50, color=MUTED, linestyle="--", linewidth=0.8, alpha=0.6)
    ax.grid(axis="x")
    for bar, rate in zip(bars, rates):
        ax.text(rate + 1.2, bar.get_y() + bar.get_height() / 2, f"{rate:.1f}%", va="center", fontsize=9)
    fig.savefig(OUT / "win_rates.png", dpi=144, facecolor=BG)
    plt.close(fig)


def plot_overspend(results) -> None:
    labels = [_label(r) for r in results]
    x = np.arange(len(labels))
    w = 0.38
    p0 = [r.avg_overspend_p0 for r in results]
    p1 = [r.avg_overspend_p1 for r in results]

    fig, ax = plt.subplots(figsize=(11, 5.5), layout="constrained")
    ax.bar(x - w / 2, p0, w, label="P0 overspend", color=ORANGE, edgecolor=GRID)
    ax.bar(x + w / 2, p1, w, label="P1 overspend", color=TEAL, edgecolor=GRID)
    ax.set_xticks(x, labels, rotation=28, ha="right")
    ax.set_ylabel("Avg gold leaked per game")
    ax.set_title("Overspend (spend-all-gold buys)", color=GOLD, fontsize=14, fontweight="bold")
    ax.legend(facecolor=PANEL, edgecolor=GRID)
    ax.grid(axis="y")
    fig.savefig(OUT / "overspend.png", dpi=144, facecolor=BG)
    plt.close(fig)


def plot_pace_colonies(results) -> None:
    key = next(r for r in results if r.p0 == "income" and r.p1 == "rush")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), layout="constrained")

    matchups_short = [_label(r) for r in results]
    turns = [r.avg_turns for r in results]
    ax1.barh(matchups_short, turns, color=SKY, edgecolor=GRID)
    ax1.set_xlabel("Avg turns (shared rounds)")
    ax1.set_title("Game length", color=GOLD, fontsize=12, fontweight="bold")
    ax1.grid(axis="x")

    bots = [f"P0 ({key.p0})", f"P1 ({key.p1})"]
    colonies = [
        key.avg_colony_turn_p0 or 0,
        key.avg_colony_turn_p1 or 0,
    ]
    ax2.bar(bots, colonies, color=[ORANGE, TEAL], edgecolor=GRID, width=0.55)
    ax2.set_ylabel("Avg first colony turn")
    ax2.set_title("income vs rush — colony timing", color=GOLD, fontsize=12, fontweight="bold")
    ax2.grid(axis="y")

    fig.savefig(OUT / "pace_colonies.png", dpi=144, facecolor=BG)
    plt.close(fig)


def write_summary_markdown_snippet(results) -> None:
    """Optional: print table rows for pasting into simulation.md."""
    for r in results:
        print(
            f"| {r.p0} | {r.p1} | {r.p0_win_rate:.1f} | {r.draws} | "
            f"{r.avg_turns:.1f} | {r.avg_overspend_p0:.1f} | {r.avg_overspend_p1:.1f} |"
        )


def write_summary_json(results) -> None:
    data = {
        "games_per_matchup": GAMES,
        "seed": SEED,
        "matchups": [
            {
                "p0": r.p0,
                "p1": r.p1,
                "p0_win_rate": round(r.p0_win_rate, 2),
                "draws": r.draws,
                "unfinished": r.games - r.finished,
                "avg_turns": round(r.avg_turns, 2),
                "avg_overspend_p0": round(r.avg_overspend_p0, 2),
                "avg_overspend_p1": round(r.avg_overspend_p1, 2),
                "avg_colony_turn_p0": round(r.avg_colony_turn_p0, 2) if r.avg_colony_turn_p0 else None,
                "avg_colony_turn_p1": round(r.avg_colony_turn_p1, 2) if r.avg_colony_turn_p1 else None,
                "avg_vp_margin": round(r.avg_vp_margin, 2),
            }
            for r in results
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(data, indent=2) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _style()
    from spacebase2p.benchmark import DEFAULT_MATCHUPS

    print(f"Running {GAMES} games × {len(DEFAULT_MATCHUPS)} matchups (seed {SEED})...")
    results = run_all_matchups(games=GAMES, seed=SEED)
    plot_win_rates(results)
    plot_overspend(results)
    plot_pace_colonies(results)
    write_summary_json(results)
    print(f"Wrote plots to {OUT}")


if __name__ == "__main__":
    main()
