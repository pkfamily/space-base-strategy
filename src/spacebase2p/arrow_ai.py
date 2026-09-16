from __future__ import annotations

from spacebase2p.dice import Roll, legal_allocation_modes, sector_hits
from spacebase2p.game import Game
from spacebase2p.models import AllocationMode, ArrowChoice, PlayerState
from spacebase2p.rewards import RewardDelta, _apply_side, evaluate_roll


def _score_delta(delta: RewardDelta) -> float:
    return delta.vp * 3.0 + delta.gold + delta.income * 2.0


def sector_standing_value(player: PlayerState, sector: int, active_player_turn: bool) -> float:
    """Heuristic value of a sector's blue or red rewards (no arrows)."""
    st = player.sector(sector)
    delta = RewardDelta()
    if active_player_turn:
        if st.colony or st.stationed is None:
            return 0.0
        _apply_side(st.stationed.station, delta)
    else:
        for card in st.deployed:
            _apply_side(card.deployed, delta)
    return _score_delta(delta)


def choose_arrow_direction(
    player: PlayerState,
    from_sector: int,
    active_player_turn: bool,
    options: list[ArrowChoice],
) -> ArrowChoice:
    if len(options) == 1:
        return options[0]
    best = options[0]
    best_score = -1.0
    for direction in options:
        neighbor = from_sector - 1 if direction == "left" else from_sector + 1
        if neighbor < 1 or neighbor > 12:
            continue
        score = sector_standing_value(player, neighbor, active_player_turn)
        if score > best_score:
            best_score = score
            best = direction
    return best


def best_allocation(
    game: Game,
    player_idx: int,
    roll: Roll,
    active_idx: int,
) -> AllocationMode:
    player = game.players[player_idx]
    is_active = player_idx == active_idx
    best_mode = AllocationMode.SINGLES
    best_score = -1.0

    for mode in legal_allocation_modes(roll):
        hits = sector_hits(roll, mode)
        sectors_times = [(h.sector, h.times) for h in hits]

        def chooser(options: list[ArrowChoice], from_sector: int = 0) -> ArrowChoice | None:
            if not options:
                return None
            return choose_arrow_direction(player, from_sector, is_active, options)

        delta = evaluate_roll(player, sectors_times, is_active, mode, chooser)
        score = _score_delta(delta)
        if score > best_score:
            best_score = score
            best_mode = mode
    return best_mode
