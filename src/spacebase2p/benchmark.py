from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field

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
    ("chain", "rush"),
    ("chain", "income"),
    ("rush", "chain"),
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
    median_turns: float
    avg_overspend_p0: float
    avg_overspend_p1: float
    avg_passes_p0: float
    avg_passes_p1: float
    avg_colony_turn_p0: float | None
    avg_colony_turn_p1: float | None
    avg_vp_margin: float
    avg_vp_colonies_p0: float = 0.0
    avg_vp_colonies_p1: float = 0.0
    avg_vp_dice_p0: float = 0.0
    avg_vp_dice_p1: float = 0.0
    turn_samples: list[int] = field(default_factory=list)

    @property
    def p0_win_rate(self) -> float:
        if self.finished == 0:
            return 0.0
        return 100.0 * self.p0_wins / self.finished


def play_one(
    p0: str,
    p1: str,
    seed: int,
    max_turns: int = 800,
) -> Game | None:
    gr = random.Random(seed)
    bots = make_bot_pair([p0, p1], gr)
    g = Game.new(bots, seed=gr.randint(0, 2**31 - 1))
    t = 0
    while not g.is_finished() and t < max_turns:
        g.play_turn()
        t += 1
    if not g.is_finished():
        return None
    return g


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
    passes0 = passes1 = 0
    vp_col0 = vp_col1 = 0
    vp_dice0 = vp_dice1 = 0
    turns_list: list[int] = []
    margins: list[int] = []
    colony0: list[int] = []
    colony1: list[int] = []

    for _ in range(games):
        g = play_one(p0, p1, rng.randint(0, 2**31 - 1), max_turns=max_turns)
        if g is None:
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
        passes0 += g.stats[0].pass_count
        passes1 += g.stats[1].pass_count
        vp_col0 += g.stats[0].vp_from_colonies
        vp_col1 += g.stats[1].vp_from_colonies
        vp_dice0 += g.stats[0].vp_from_dice
        vp_dice1 += g.stats[1].vp_from_dice
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

    med_turns = statistics.median(turns_list) if turns_list else 0.0

    return MatchupResult(
        p0=p0,
        p1=p1,
        games=games,
        finished=finished,
        p0_wins=p0_wins,
        p1_wins=p1_wins,
        draws=draws,
        avg_turns=avg(turns_list),
        median_turns=float(med_turns),
        avg_overspend_p0=overspend0 / finished if finished else 0.0,
        avg_overspend_p1=overspend1 / finished if finished else 0.0,
        avg_passes_p0=passes0 / finished if finished else 0.0,
        avg_passes_p1=passes1 / finished if finished else 0.0,
        avg_colony_turn_p0=avg_opt(colony0),
        avg_colony_turn_p1=avg_opt(colony1),
        avg_vp_margin=avg(margins),
        avg_vp_colonies_p0=vp_col0 / finished if finished else 0.0,
        avg_vp_colonies_p1=vp_col1 / finished if finished else 0.0,
        avg_vp_dice_p0=vp_dice0 / finished if finished else 0.0,
        avg_vp_dice_p1=vp_dice1 / finished if finished else 0.0,
        turn_samples=turns_list,
    )


def run_all_matchups(
    games: int = 800,
    seed: int = 42,
    max_turns: int = 800,
) -> list[MatchupResult]:
    results: list[MatchupResult] = []
    for i, (a, b) in enumerate(DEFAULT_MATCHUPS):
        # Separate RNG stream per matchup so parallel rows are not replaying the same game seeds.
        matchup_seed = seed + i * 100_003
        results.append(run_matchup(a, b, games=games, seed=matchup_seed, max_turns=max_turns))
    return results


def rush_mirror_turns(games: int = 120, seed: int = 99) -> list[int]:
    return run_matchup("rush", "rush", games=games, seed=seed).turn_samples
