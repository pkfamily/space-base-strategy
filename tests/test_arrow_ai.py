from spacebase2p.arrow_ai import choose_arrow_direction
from spacebase2p.models import PlayerState, ShipCard, SideEffects


def test_arrow_chooses_higher_vp_neighbor():
    player = PlayerState()
    player.sector(7).stationed = ShipCard(
        "arr",
        7,
        2,
        5,
        SideEffects(arrow_right=True),
        SideEffects(),
    )
    player.sector(8).stationed = ShipCard("pay", 8, 2, 5, SideEffects(vp=5), SideEffects())
    player.sector(6).stationed = ShipCard("weak", 6, 1, 3, SideEffects(gold=1), SideEffects())
    pick = choose_arrow_direction(player, 7, True, ["left", "right"])
    assert pick == "right"
