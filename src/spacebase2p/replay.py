from __future__ import annotations

from spacebase2p.bots import make_bot_pair
from spacebase2p.game import BuyAction, BuyKind, Game


def format_buy(action: BuyAction) -> str:
    if action.kind == BuyKind.PASS:
        return "PASS"
    if action.kind == BuyKind.SHIP and action.ship:
        return f"BUY ship {action.ship.id} (s{action.ship.sector}, {action.ship.cost}g)"
    if action.kind == BuyKind.COLONY and action.colony:
        return f"BUY colony s{action.colony.sector} (+{action.colony.vp} VP, {action.colony.cost}g)"
    return "?"


def run_replay(
    p0: str,
    p1: str,
    seed: int,
    max_turns: int = 200,
) -> list[str]:
    import random

    rng = random.Random(seed)
    bots = make_bot_pair([p0, p1], rng)
    game = Game.new(bots, seed=seed)
    lines: list[str] = [
        f"seed={seed}  Player1={p0}  Player2={p1}  first_roller=Player{game.active + 1}",
        "",
    ]

    turns = 0
    while not game.is_finished() and turns < max_turns:
        active = game.active
        lines.append(f"--- Round {game.turn_number}  Player {active + 1} to act ---")
        for pidx in range(2):
            p = game.players[pidx]
            lines.append(f"  Player {pidx + 1} before: {p.vp} VP, {p.gold}g, inc {p.income}")

        game.play_turn()
        turns += 1

        for pidx in range(2):
            p = game.players[pidx]
            st = game.stats[pidx]
            lines.append(
                f"  Player {pidx + 1} after:  {p.vp} VP, {p.gold}g  "
                f"(colony VP {st.vp_from_colonies}, dice VP {st.vp_from_dice}, passes {st.pass_count})"
            )
        lines.append("")

        if game.is_finished():
            break

    if game.is_finished():
        w = game.winner()
        lines.append(
            f"GAME OVER  winner=Player {w + 1}" if w is not None else "GAME OVER  DRAW"
        )
    else:
        lines.append("STOPPED (turn cap)")
    return lines
