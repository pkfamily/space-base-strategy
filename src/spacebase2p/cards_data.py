from __future__ import annotations

import json
import random
from functools import lru_cache
from importlib import resources
from typing import Any

from spacebase2p.models import ColonyOffer, ShipCard, SideEffects


def _side(data: dict[str, Any] | None) -> SideEffects:
    if not data:
        return SideEffects()
    return SideEffects(
        gold=int(data.get("gold", 0)),
        income=int(data.get("income", 0)),
        vp=int(data.get("vp", 0)),
        rockets=int(data.get("rockets", 0)),
        arrow_left=bool(data.get("arrow_left", False)),
        arrow_right=bool(data.get("arrow_right", False)),
    )


def _ship(raw: dict[str, Any], level: int) -> ShipCard:
    return ShipCard(
        id=raw["id"],
        sector=int(raw["sector"]),
        level=level,
        cost=int(raw["cost"]),
        station=_side(raw.get("station")),
        deployed=_side(raw.get("deployed")),
    )


@lru_cache(maxsize=1)
def _load_ship_data() -> dict[str, list[ShipCard]]:
    text = resources.files("spacebase2p.data").joinpath("ships.json").read_text(encoding="utf-8")
    raw = json.loads(text)
    return {
        "level1": [_ship(c, 1) for c in raw["level1"]],
        "level2": [_ship(c, 2) for c in raw["level2"]],
        "level3": [_ship(c, 3) for c in raw["level3"]],
    }


@lru_cache(maxsize=1)
def _load_colony_data() -> list[ColonyOffer]:
    text = resources.files("spacebase2p.data").joinpath("colonies.json").read_text(encoding="utf-8")
    raw = json.loads(text)
    return [ColonyOffer(sector=int(c["sector"]), vp=int(c["vp"]), cost=int(c["cost"])) for c in raw]


def level1_deck() -> list[ShipCard]:
    return _load_ship_data()["level1"][:]


def level2_deck() -> list[ShipCard]:
    return _load_ship_data()["level2"][:]


def level3_deck() -> list[ShipCard]:
    return _load_ship_data()["level3"][:]


def shuffled_decks(rng: random.Random) -> tuple[list[ShipCard], list[ShipCard], list[ShipCard]]:
    d1 = level1_deck()
    d2 = level2_deck()
    d3 = level3_deck()
    rng.shuffle(d1)
    rng.shuffle(d2)
    rng.shuffle(d3)
    return d1, d2, d3


def colony_offers() -> list[ColonyOffer]:
    return _load_colony_data()[:]


def draw_opening_level1(rng: random.Random) -> ShipCard:
    return rng.choice(level1_deck())
