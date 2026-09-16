from __future__ import annotations

from dataclasses import dataclass

from spacebase2p.models import AllocationMode


@dataclass(frozen=True)
class Roll:
    d1: int
    d2: int

    @property
    def is_doubles(self) -> bool:
        return self.d1 == self.d2

    @property
    def sum_value(self) -> int:
        return self.d1 + self.d2


@dataclass(frozen=True)
class SectorHit:
    sector: int
    times: int


def sector_hits(roll: Roll, mode: AllocationMode) -> list[SectorHit]:
    """Which sectors activate and how many times (before opponent-specific resolution)."""
    if mode == AllocationMode.SUM:
        return [SectorHit(roll.sum_value, 1)]

    if roll.is_doubles:
        return [SectorHit(roll.d1, 2)]

    if roll.d1 == roll.d2:
        return [SectorHit(roll.d1, 2)]

    return [SectorHit(roll.d1, 1), SectorHit(roll.d2, 1)]


def legal_allocation_modes(roll: Roll) -> list[AllocationMode]:
    modes = [AllocationMode.SINGLES]
    s = roll.sum_value
    if 2 <= s <= 12:
        modes.append(AllocationMode.SUM)
    return modes
