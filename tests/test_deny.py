import random

from spacebase2p.bots import ChainBot, make_bot_pair
from spacebase2p.bot_policy import deny_colony_action
from spacebase2p.game import Game, legal_colony_buys
from spacebase2p.models import ColonyOffer


def test_deny_colony_when_opponent_close():
    rng = random.Random(0)
    g = Game.new(make_bot_pair(["rush", "rush"], rng), seed=1)
    g.players[0].gold = 12
    g.players[1].vp = 32
    g.players[1].gold = 8
    colonies = legal_colony_buys(g.players[0], g.market)
    action = deny_colony_action(g, 0, colonies)
    assert action is not None
    assert action.kind.name == "COLONY"


def test_chain_bot_exists():
    rng = random.Random(1)
    bot = ChainBot(rng)
    g = Game.new([bot, ChainBot(rng)], seed=2)
    assert bot.choose_buy(g, 0).kind is not None
