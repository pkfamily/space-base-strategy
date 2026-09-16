from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Protocol

from spacebase2p.cards_data import draw_opening_level1
from spacebase2p.dice import Roll, sector_hits
from spacebase2p.market import Market
from spacebase2p.models import AllocationMode, ColonyOffer, PlayerState, ShipCard
from spacebase2p.rewards import apply_delta, evaluate_roll


class BuyKind(Enum):
    SHIP = "ship"
    COLONY = "colony"
    PASS = "pass"


@dataclass(frozen=True)
class BuyAction:
    kind: BuyKind
    ship: ShipCard | None = None
    colony: ColonyOffer | None = None


class Bot(Protocol):
    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode: ...

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
    ) -> str: ...

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction: ...


@dataclass
class GameStats:
    overspend_total: int = 0
    first_colony_turn: int | None = None
    colony_purchases: int = 0


@dataclass
class Game:
    rng: random.Random
    players: list[PlayerState]
    market: Market
    active: int = 0
    turn_number: int = 1
    endgame_triggered: bool = False
    final_turn_player: int | None = None
    game_over: bool = False
    stats: list[GameStats] = field(default_factory=list)
    bots: list[Bot] = field(default_factory=list)

    @classmethod
    def new(cls, bots: list[Bot], seed: int | None = None) -> Game:
        rng = random.Random(seed)
        p0 = PlayerState(gold=5)
        p1 = PlayerState(gold=5)
        market = Market.new(rng)

        c0 = draw_opening_level1(rng)
        c1 = draw_opening_level1(rng)
        _station_card(p0, c0)
        _station_card(p1, c1)
        p0.gold -= c0.cost
        p1.gold -= c1.cost
        p1.gold += 1  # second player bonus

        if c0.sector >= c1.sector:
            active = 0
        else:
            active = 1

        game = cls(
            rng=rng,
            players=[p0, p1],
            market=market,
            active=active,
            stats=[GameStats(), GameStats()],
            bots=bots,
        )
        return game

    def current_player(self) -> PlayerState:
        return self.players[self.active]

    def opponent_idx(self, idx: int) -> int:
        return 1 - idx

    def roll_dice(self) -> Roll:
        return Roll(self.rng.randint(1, 6), self.rng.randint(1, 6))

    def play_turn(self) -> None:
        roll = self.roll_dice()
        active_idx = self.active

        for pidx in range(2):
            bot = self.bots[pidx]
            mode = bot.choose_allocation(self, pidx, roll, active_idx)
            is_active_turn = pidx == active_idx
            hits = sector_hits(roll, mode)

            def arrow_chooser(options: list) -> str | None:
                if not options:
                    return None
                return bot.choose_arrows(self, pidx, options)

            sectors_times = [(h.sector, h.times) for h in hits]
            delta = evaluate_roll(
                self.players[pidx],
                sectors_times,
                is_active_turn,
                mode,
                arrow_chooser,
            )
            apply_delta(self.players[pidx], delta)
            self._check_endgame_trigger(pidx)

        buy = self.bots[active_idx].choose_buy(self, active_idx)
        self._resolve_buy(active_idx, buy)

        if self.endgame_triggered and self.active == self.final_turn_player:
            self.game_over = True

        self.active = 1 - self.active
        if self.active == 0:
            self.turn_number += 1

    def _check_endgame_trigger(self, pidx: int) -> None:
        if self.endgame_triggered:
            return
        if self.players[pidx].vp >= 40:
            self.endgame_triggered = True
            self.final_turn_player = self.opponent_idx(pidx)

    def is_finished(self) -> bool:
        return self.game_over

    def winner(self) -> int | None:
        """0, 1, or None for draw."""
        if not self.is_finished():
            raise RuntimeError("game not finished")
        v0, v1 = self.players[0].vp, self.players[1].vp
        if v0 > v1:
            return 0
        if v1 > v0:
            return 1
        return None

    def _resolve_buy(self, pidx: int, action: BuyAction) -> None:
        player = self.players[pidx]
        if action.kind == BuyKind.PASS:
            return

        gold_before = player.gold
        if action.kind == BuyKind.SHIP:
            card = action.ship
            assert card is not None
            if player.gold < card.cost:
                return
            if player.sector(card.sector).colony:
                return
            player.gold = 0
            overspend = max(0, gold_before - card.cost)
            self.stats[pidx].overspend_total += overspend
            _station_card(player, card)
            self.market.remove_ship(card, self.rng)
        elif action.kind == BuyKind.COLONY:
            colony = action.colony
            assert colony is not None
            if player.gold < colony.cost:
                return
            if player.sector(colony.sector).colony:
                return
            player.gold = 0
            overspend = max(0, gold_before - colony.cost)
            self.stats[pidx].overspend_total += overspend
            _place_colony(player, colony)
            player.vp += colony.vp
            self.market.remove_colony(colony)
            self.stats[pidx].colony_purchases += 1
            if self.stats[pidx].first_colony_turn is None:
                self.stats[pidx].first_colony_turn = self.turn_number
            self._check_endgame_trigger(pidx)

        if player.gold < player.income:
            player.gold = player.income

    def run_to_completion(self, max_turns: int = 500) -> None:
        turns = 0
        while not self.is_finished() and turns < max_turns:
            self.play_turn()
            turns += 1


def _station_card(player: PlayerState, card: ShipCard) -> None:
    st = player.sector(card.sector)
    if st.stationed is not None:
        st.deployed.append(st.stationed)
    st.stationed = card


def _place_colony(player: PlayerState, colony: ColonyOffer) -> None:
    st = player.sector(colony.sector)
    if st.stationed is not None:
        st.deployed.append(st.stationed)
        st.stationed = None
    st.colony = True


def legal_ship_buys(player: PlayerState, market: Market) -> list[ShipCard]:
    out: list[ShipCard] = []
    for card in market.all_ships():
        if player.gold < card.cost:
            continue
        if player.sector(card.sector).colony:
            continue
        out.append(card)
    return out


def legal_colony_buys(player: PlayerState, market: Market) -> list[ColonyOffer]:
    out: list[ColonyOffer] = []
    for colony in market.colonies:
        if player.gold < colony.cost:
            continue
        if player.sector(colony.sector).colony:
            continue
        out.append(colony)
    return out
