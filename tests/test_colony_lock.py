from spacebase2p.game import BuyAction, BuyKind, Game, legal_ship_buys, _place_colony
from spacebase2p.bots import RandomBot
import random

from spacebase2p.models import ColonyOffer, PlayerState, ShipCard, SideEffects


def test_cannot_buy_ship_in_colony_sector():
    rng = random.Random(0)
    game = Game.new([RandomBot(rng), RandomBot(rng)], seed=2)
    p = game.players[0]
    _place_colony(p, ColonyOffer(sector=5))
    card = ShipCard("x", 5, 1, 2, SideEffects(), SideEffects())
    game.market.face_l1.append(card)
    p.gold = 10
    assert card not in legal_ship_buys(p, game.market)
    before = p.gold
    game._resolve_buy(0, BuyAction(BuyKind.SHIP, ship=card))
    assert p.gold == before
