from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class AllocationMode(Enum):
    SINGLES = "singles"
    SUM = "sum"


@dataclass(frozen=True)
class SideEffects:
    """Station (blue) or deployed (red) rewards — supported effect types only."""

    gold: int = 0
    income: int = 0
    vp: int = 0
    rockets: int = 0
    arrow_left: bool = False
    arrow_right: bool = False

    def rocket_vp(self) -> int:
        return self.rockets

    @property
    def has_arrow(self) -> bool:
        return self.arrow_left or self.arrow_right


@dataclass(frozen=True)
class ShipCard:
    id: str
    sector: int
    level: int
    cost: int
    station: SideEffects
    deployed: SideEffects


@dataclass
class ColonyOffer:
    sector: int
    vp: int = 1
    cost: int = 3


@dataclass
class SectorState:
    stationed: ShipCard | None = None
    deployed: list[ShipCard] = field(default_factory=list)
    colony: bool = False


@dataclass
class PlayerState:
    gold: int = 0
    income: int = 0
    vp: int = 0
    sectors: dict[int, SectorState] = field(default_factory=dict)

    def sector(self, n: int) -> SectorState:
        if n not in self.sectors:
            self.sectors[n] = SectorState()
        return self.sectors[n]


ArrowChoice = Literal["left", "right"] | None
