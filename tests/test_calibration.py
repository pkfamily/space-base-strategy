import statistics

from spacebase2p.benchmark import rush_mirror_turns


def test_rush_mirror_median_turns_near_2p_pace():
    """2p table games often end in under ~20 turns per player (~20 shared rounds)."""
    turns = rush_mirror_turns(games=100, seed=7)
    assert len(turns) >= 95
    med = statistics.median(turns)
    assert 14 <= med <= 22, f"median rounds {med} outside calibration band 14–22"


def test_rush_mirror_avg_overspend_not_extreme():
    from spacebase2p.benchmark import run_matchup

    r = run_matchup("rush", "rush", games=80, seed=11)
    assert r.avg_overspend_p0 < 25
    assert r.avg_overspend_p1 < 25
