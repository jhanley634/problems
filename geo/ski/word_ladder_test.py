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

        for length, num_words in [
            (14, 136_099),  # 9761),
            (10, 303_762),  # 30_824),
            (6, 90_290),  # 17_462),
            (4, 9118),  # 4994),
            (3, 969),  # 1294),
        ]:
            wl = WordLadder(length=length)
            self.assertEqual(num_words, len(wl.words))
            if length == 10:
                self.assertEqual(
                    ["blistering", "blustering", "clustering"],
                    wl.find_path("blistering", "clustering"),
                )
            if length == 6:
                self.assertEqual(
                    self._get_6_char_path(), wl.find_path("boyish", "paunch")
                )
            if length == 4:
                self.assertEqual(
                    ["shoe", "sloe", "floe", "flop", "flap"],
                    wl.find_path("shoe", "flap"),
                )
        self.assertEqual(["dog", "cog", "cag", "cat"], wl.find_path("dog", "cat"))
        self.assertEqual(["cat", "cot", "dot", "dog"], wl.find_path("cat", "dog"))
        self.assertEqual(["cat", "pat", "pot", "pow"], wl.find_path("cat", "pow"))

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
