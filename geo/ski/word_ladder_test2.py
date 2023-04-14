# Copyright 2023 John Hanley. MIT licensed.

import unittest

from geo.ski.word_ladder2 import WordLadder
from geo.ski.word_ladder_test import _get_months


class TestWordLadder2(unittest.TestCase):
    def test_months(self) -> None:
        months = list(_get_months())
        self.assertEqual("jan feb mar apr may jun jul", " ".join(months))

        wl = WordLadder(3, months)
        feb_may = "feb jul jan jun mar apr may"
        self.assertEqual(feb_may, " ".join(wl.vocabulary[i] for i in wl.rev_vocab))
        self.assertEqual([1, 3, 2, 4, 5, 0, 6], wl.rev_vocab)

        self.assertEqual("apr", wl.word_str(0 * wl.length))
        self.assertEqual("feb", wl.word_str(1 * wl.length))
        self.assertEqual("jan", wl.word_str(2 * wl.length))
        self.assertEqual("mar", wl.word_str(5 * wl.length))

        self.assertEqual("_ar", wl.prototype_str(5 * wl.length + 0))
        self.assertEqual("m_r", wl.prototype_str(5 * wl.length + 1))
        self.assertEqual("ma_", wl.prototype_str(5 * wl.length + 2))

        self.assertEqual([], list(wl._adjacent_words(5 * wl.length, 0)))
        self.assertEqual([], list(wl._adjacent_words(5 * wl.length, 1)))
        self.assertEqual(["may"], list(wl._adjacent_words(5 * wl.length, 2)))

        path = ["jan", "jun", "jul"]
        self.assertEqual(path, wl.find_path(path[0], path[-1]))
