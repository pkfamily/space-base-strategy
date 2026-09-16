from __future__ import annotations

from spacebase2p.game import BuyAction, BuyKind, Game
from spacebase2p.models import ColonyOffer, ShipCard

# Pass if buying would waste more than this much gold (spend-all rule).
MAX_GOLD_WASTE = 2


def gold_waste(gold: int, cost: int) -> int:
    return max(0, gold - cost)


def worth_buying(gold: int, cost: int, *, keystone: bool = False) -> bool:
    if gold < cost:
        return False
    if keystone:
        return True
    return gold_waste(gold, cost) <= MAX_GOLD_WASTE


def opponent_vp(game: Game, player_idx: int) -> int:
    return game.players[game.opponent_idx(player_idx)].vp


def should_race_colonies(game: Game, player_idx: int) -> bool:
    """Closing phase: convert gold to VP like real 2p races."""
    me = game.players[player_idx]
    opp_vp = opponent_vp(game, player_idx)
    if opp_vp >= 18 or me.vp >= 15:
        return True
    if me.vp >= 12 and me.gold >= 9:
        return True
    if opp_vp >= 25:
        return True
    return False


def best_colony(colonies: list[ColonyOffer]) -> ColonyOffer | None:
    if not colonies:
        return None
    return max(colonies, key=lambda c: (c.vp / c.cost, c.vp, -c.sector))


def best_ship_for_income(ships: list[ShipCard]) -> ShipCard | None:
    income_cards = [c for c in ships if c.station.income > 0]
    if not income_cards:
        return None
    return max(income_cards, key=lambda c: (c.station.income, c.station.gold, -c.cost))


def best_ship_rush_engine(ships: list[ShipCard]) -> ShipCard | None:
    low = [c for c in ships if 1 <= c.sector <= 6]
    rockets = [c for c in low if c.deployed.rockets > 0]
    if rockets:
        return max(rockets, key=lambda c: (c.deployed.rockets, c.station.gold, -c.cost))
    cargo = [c for c in low if c.station.gold >= 2]
    if cargo:
        return max(cargo, key=lambda c: (c.station.gold, -c.cost))
    return None


def pick_ship_buy(
    game: Game,
    player_idx: int,
    ships: list[ShipCard],
    *,
    prefer: str,
    keystone_filter=None,
) -> BuyAction | None:
    player = game.players[player_idx]
    gold = player.gold

    if prefer == "income":
        card = best_ship_for_income(ships)
    else:
        card = best_ship_rush_engine(ships)

    if card is None and ships:
        affordable = [c for c in ships if worth_buying(gold, c.cost)]
        card = min(affordable, key=lambda c: c.cost) if affordable else None

    if card is None:
        return None

    keystone = keystone_filter(card) if keystone_filter else False
    if worth_buying(gold, card.cost, keystone=keystone):
        return BuyAction(BuyKind.SHIP, ship=card)
    return None
