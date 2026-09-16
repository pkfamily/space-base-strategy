from __future__ import annotations

import random
from dataclasses import dataclass

from spacebase2p.bots import make_bot_pair
from spacebase2p.game import Game


@dataclass
class SimulationSummary:
    games: int
    p0_wins: int
    p1_wins: int
    draws: int
    avg_overspend_p0: float
    avg_overspend_p1: float
    avg_colony_turn_p0: float | None
    avg_colony_turn_p1: float | None


def run_simulation(
    games: int,
    bot_p0: str,
    bot_p1: str,
    seed: int | None = None,
) -> SimulationSummary:
    rng = random.Random(seed)
    p0_wins = p1_wins = draws = 0
    overspend0 = overspend1 = 0
    colony_turns0: list[int] = []
    colony_turns1: list[int] = []

    for i in range(games):
        game_rng = random.Random(rng.randint(0, 2**31 - 1))
        bots = make_bot_pair([bot_p0, bot_p1], game_rng)
        game = Game.new(bots, seed=game_rng.randint(0, 2**31 - 1))
        game.run_to_completion()
        w = game.winner()
        if w == 0:
            p0_wins += 1
        elif w == 1:
            p1_wins += 1
        else:
            draws += 1
        overspend0 += game.stats[0].overspend_total
        overspend1 += game.stats[1].overspend_total
        if game.stats[0].first_colony_turn is not None:
            colony_turns0.append(game.stats[0].first_colony_turn)
        if game.stats[1].first_colony_turn is not None:
            colony_turns1.append(game.stats[1].first_colony_turn)

    def avg_colony(turns: list[int]) -> float | None:
        if not turns:
            return None
        return sum(turns) / len(turns)

    return SimulationSummary(
        games=games,
        p0_wins=p0_wins,
        p1_wins=p1_wins,
        draws=draws,
        avg_overspend_p0=overspend0 / games,
        avg_overspend_p1=overspend1 / games,
        avg_colony_turn_p0=avg_colony(colony_turns0),
        avg_colony_turn_p1=avg_colony(colony_turns1),
    )
