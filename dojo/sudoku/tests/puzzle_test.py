# Copyright 2023 John Hanley. MIT licensed.

import unittest

from dojo.sudoku.puzzle import Grid


class PuzzleTest(unittest.TestCase):
    def test_grid_is_valid(self) -> None:
        p = Grid(size=2).from_string("1234 1234  1234 1234")
        p = Grid(size=2).from_string("12 23  34 41   34 41  12 23")
        p = Grid(size=2).from_string(
            """
            12  34
            34  12

            41  23
            23  41
            """
        )
        self.assertTrue(p.is_valid())

    def test_wildcard_valid(self) -> None:
        p = Grid(size=2).from_string("-" * 16)
        self.assertTrue(p.is_valid())
