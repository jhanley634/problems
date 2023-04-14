#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# https://stackoverflow.com/questions/76016826/algorithm-to-match-a-pool-of-players-by-rating

from dataclasses import dataclass
import unittest


@dataclass
class Player:
    name: str
    rating: int

    def __lt__(self, other):
        return self.rating < other.rating

    def __repr__(self):
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


def get_deltas(pool: list[Player]):
    pool = sorted(pool)
    return [pool[i + 1].rating - pool[i].rating for i in range(len(pool) - 1)]


def get_player_pairs(pool: list[Player]):
    max_delta = max(get_deltas(pool))
    pool = sorted(pool)
    while len(pool) > 1:
        if pool[0].rating - pool[1].rating < max_delta:
            yield pool.pop(0), pool.pop(0)
        else:
            pool.pop(0)


class TestMatchPlayers(unittest.TestCase):
    def test_get_deltas(self):
        self.assertEqual([10, 40, 10, 10], get_deltas(pool))
        self.assertEqual(40, max(get_deltas(pool)))

    def test_get_pairs(self):
        self.assertEqual(
            [
                "(John 1600, Chris 1610)",
                "(Rob 1650, Frank 1660)",
            ],
            list(map(str, get_player_pairs(pool))),
        )
