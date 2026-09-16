from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from spacebase2p.models import AllocationMode, ArrowChoice, PlayerState, ShipCard, SideEffects


@dataclass
class RewardDelta:
    gold: int = 0
    income: int = 0
    vp: int = 0


@dataclass
class ResolutionContext:
    """Tracks per-roll limits for arrow chaining."""

    mode: AllocationMode
    sector_visit_budget: dict[int, int] = field(default_factory=dict)

    def budget_for(self, sector: int) -> int:
        if self.mode == AllocationMode.SUM:
            return 1
        return self.sector_visit_budget.get(sector, 2)

    def consume(self, sector: int, times: int = 1) -> int:
        """Return how many activations are allowed for this sector now."""
        allowed = self.budget_for(sector)
        if allowed <= 0:
            return 0
        take = min(times, allowed)
        if self.mode == AllocationMode.SINGLES:
            self.sector_visit_budget[sector] = allowed - take
        return take


def _side_for_turn(card: ShipCard, active_player: bool) -> SideEffects:
    return card.station if active_player else card.deployed


def _apply_side(effects: SideEffects, delta: RewardDelta) -> None:
    delta.gold += effects.gold
    delta.income += effects.income
    delta.vp += effects.vp
    if effects.rockets:
        delta.vp += effects.rocket_vp()


def _neighbor(sector: int, direction: ArrowChoice) -> int | None:
    if direction == "left":
        n = sector - 1
    elif direction == "right":
        n = sector + 1
    else:
        return None
    if 1 <= n <= 12:
        return n
    return None


def _arrow_directions(effects: SideEffects, choose: Callable[[list[ArrowChoice]], ArrowChoice]) -> list[ArrowChoice]:
    dirs: list[ArrowChoice] = []
    if effects.arrow_left:
        dirs.append("left")
    if effects.arrow_right:
        dirs.append("right")
    if not dirs:
        return []
    if len(dirs) == 1:
        return dirs
    picked = choose(dirs)
    return [picked] if picked else []


def resolve_sector_rewards(
    player: PlayerState,
    sector: int,
    active_player_turn: bool,
    ctx: ResolutionContext,
    times: int,
    arrow_chooser: Callable[[list[ArrowChoice]], ArrowChoice],
) -> RewardDelta:
    """Resolve stationed (blue) or deployed (red) rewards for sector activations."""
    delta = RewardDelta()
    activations = ctx.consume(sector, times)
    if activations <= 0:
        return delta

    for _ in range(activations):
        _resolve_one_activation(player, sector, active_player_turn, ctx, arrow_chooser, delta)
    return delta


def _resolve_one_activation(
    player: PlayerState,
    sector: int,
    active_player_turn: bool,
    ctx: ResolutionContext,
    arrow_chooser: Callable[[list[ArrowChoice]], ArrowChoice],
    delta: RewardDelta,
) -> None:
    st = player.sector(sector)

    if active_player_turn:
        if st.colony:
            stationed = None
        else:
            stationed = st.stationed
        if stationed is not None:
            effects = stationed.station
            _apply_side(effects, delta)
            for direction in _arrow_directions(effects, arrow_chooser):
                n = _neighbor(sector, direction)
                if n is not None:
                    sub = resolve_sector_rewards(
                        player, n, active_player_turn, ctx, 1, arrow_chooser
                    )
                    delta.gold += sub.gold
                    delta.income += sub.income
                    delta.vp += sub.vp
    else:
        for card in st.deployed:
            effects = card.deployed
            _apply_side(effects, delta)
            for direction in _arrow_directions(effects, arrow_chooser):
                n = _neighbor(sector, direction)
                if n is not None:
                    sub = resolve_sector_rewards(
                        player, n, active_player_turn, ctx, 1, arrow_chooser
                    )
                    delta.gold += sub.gold
                    delta.income += sub.income
                    delta.vp += sub.vp


def apply_delta(player: PlayerState, delta: RewardDelta) -> None:
    player.gold += delta.gold
    player.income += delta.income
    player.vp += delta.vp


def evaluate_roll(
    player: PlayerState,
    sectors_and_times: list[tuple[int, int]],
    active_player_turn: bool,
    mode: AllocationMode,
    arrow_chooser: Callable[[list[ArrowChoice]], ArrowChoice],
) -> RewardDelta:
    ctx = ResolutionContext(mode=mode)
    total = RewardDelta()
    for sector, times in sectors_and_times:
        part = resolve_sector_rewards(
            player, sector, active_player_turn, ctx, times, arrow_chooser
        )
        total.gold += part.gold
        total.income += part.income
        total.vp += part.vp
    return total
