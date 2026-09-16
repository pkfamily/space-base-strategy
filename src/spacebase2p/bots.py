from __future__ import annotations

import random
from typing import Sequence

from spacebase2p.arrow_ai import best_allocation, choose_arrow_direction
from spacebase2p.bot_policy import (
    best_chain_ship,
    best_colony,
    deny_arrow_ship,
    deny_colony_action,
    pick_ship_buy,
    should_race_colonies,
    worth_buying,
)
from spacebase2p.dice import Roll, legal_allocation_modes
from spacebase2p.game import BuyAction, BuyKind, Game, legal_colony_buys, legal_ship_buys
from spacebase2p.models import AllocationMode, ArrowChoice


def _resolve_buy(
    game: Game,
    player_idx: int,
    *,
    prefer: str,
    use_deny: bool,
    use_chains: bool,
    target_income: int | None = None,
) -> BuyAction:
    player = game.players[player_idx]
    colonies = legal_colony_buys(player, game.market)
    ships = legal_ship_buys(player, game.market)

    if use_deny:
        deny = deny_colony_action(game, player_idx, colonies)
        if deny:
            return deny
        arrow_deny = deny_arrow_ship(ships, game, player_idx)
        if arrow_deny:
            return BuyAction(BuyKind.SHIP, ship=arrow_deny)

    if should_race_colonies(game, player_idx):
        best = best_colony(colonies)
        if best and worth_buying(player.gold, best.cost, keystone=True):
            return BuyAction(BuyKind.COLONY, colony=best)

    if use_chains and not should_race_colonies(game, player_idx):
        chain = best_chain_ship(ships, game, player_idx)
        if chain and worth_buying(player.gold, chain.cost, keystone=True):
            return BuyAction(BuyKind.SHIP, ship=chain)

    if prefer == "income" and target_income is not None and player.income < target_income:
        action = pick_ship_buy(game, player_idx, ships, prefer="income")
        if action:
            return action

    if not should_race_colonies(game, player_idx):
        action = pick_ship_buy(game, player_idx, ships, prefer=prefer)
        if action:
            return action

    if colonies:
        best = best_colony(colonies)
        if best and worth_buying(player.gold, best.cost, keystone=True):
            return BuyAction(BuyKind.COLONY, colony=best)

    action = pick_ship_buy(game, player_idx, ships, prefer=prefer)
    if action:
        return action
    return BuyAction(BuyKind.PASS)


def _resolve_snowball_buy(game: Game, player_idx: int, target_income: int) -> BuyAction:
    """Tempo plan: rush race plus efficient 5–8 income in one scoring pass."""
    player = game.players[player_idx]
    prefer = "tempo" if player.income < target_income else "rush"
    return _resolve_buy(
        game,
        player_idx,
        prefer=prefer,
        use_deny=True,
        use_chains=prefer == "tempo",
    )


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

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
        from_sector: int = 0,
    ) -> str:
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
        return best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
        from_sector: int = 0,
    ) -> str:
        is_active = player_idx == game.active
        return choose_arrow_direction(game.players[player_idx], from_sector, is_active, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        return _resolve_buy(
            game,
            player_idx,
            prefer="income",
            use_deny=True,
            use_chains=False,
            target_income=self.target_income,
        )


class RushBot:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        return best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
        from_sector: int = 0,
    ) -> str:
        is_active = player_idx == game.active
        return choose_arrow_direction(game.players[player_idx], from_sector, is_active, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        return _resolve_buy(
            game,
            player_idx,
            prefer="rush",
            use_deny=True,
            use_chains=False,
        )


class SnowballBot:
    """Disciplined 2p income plan (5–8), then colony rush like the guide."""

    def __init__(self, rng: random.Random, target_income: int | None = None) -> None:
        self.rng = rng
        self.target_income = target_income or 6

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        return best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
        from_sector: int = 0,
    ) -> str:
        is_active = player_idx == game.active
        return choose_arrow_direction(game.players[player_idx], from_sector, is_active, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        return _resolve_snowball_buy(game, player_idx, self.target_income)


class ChainBot:
    """Income + blue arrows (7–11), smart allocation, deny."""

    def __init__(self, rng: random.Random, target_income: int | None = None) -> None:
        self.rng = rng
        self.target_income = target_income or rng.randint(4, 6)

    def choose_allocation(
        self,
        game: Game,
        player_idx: int,
        roll: Roll,
        active_idx: int,
    ) -> AllocationMode:
        return best_allocation(game, player_idx, roll, active_idx)

    def choose_arrows(
        self,
        game: Game,
        player_idx: int,
        options: list[str],
        from_sector: int = 0,
    ) -> str:
        is_active = player_idx == game.active
        return choose_arrow_direction(game.players[player_idx], from_sector, is_active, options)

    def choose_buy(self, game: Game, player_idx: int) -> BuyAction:
        return _resolve_buy(
            game,
            player_idx,
            prefer="income",
            use_deny=True,
            use_chains=True,
            target_income=self.target_income,
        )


def make_bot_pair(names: Sequence[str], rng: random.Random) -> list:
    bots = []
    for name in names:
        key = name.lower()
        if key == "income":
            bots.append(IncomeBot(rng))
        elif key == "rush":
            bots.append(RushBot(rng))
        elif key == "chain":
            bots.append(ChainBot(rng))
        elif key in ("snowball", "snow"):
            bots.append(SnowballBot(rng))
        elif key in ("random", "rand"):
            bots.append(RandomBot(rng))
        else:
            raise ValueError(f"unknown bot: {name}")
    return bots
