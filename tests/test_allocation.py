from spacebase2p.dice import Roll, sector_hits
from spacebase2p.models import AllocationMode


def test_singles_different_dice():
    hits = sector_hits(Roll(2, 5), AllocationMode.SINGLES)
    assert [(h.sector, h.times) for h in hits] == [(2, 1), (5, 1)]


def test_sum_allocation():
    hits = sector_hits(Roll(2, 5), AllocationMode.SUM)
    assert [(h.sector, h.times) for h in hits] == [(7, 1)]


def test_sum_on_doubles_uses_sum_sector_once():
    hits = sector_hits(Roll(4, 4), AllocationMode.SUM)
    assert [(h.sector, h.times) for h in hits] == [(8, 1)]
