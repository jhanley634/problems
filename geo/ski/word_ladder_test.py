import sys
import unittest

from sortedcontainers import SortedList

from .word_ladder import WordLadder, hamming_distance


class TestSortedList(unittest.TestCase):
    def test_sorted_list(self):
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
    def test_symmetric_hamming_distance(self):
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


class TestWordLadder(unittest.TestCase):
    def test_init(self):
        self.assertEqual(1_000, sys.getrecursionlimit())
        sys.setrecursionlimit(10_000)

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
    def _get_5_char_path():
        return ["douse", "rouse", "route", "foute", "flute", "flume", "flame"]

    @staticmethod
    def _get_6_char_path():
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
