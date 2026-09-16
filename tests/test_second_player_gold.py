import random

from spacebase2p.bots import make_bot_pair
from spacebase2p.game import Game


def _opening_cost(player) -> int:
    for sector in range(1, 13):
        st = player.sector(sector)
        if st.stationed is not None:
            return st.stationed.cost
    raise AssertionError("no opening ship")


def test_second_player_gets_plus_one_gold():
    rng = random.Random(0)
    saw_p0_second = saw_p1_second = False
    for seed in range(300):
        bots = make_bot_pair(["rush", "rush"], rng)
        g = Game.new(bots, seed=seed)
        starter = g.active
        second = 1 - starter
        p0, p1 = g.players
        c0, c1 = _opening_cost(p0), _opening_cost(p1)
        assert p0.gold == 5 - c0 + (1 if second == 0 else 0)
        assert p1.gold == 5 - c1 + (1 if second == 1 else 0)
        if second == 0:
            saw_p0_second = True
        else:
            saw_p1_second = True
    assert saw_p0_second and saw_p1_second
