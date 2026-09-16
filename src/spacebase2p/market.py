from __future__ import annotations

import random
from dataclasses import dataclass, field

from spacebase2p.cards_data import colony_offers, shuffled_decks
from spacebase2p.models import ColonyOffer, ShipCard


@dataclass
class Market:
    face_l1: list[ShipCard] = field(default_factory=list)
    face_l2: list[ShipCard] = field(default_factory=list)
    face_l3: list[ShipCard] = field(default_factory=list)
    deck_l1: list[ShipCard] = field(default_factory=list)
    deck_l2: list[ShipCard] = field(default_factory=list)
    deck_l3: list[ShipCard] = field(default_factory=list)
    colonies: list[ColonyOffer] = field(default_factory=list)

    @classmethod
    def new(cls, rng: random.Random) -> Market:
        d1, d2, d3 = shuffled_decks(rng)
        m = cls(
            deck_l1=d1,
            deck_l2=d2,
            deck_l3=d3,
            colonies=colony_offers(),
        )
        m._refill_level(1, rng, initial=True)
        m._refill_level(2, rng, initial=True)
        m._refill_level(3, rng, initial=True)
        return m

    def _deck(self, level: int) -> list[ShipCard]:
        if level == 1:
            return self.deck_l1
        if level == 2:
            return self.deck_l2
        return self.deck_l3

    def _face(self, level: int) -> list[ShipCard]:
        if level == 1:
            return self.face_l1
        if level == 2:
            return self.face_l2
        return self.face_l3

    def _refill_level(self, level: int, rng: random.Random, initial: bool = False) -> None:
        face = self._face(level)
        deck = self._deck(level)
        target = 6
        while len(face) < target and deck:
            face.append(deck.pop())

    def all_ships(self) -> list[ShipCard]:
        return self.face_l1 + self.face_l2 + self.face_l3

    def remove_ship(self, card: ShipCard, rng: random.Random) -> None:
        for level in (1, 2, 3):
            face = self._face(level)
            if card in face:
                face.remove(card)
                self._refill_level(level, rng)
                return
        raise ValueError(f"card not in market: {card.id}")

    def remove_colony(self, colony: ColonyOffer) -> None:
        self.colonies = [c for c in self.colonies if c.sector != colony.sector]
