# Copyright 2023 John Hanley. MIT licensed.
from typing import Generator
import datetime as dt
import sys
import unittest

from sortedcontainers import SortedList

from .word_ladder import WordLadder, hamming_distance


class TestSortedList(unittest.TestCase):
    def test_sorted_list(self) -> None:
        xs = SortedList([9, 5, 6, 7])
        self.assertEqual([5, 6, 7, 9], xs)
        self.assertEqual(6, xs[1])
        self.assertEqual([5, 6], xs[:2])

        i = xs.bisect_left(4)
        self.assertEqual(0, i)
        i = xs.bisect_left(5)
        self.assertEqual(0, i)
        i = xs.bisect_left(7)
        self.assertEqual(2, i)

        i = xs.bisect_right(7)
        self.assertEqual(3, i)
        i = xs.bisect_right(9)
        self.assertEqual(4, i)
        i = xs.bisect_right(10)
        self.assertEqual(4, i)


class TestHammingDistance(unittest.TestCase):
    def test_symmetric_hamming_distance(self) -> None:
        for a, b, distance in [
            ("abc", "abc", 0),
            ("abc", "bbc", 1),
            ("abc", "azc", 1),
            ("abc", "abz", 1),
            ("abc", "ayz", 2),
            ("abc", "def", 3),
        ]:
            self.assertEqual(distance, hamming_distance(a, b))
            self.assertEqual(distance, hamming_distance(b, a))


def _get_months() -> Generator[str, None, None]:
    for month in range(1, 8):
        yield dt.date(2023, month, 1).strftime("%b").lower()


class TestWordLadder(unittest.TestCase):
    def test_months(self) -> None:
        months = list(_get_months())
        self.assertEqual(["jan", "feb", "mar", "apr", "may", "jun", "jul"], months)

        wl = WordLadder(3, months)
        path = ["jan", "jun", "jul"]
        self.assertEqual(path, wl.find_path(path[0], path[-1]))

    def test_init(self) -> None:
        self.assertGreaterEqual(sys.getrecursionlimit(), 1_000)
        sys.setrecursionlimit(10_000)

        wl = WordLadder(length=3)
        assert wl
        for length, num_words, path in [
            (10, 303_762, ["blistering", "blustering", "clustering"]),
            (7, 154_820, ["blister", "bluster", "cluster"]),
            (6, 90_290, self._get_6_char_path()),
            (5, 36_485, self._get_5_char_path()),
            (4, 9118, ["shoe", "sloe", "floe", "flop", "flap"]),
            (3, 969, ["cat", "pat", "pot", "pow"]),
        ]:
            wl = WordLadder(length=length)
            self.assertEqual(num_words, len(wl.words))
            word_pair = [path[0], path[-1]]
            self.assertEqual(path, wl.find_path(*word_pair))
            self.assertEqual(len(path), len(wl.find_path(*reversed(word_pair))))

        self.assertEqual(["dog", "cog", "cag", "cat"], wl.find_path("dog", "cat"))
        self.assertEqual(["cat", "cot", "dot", "dog"], wl.find_path("cat", "dog"))

    @staticmethod
    def _get_5_char_path() -> list[str]:
        return ["douse", "rouse", "route", "foute", "flute", "flume", "flame"]

    @staticmethod
    def _get_6_char_path() -> list[str]:
        return [
            "boyish",
            "bayish",
            "barish",
            "rarish",
            "rawish",
            "rewish",
            "relish",
            "relist",
            "relict",
            "relick",
            "relink",
            "reline",
            "feline",
            "ferine",
            "serine",
            "scrine",
            "scrike",
            "strike",
            "strake",
            "straka",
            "strata",
            "strath",
            "struth",
            "stouth",
            "scouth",
            "scouch",
            "scotch",
            "scutch",
            "slutch",
            "clutch",
            "clunch",
            "caunch",
            "paunch",
        ]
