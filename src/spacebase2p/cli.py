from __future__ import annotations

import argparse

from spacebase2p.simulate import run_simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate 2-player Space Base games")
    parser.add_argument("-n", "--games", type=int, default=100, help="number of games")
    parser.add_argument("--p0", default="income", help="bot for player 0: income|rush|random")
    parser.add_argument("--p1", default="rush", help="bot for player 1")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    args = parser.parse_args()

    summary = run_simulation(args.games, args.p0, args.p1, seed=args.seed)
    g = summary.games
    print(f"Games: {g}")
    print(f"P0 ({args.p0}) wins: {summary.p0_wins} ({100 * summary.p0_wins / g:.1f}%)")
    print(f"P1 ({args.p1}) wins: {summary.p1_wins} ({100 * summary.p1_wins / g:.1f}%)")
    print(f"Draws: {summary.draws} ({100 * summary.draws / g:.1f}%)")
    print(f"Avg overspend P0: {summary.avg_overspend_p0:.2f}")
    print(f"Avg overspend P1: {summary.avg_overspend_p1:.2f}")
    c0 = summary.avg_colony_turn_p0
    c1 = summary.avg_colony_turn_p1
    print(f"Avg first colony turn P0: {c0:.1f}" if c0 is not None else "Avg first colony turn P0: n/a")
    print(f"Avg first colony turn P1: {c1:.1f}" if c1 is not None else "Avg first colony turn P1: n/a")


if __name__ == "__main__":
    main()
