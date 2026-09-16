from __future__ import annotations

import random
from typing import Sequence

from spacebase2p.bot_policy import (
    best_colony,
    pick_ship_buy,
    should_race_colonies,
    worth_buying,
)
from spacebase2p.dice import Roll, legal_allocation_modes, sector_hits
from spacebase2p.game import BuyAction, BuyKind, Game, legal_colony_buys, legal_ship_buys
from spacebase2p.models import AllocationMode
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
        return self.rng.choice(legal_allocation_modes(roll))

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
    """Stack income to target, then race colonies; pass on leaky buys."""

    def __init__(self, rng: random.Random, target_income: int | None = None) -> None:
        self.rng = rng
        self.target_income = target_income or rng.randint(5, 7)

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
        colonies = legal_colony_buys(player, game.market)
        ships = legal_ship_buys(player, game.market)

        if should_race_colonies(game, player_idx):
            best = best_colony(colonies)
            if best and worth_buying(player.gold, best.cost, keystone=True):
                return BuyAction(BuyKind.COLONY, colony=best)

        if player.income < self.target_income:
            action = pick_ship_buy(game, player_idx, ships, prefer="income")
            if action:
                return action

        if colonies:
            best = best_colony(colonies)
            if best and worth_buying(player.gold, best.cost, keystone=should_race_colonies(game, player_idx)):
                return BuyAction(BuyKind.COLONY, colony=best)

        action = pick_ship_buy(
            game,
            player_idx,
            ships,
            prefer="income",
            keystone_filter=lambda c: c.station.income > 0 and c.station.arrow_right,
        )
        if action:
            return action

        return BuyAction(BuyKind.PASS)


class RushBot:
    """1–6 engines, then colony race; pass on overspend."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

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
        colonies = legal_colony_buys(player, game.market)
        ships = legal_ship_buys(player, game.market)

        if should_race_colonies(game, player_idx):
            best = best_colony(colonies)
            if best and worth_buying(player.gold, best.cost, keystone=True):
                return BuyAction(BuyKind.COLONY, colony=best)

        if not should_race_colonies(game, player_idx):
            action = pick_ship_buy(game, player_idx, ships, prefer="rush")
            if action:
                return action

        if colonies:
            best = best_colony(colonies)
            if best and worth_buying(player.gold, best.cost, keystone=True):
                return BuyAction(BuyKind.COLONY, colony=best)

        action = pick_ship_buy(game, player_idx, ships, prefer="rush")
        if action:
            return action

        return BuyAction(BuyKind.PASS)


def make_bot_pair(names: Sequence[str], rng: random.Random) -> list:
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
