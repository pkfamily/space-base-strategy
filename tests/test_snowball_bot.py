import random

from spacebase2p.benchmark import run_matchup
from spacebase2p.bots import SnowballBot, make_bot_pair


def test_snowball_bot_registered():
    rng = random.Random(0)
    bots = make_bot_pair(["snowball", "rush"], rng)
    assert isinstance(bots[0], SnowballBot)


def test_snowball_competitive_vs_rush():
    r = run_matchup("snowball", "rush", games=200, seed=42)
    assert r.p0_win_rate >= 40.0
    assert r.avg_overspend_p0 < 35.0
