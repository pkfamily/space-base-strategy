from __future__ import annotations

import random
from typing import Iterator

from spacebase2p.models import ColonyOffer, ShipCard, SideEffects

# Representative base-game-style deck (no charge, You Win, Gordon, swap, dice-fix).


def _card(
    cid: str,
    sector: int,
    level: int,
    cost: int,
    sb: tuple[int, int, int, int, bool, bool],
    db: tuple[int, int, int, int, bool, bool],
) -> ShipCard:
    def side(t: tuple[int, int, int, int, bool, bool]) -> SideEffects:
        g, inc, vp, rockets, al, ar = t
        return SideEffects(g, inc, vp, rockets, al, ar)

    return ShipCard(cid, sector, level, cost, side(sb), side(db))


def level1_deck() -> list[ShipCard]:
    cards = [
        _card("L1-6-2g", 6, 1, 3, (2, 0, 0, 0, False, False), (0, 0, 1, 0, False, False)),
        _card("L1-5-2g", 5, 1, 3, (2, 0, 0, 0, False, False), (0, 0, 0, 1, False, False)),
        _card("L1-4-2g", 4, 1, 3, (2, 0, 0, 0, False, False), (1, 0, 0, 0, False, False)),
        _card("L1-6-inc", 6, 1, 3, (1, 1, 0, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L1-7-inc", 7, 1, 3, (1, 1, 0, 0, False, False), (0, 1, 0, 0, False, False)),
        _card("L1-8-inc", 8, 1, 3, (2, 1, 0, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L1-3-1g", 3, 1, 2, (1, 0, 0, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L1-2-1g", 2, 1, 2, (1, 0, 0, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L1-1-vp", 1, 1, 2, (0, 0, 1, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L1-7-g", 7, 1, 3, (2, 0, 0, 0, False, False), (0, 0, 1, 0, False, False)),
        _card("L1-5-rkt", 5, 1, 3, (1, 0, 0, 0, False, False), (0, 0, 0, 2, False, False)),
        _card("L1-6-rkt", 6, 1, 3, (1, 0, 0, 0, False, False), (0, 0, 0, 2, False, False)),
    ]
    return cards


def level2_deck() -> list[ShipCard]:
    return [
        _card("L2-7-arr", 7, 2, 5, (0, 0, 0, 0, False, True), (0, 0, 0, 0, False, False)),
        _card("L2-8-arr", 8, 2, 5, (0, 0, 0, 0, False, True), (0, 0, 1, 0, False, False)),
        _card("L2-9-arr", 9, 2, 6, (0, 0, 0, 0, False, True), (0, 0, 0, 0, False, False)),
        _card("L2-10-vp", 10, 2, 6, (0, 0, 3, 0, False, False), (0, 0, 2, 0, False, False)),
        _card("L2-8-inc2", 8, 2, 5, (1, 2, 0, 0, False, False), (0, 0, 0, 0, False, False)),
        _card("L2-6-cargo", 6, 2, 4, (3, 0, 0, 0, False, False), (0, 0, 0, 1, False, False)),
        _card("L2-5-cargo", 5, 2, 4, (3, 0, 0, 0, False, False), (0, 0, 0, 1, False, False)),
        _card("L2-4-cargo", 4, 2, 4, (3, 0, 0, 0, False, False), (1, 0, 0, 0, False, False)),
        _card("L2-11-vp", 11, 2, 7, (0, 0, 4, 0, False, False), (0, 0, 2, 0, False, False)),
        _card("L2-9-gvp", 9, 2, 6, (2, 0, 2, 0, False, False), (0, 0, 1, 0, False, False)),
        _card("L2-7-left", 7, 2, 5, (0, 0, 0, 0, True, False), (0, 0, 0, 0, False, False)),
        _card("L2-6-rkt3", 6, 2, 5, (2, 0, 0, 0, False, False), (0, 0, 0, 3, False, False)),
    ]


def level3_deck() -> list[ShipCard]:
    return [
        _card("L3-9-vp", 9, 3, 8, (0, 0, 5, 0, False, False), (0, 0, 3, 0, False, False)),
        _card("L3-10-vp", 10, 3, 8, (0, 0, 6, 0, False, False), (0, 0, 3, 0, False, False)),
        _card("L3-8-inc", 8, 3, 7, (2, 2, 0, 0, False, False), (0, 1, 0, 0, False, False)),
        _card("L3-6-rkt", 6, 3, 7, (3, 0, 0, 0, False, False), (0, 0, 0, 4, False, False)),
        _card("L3-11-arr", 11, 3, 9, (0, 0, 2, 0, False, True), (0, 0, 2, 0, False, False)),
        _card("L3-12-vp", 12, 3, 9, (0, 0, 7, 0, False, False), (0, 0, 4, 0, False, False)),
        _card("L3-7-chain", 7, 3, 7, (1, 1, 0, 0, False, True), (0, 0, 1, 0, False, False)),
        _card("L3-5-rkt", 5, 3, 6, (2, 0, 0, 0, False, False), (0, 0, 0, 3, False, False)),
        _card("L3-4-gold", 4, 3, 6, (4, 0, 0, 0, False, False), (2, 0, 0, 0, False, False)),
    ]


def shuffled_decks(rng: random.Random) -> tuple[list[ShipCard], list[ShipCard], list[ShipCard]]:
    d1 = level1_deck()[:]
    d2 = level2_deck()[:]
    d3 = level3_deck()[:]
    rng.shuffle(d1)
    rng.shuffle(d2)
    rng.shuffle(d3)
    return d1, d2, d3


def colony_offers() -> list[ColonyOffer]:
    return [ColonyOffer(sector=s, vp=1, cost=3) for s in range(1, 13)]


def draw_opening_level1(rng: random.Random) -> ShipCard:
    deck = level1_deck()
    return rng.choice(deck)
