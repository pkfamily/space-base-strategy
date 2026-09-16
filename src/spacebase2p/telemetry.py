from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlayerTelemetry:
    overspend_total: int = 0
    first_colony_turn: int | None = None
    colony_purchases: int = 0
    pass_count: int = 0
    vp_from_colonies: int = 0
    vp_from_dice_blue: int = 0
    vp_from_dice_red: int = 0

    @property
    def vp_from_dice(self) -> int:
        return self.vp_from_dice_blue + self.vp_from_dice_red


@dataclass
class GameTelemetry:
    """Snapshot at end of a finished game."""

    rounds: int
    winner: int | None
    players: list[PlayerTelemetry]
    unfinished: bool = False

    @property
    def total_colonies(self) -> int:
        return sum(p.colony_purchases for p in self.players)
