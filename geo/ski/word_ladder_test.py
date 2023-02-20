import sys
import unittest

from sortedcontainers import SortedList

from .word_ladder import WordLadder


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


class TestWordLadder(unittest.TestCase):
    def test_init(self):
        self.assertEqual(1_000, sys.getrecursionlimit())
        sys.setrecursionlimit(10_000)

        for length, num_words in [
            (14, 9761),
            (10, 30_824),
            (6, 17_462),
            (4, 4994),
            (3, 1294),
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

        self.assertEqual(3882, len(wl.pfx_nodes))

        # Pick an arbitrary word.
        i = int(len(wl.pfx_nodes) * 0.1)
        self.assertEqual("pen", wl.pfx_nodes[i].word)

        self.assertEqual(["dog", "cog", "cag", "cat"], wl.find_path("dog", "cat"))
        self.assertEqual(["cat", "cag", "cog", "dog"], wl.find_path("cat", "dog"))
        self.assertEqual(["cat", "caw", "cow", "pow"], wl.find_path("cat", "pow"))

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
