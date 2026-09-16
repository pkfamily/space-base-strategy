from __future__ import annotations

import random
from typing import Sequence

from spacebase2p.dice import Roll, legal_allocation_modes, sector_hits
from spacebase2p.game import BuyAction, BuyKind, Game, legal_colony_buys, legal_ship_buys
from spacebase2p.models import AllocationMode, ColonyOffer, ShipCard
from spacebase2p.rewards import evaluate_roll


def _greedy_arrows(_game: Game, _pidx: int, options: list[str]) -> str:
    return options[0]


def _best_allocation(
    game: Game,
    pidx: int,
    roll: Roll,
    active_idx: int,
) -> AllocationMode:
    player = game.players[pidx]
    is_active = pidx == active_idx
    best_mode = AllocationMode.SINGLES
    best_score = -1.0

    for mode in legal_allocation_modes(roll):
        hits = sector_hits(roll, mode)
        sectors_times = [(h.sector, h.times) for h in hits]
        delta = evaluate_roll(
            player,
            sectors_times,
            is_active,
            mode,
            lambda opts: opts[0] if opts else None,
        )
        score = delta.vp * 3 + delta.gold + delta.income * 2
        if score > best_score:
            best_score = score
            best_mode = mode
    return best_mode


class RandomBot:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        modes = legal_allocation_modes(roll)
        return self.rng.choice(modes)

    def choose_arrows(self, game: Game, player_idx: int, options: list[str]) -> str:
        return self.rng.choice(options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        player = game.players[player_idx]
        ships = legal_ship_buys(player, game.market)
        colonies = legal_colony_buys(player, game.market)
        options: list[BuyAction] = [BuyAction(BuyKind.PASS)]
        options.extend(BuyAction(BuyKind.SHIP, ship=c) for c in ships)
        options.extend(BuyAction(BuyKind.COLONY, colony=c) for c in colonies)
        return self.rng.choice(options)


class IncomeBot:
    """Buy income until 5–8, then prioritize colonies."""

    def __init__(self, rng: random.Random, target_income: int | None = None) -> None:
        self.rng = rng
        self.target_income = target_income or rng.randint(5, 8)

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        return _best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(self, game: Game, player_idx: int, options: list[str]) -> str:
        return _greedy_arrows(game, player_idx, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        player = game.players[player_idx]
        if player.income < self.target_income:
            ships = legal_ship_buys(player, game.market)
            income_cards = [c for c in ships if c.station.income > 0]
            if income_cards:
                return BuyAction(BuyKind.SHIP, ship=max(income_cards, key=lambda c: c.station.income))
            if ships:
                return BuyAction(BuyKind.SHIP, ship=ships[0])

        colonies = legal_colony_buys(player, game.market)
        if colonies:
            return BuyAction(BuyKind.COLONY, colony=colonies[0])

        ships = legal_ship_buys(player, game.market)
        if ships:
            return BuyAction(BuyKind.SHIP, ship=ships[0])
        return BuyAction(BuyKind.PASS)


class RushBot:
    """Early cargo/rockets on 1–6, colonies from ~20 VP."""

    def __init__(self, rng: random.Random, colony_threshold: int = 20) -> None:
        self.rng = rng
        self.colony_threshold = colony_threshold

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        return _best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(self, game: Game, player_idx: int, options: list[str]) -> str:
        return _greedy_arrows(game, player_idx, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        player = game.players[player_idx]
        ships = legal_ship_buys(player, game.market)

        if player.vp < self.colony_threshold:
            low = [c for c in ships if 1 <= c.sector <= 6]
            rockets = [c for c in low if c.deployed.rockets > 0]
            cargo = [c for c in low if c.station.gold >= 2]
            if rockets:
                return BuyAction(BuyKind.SHIP, ship=max(rockets, key=lambda c: c.deployed.rockets))
            if cargo:
                return BuyAction(BuyKind.SHIP, ship=max(cargo, key=lambda c: c.station.gold))

        colonies = legal_colony_buys(player, game.market)
        if colonies and player.vp >= self.colony_threshold - 5:
            return BuyAction(BuyKind.COLONY, colony=colonies[0])

        if ships:
            return BuyAction(BuyKind.SHIP, ship=ships[0])
        return BuyAction(BuyKind.PASS)


def make_bot_pair(
    names: Sequence[str],
    rng: random.Random,
) -> list:
    bots = []
    for name in names:
        key = name.lower()
        if key == "income":
            bots.append(IncomeBot(rng))
        elif key == "rush":
            bots.append(RushBot(rng))
        elif key in ("random", "rand"):
            bots.append(RandomBot(rng))
        else:
            raise ValueError(f"unknown bot: {name}")
    return bots
