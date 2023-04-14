#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# https://stackoverflow.com/questions/76016826/algorithm-to-match-a-pool-of-players-by-rating

from dataclasses import dataclass
from itertools import pairwise
from typing import Any, Generator
import unittest


@dataclass
class Player:
    name: str
    rating: int

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Player):
            return False
        return self.rating < other.rating

    def __repr__(self) -> str:
        return f"{self.name} {self.rating}"


pool = [
    Player(name, rating)
    for name, rating in [
        ("John", 1600),
        ("Jasmine", 1670),
        ("Chris", 1610),
        ("Rob", 1650),
        ("Frank", 1660),
    ]
]


def get_deltas(pool: list[Player]) -> Generator[int, None, None]:
    pool = sorted(pool)
    for a, b in pairwise(pool):
        yield b.rating - a.rating


def get_player_pairs(
    pool: list[Player],
) -> Generator[tuple[Player, Player], None, None]:
    max_delta = max(get_deltas(pool))
    pool = sorted(pool)
    while len(pool) > 1:
        if pool[0].rating - pool[1].rating < max_delta:
            yield pool.pop(0), pool.pop(0)
        else:
            pool.pop(0)


class TestMatchPlayers(unittest.TestCase):
    def test_get_deltas(self) -> None:
        self.assertEqual([10, 40, 10, 10], list(get_deltas(pool)))
        self.assertEqual(40, max(get_deltas(pool)))

    def test_get_pairs(self) -> None:
        self.assertEqual(
            [
                "(John 1600, Chris 1610)",
                "(Rob 1650, Frank 1660)",
            ],
            list(map(str, get_player_pairs(pool))),
        )
