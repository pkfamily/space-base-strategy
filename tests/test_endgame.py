from spacebase2p.bots import RandomBot
from spacebase2p.game import Game
import random


class PassiveBot(RandomBot):
    """Never buys; used to count turns after endgame."""

    def choose_buy(self, game, player_idx):
        from spacebase2p.game import BuyAction, BuyKind

        return BuyAction(BuyKind.PASS)


def test_endgame_gives_opponent_one_more_turn():
    rng = random.Random(0)
    bots = [PassiveBot(rng), PassiveBot(rng)]
    game = Game.new(bots, seed=10)
    game.players[0].vp = 40
    game._check_endgame_trigger(0)
    assert game.final_turn_player == 1
    assert not game.game_over

    game.active = 1
    game.play_turn()
    assert game.game_over

    w = game.winner()
    assert w in (0, 1, None)


def test_winner_higher_vp_after_final_turn():
    rng = random.Random(0)
    bots = [PassiveBot(rng), PassiveBot(rng)]
    game = Game.new(bots, seed=11)
    game.players[0].vp = 42
    game.players[1].vp = 38
    game.endgame_triggered = True
    game.final_turn_player = 1
    game.active = 1
    game.play_turn()
    assert game.winner() == 0


def test_tie_is_draw():
    rng = random.Random(0)
    game = Game.new([PassiveBot(rng), PassiveBot(rng)], seed=12)
    game.players[0].vp = 41
    game.players[1].vp = 41
    game.endgame_triggered = True
    game.final_turn_player = 1
    game.active = 1
    game.game_over = True
    assert game.winner() is None
