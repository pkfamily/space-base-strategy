from __future__ import annotations

import argparse
import sys

from spacebase2p.replay import run_replay
from spacebase2p.simulate import run_simulation


def cmd_simulate(args: argparse.Namespace) -> None:
    summary = run_simulation(args.games, args.p0, args.p1, seed=args.seed)
    g = summary.games
    print(f"Games: {g}")
    print(f"Player 1 (--p0, {args.p0}) wins: {summary.p0_wins} ({100 * summary.p0_wins / g:.1f}%)")
    print(f"Player 2 (--p1, {args.p1}) wins: {summary.p1_wins} ({100 * summary.p1_wins / g:.1f}%)")
    print(f"Draws: {summary.draws} ({100 * summary.draws / g:.1f}%)")
    print(f"Avg overspend Player 1: {summary.avg_overspend_p0:.2f}")
    print(f"Avg overspend Player 2: {summary.avg_overspend_p1:.2f}")
    c0 = summary.avg_colony_turn_p0
    c1 = summary.avg_colony_turn_p1
    if c0 is not None:
        print(f"Avg first colony turn Player 1: {c0:.1f}")
    else:
        print("Avg first colony turn Player 1: n/a")
    if c1 is not None:
        print(f"Avg first colony turn Player 2: {c1:.1f}")
    else:
        print("Avg first colony turn Player 2: n/a")


def cmd_replay(args: argparse.Namespace) -> None:
    lines = run_replay(args.p0, args.p1, seed=args.seed, max_turns=args.max_turns)
    text = "\n".join(lines)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Wrote {args.output}")
    else:
        print(text)


def main(argv: list[str] | None = None) -> None:
    raw = list(argv) if argv is not None else sys.argv[1:]
    if raw and raw[0] not in ("simulate", "replay"):
        raw = ["simulate"] + raw

    parser = argparse.ArgumentParser(description="spacebase2p — 2-player Space Base simulator")
    sub = parser.add_subparsers(dest="command", required=True)

    sim = sub.add_parser("simulate", help="run N games")
    sim.add_argument("-n", "--games", type=int, default=100)
    sim.add_argument("--p0", default="income", help="Player 1 bot (income|rush|chain|snowball|random)")
    sim.add_argument("--p1", default="rush", help="Player 2 bot (seat; +1g if this seat rolls second)")
    sim.add_argument("--seed", type=int, default=None)
    sim.set_defaults(func=cmd_simulate)

    rep = sub.add_parser("replay", help="print a single annotated game")
    rep.add_argument("--p0", default="chain")
    rep.add_argument("--p1", default="rush")
    rep.add_argument("--seed", type=int, default=1)
    rep.add_argument("--max-turns", type=int, default=200)
    rep.add_argument("-o", "--output", help="write log to file")
    rep.set_defaults(func=cmd_replay)

    args = parser.parse_args(raw)
    args.func(args)


if __name__ == "__main__":
    main()
