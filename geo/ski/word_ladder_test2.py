# Copyright 2023 John Hanley. MIT licensed.
import unittest

from geo.ski.word_ladder2 import WordLadder
from geo.ski.word_ladder_test import _get_months


class TestWordLadder2(unittest.TestCase):
    def test_months(self):
        months = list(_get_months())
        self.assertEqual("jan feb mar apr may jun jul", " ".join(months))

        wl = WordLadder(3, months)
        feb_may = "feb jul jan jun mar apr may"
        self.assertEqual(feb_may, " ".join(wl.vocabulary[i] for i in wl.rev_vocab))
        self.assertEqual([1, 3, 2, 4, 5, 0, 6], wl.rev_vocab)

        self.assertEqual(9, wl._adjacent_words(0, 1))

        path = ["jan", "jun", "jul"]
        self.assertEqual(path, wl.find_path(path[0], path[-1]))
