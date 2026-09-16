from __future__ import annotations

import random
from dataclasses import dataclass

from spacebase2p.bots import make_bot_pair
from spacebase2p.game import Game

DEFAULT_MATCHUPS: list[tuple[str, str]] = [
    ("income", "rush"),
    ("rush", "income"),
    ("income", "income"),
    ("rush", "rush"),
    ("income", "random"),
    ("rush", "random"),
    ("random", "random"),
]


@dataclass
class MatchupResult:
    p0: str
    p1: str
    games: int
    finished: int
    p0_wins: int
    p1_wins: int
    draws: int
    avg_turns: float
    avg_overspend_p0: float
    avg_overspend_p1: float
    avg_colony_turn_p0: float | None
    avg_colony_turn_p1: float | None
    avg_vp_margin: float

    @property
    def p0_win_rate(self) -> float:
        if self.finished == 0:
            return 0.0
        return 100.0 * self.p0_wins / self.finished


def run_matchup(
    p0: str,
    p1: str,
    games: int = 800,
    seed: int = 42,
    max_turns: int = 800,
) -> MatchupResult:
    rng = random.Random(seed)
    p0_wins = p1_wins = draws = unfinished = 0
    overspend0 = overspend1 = 0
    turns_list: list[int] = []
    margins: list[int] = []
    colony0: list[int] = []
    colony1: list[int] = []

    for _ in range(games):
        gr = random.Random(rng.randint(0, 2**31 - 1))
        bots = make_bot_pair([p0, p1], gr)
        g = Game.new(bots, seed=gr.randint(0, 2**31 - 1))
        t = 0
        while not g.is_finished() and t < max_turns:
            g.play_turn()
            t += 1
        if not g.is_finished():
            unfinished += 1
            continue
        w = g.winner()
        if w == 0:
            p0_wins += 1
        elif w == 1:
            p1_wins += 1
        else:
            draws += 1
        overspend0 += g.stats[0].overspend_total
        overspend1 += g.stats[1].overspend_total
        turns_list.append(g.turn_number)
        margins.append(abs(g.players[0].vp - g.players[1].vp))
        if g.stats[0].first_colony_turn is not None:
            colony0.append(g.stats[0].first_colony_turn)
        if g.stats[1].first_colony_turn is not None:
            colony1.append(g.stats[1].first_colony_turn)

    finished = games - unfinished
    def avg(xs: list[int]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    def avg_opt(xs: list[int]) -> float | None:
        return avg(xs) if xs else None

    return MatchupResult(
        p0=p0,
        p1=p1,
        games=games,
        finished=finished,
        p0_wins=p0_wins,
        p1_wins=p1_wins,
        draws=draws,
        avg_turns=avg(turns_list),
        avg_overspend_p0=overspend0 / finished if finished else 0.0,
        avg_overspend_p1=overspend1 / finished if finished else 0.0,
        avg_colony_turn_p0=avg_opt(colony0),
        avg_colony_turn_p1=avg_opt(colony1),
        avg_vp_margin=avg(margins),
    )


def run_all_matchups(
    games: int = 800,
    seed: int = 42,
    max_turns: int = 800,
) -> list[MatchupResult]:
    return [run_matchup(a, b, games=games, seed=seed, max_turns=max_turns) for a, b in DEFAULT_MATCHUPS]
