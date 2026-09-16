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


def opponent_gold(game: Game, player_idx: int) -> int:
    return game.players[game.opponent_idx(player_idx)].gold


def opponent_needs_close(game: Game, player_idx: int) -> bool:
    opp = game.players[game.opponent_idx(player_idx)]
    return opp.vp >= 28 or (opp.vp >= 24 and opp.gold >= 6)


def deny_colony_action(
    game: Game,
    player_idx: int,
    colonies: list[ColonyOffer],
) -> BuyAction | None:
    """Take a high-VP colony when the opponent is threatening to close."""
    if not opponent_needs_close(game, player_idx):
        return None
    player = game.players[player_idx]
    affordable = [c for c in colonies if worth_buying(player.gold, c.cost, keystone=True)]
    if not affordable:
        return None
    return BuyAction(BuyKind.COLONY, colony=max(affordable, key=lambda c: (c.vp, -c.sector)))


def _arrow_target_value(game: Game, player_idx: int, card: ShipCard) -> float:
    """How juicy is the sector this arrow would feed on our board?"""
    player = game.players[player_idx]
    sector = card.sector
    total = 0.0
    if card.station.arrow_right and sector < 12:
        total += sector_standing_value(player, sector + 1, True)
    if card.station.arrow_left and sector > 1:
        total += sector_standing_value(player, sector - 1, True)
    return total


def sector_standing_value(player, sector: int, active_player_turn: bool) -> float:
    from spacebase2p.rewards import RewardDelta, _apply_side

    st = player.sector(sector)
    delta = RewardDelta()
    if active_player_turn:
        if st.colony or st.stationed is None:
            return 0.0
        _apply_side(st.stationed.station, delta)
    else:
        for c in st.deployed:
            _apply_side(c.deployed, delta)
    return delta.vp * 3 + delta.gold + delta.income * 2


def deny_arrow_ship(ships: list[ShipCard], game: Game, player_idx: int) -> ShipCard | None:
    """Hate-draft arrows on 7–11 that feed strong neighbors or block opponent chains."""
    opp = game.players[game.opponent_idx(player_idx)]
    candidates = [
        c
        for c in ships
        if 7 <= c.sector <= 11 and c.station.has_arrow and worth_buying(game.players[player_idx].gold, c.cost, keystone=True)
    ]
    if not candidates:
        return None

    def opp_chain_value(card: ShipCard) -> float:
        v = 0.0
        s = card.sector
        if card.station.arrow_right and s < 12:
            v += sector_standing_value(opp, s + 1, False)
        if card.station.arrow_left and s > 1:
            v += sector_standing_value(opp, s - 1, False)
        return v

    return max(candidates, key=lambda c: (opp_chain_value(c), _arrow_target_value(game, player_idx, c), -c.cost))


def best_chain_ship(ships: list[ShipCard], game: Game, player_idx: int) -> ShipCard | None:
    player = game.players[player_idx]
    arrows = [
        c
        for c in ships
        if 7 <= c.sector <= 11 and c.station.has_arrow
    ]
    if not arrows:
        return None
    affordable = [c for c in arrows if worth_buying(player.gold, c.cost, keystone=c.station.has_arrow)]
    if not affordable:
        return None
    return max(affordable, key=lambda c: (_arrow_target_value(game, player_idx, c), c.station.vp, -c.cost))


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
