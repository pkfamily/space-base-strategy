from spacebase2p.game import BuyAction, BuyKind, Game, Market
from spacebase2p.bots import RandomBot
import random

from spacebase2p.models import PlayerState, ShipCard, SideEffects


def test_income_refill_only_after_purchase():
    rng = random.Random(0)
    bots = [RandomBot(rng), RandomBot(rng)]
    game = Game.new(bots, seed=1)
    p = game.players[0]
    p.gold = 2
    p.income = 5
    game._resolve_buy(0, BuyAction(BuyKind.PASS))
    assert p.gold == 2

    card = ShipCard(
        "cheap",
        3,
        1,
        2,
        SideEffects(),
        SideEffects(),
    )
    game.market = Market.new(rng)
    game.market.face_l1.insert(0, card)
    p.gold = 4
    p.income = 5
    game._resolve_buy(0, BuyAction(BuyKind.SHIP, ship=card))
    assert p.gold == 5
