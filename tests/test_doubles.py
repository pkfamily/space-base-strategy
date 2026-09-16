from spacebase2p.dice import Roll, sector_hits
from spacebase2p.models import AllocationMode, PlayerState, ShipCard, SideEffects
from spacebase2p.rewards import ResolutionContext, resolve_sector_rewards


def _simple_card(sector: int, gold: int) -> ShipCard:
    side = SideEffects(gold=gold)
    return ShipCard(f"c-{sector}", sector, 1, 3, side, SideEffects())


def test_doubles_singles_hits_twice():
    hits = sector_hits(Roll(3, 3), AllocationMode.SINGLES)
    assert [(h.sector, h.times) for h in hits] == [(3, 2)]


def test_doubles_doubles_gold_twice():
    player = PlayerState()
    player.sector(4).stationed = _simple_card(4, 2)
    ctx = ResolutionContext(mode=AllocationMode.SINGLES)
    delta = resolve_sector_rewards(player, 4, True, ctx, 2, lambda _: None)
    assert delta.gold == 4
