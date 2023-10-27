# Copyright 2023 John Hanley. MIT licensed.

import unittest

from dojo.sudoku.puzzle import Grid, solve


class PuzzleTest(unittest.TestCase):
    def setUp(self):
        self.puzzle = Grid(size=2).from_string(
            """
            12  34
            34  12

            41  23
            23  41
            """
        )

    def test_grid_is_valid(self) -> None:
        self.assertTrue(self.puzzle.is_valid())
        self.assertTrue(self.puzzle.is_solved())

        self.puzzle.grid[0, 0] = 4
        self.assertFalse(self.puzzle.is_valid())
        self.assertFalse(self.puzzle.is_solved())

        self.puzzle.grid[0, 0] = 0
        self.assertTrue(self.puzzle.is_valid())
        self.assertFalse(self.puzzle.is_solved())

    def test_wildcard_valid(self) -> None:
        self.assertTrue(Grid(size=2).from_string("" + "-" * 16).is_valid())

        self.assertTrue(Grid(size=2).from_string("1" + "-" * 15).is_valid())

        self.assertTrue(Grid(size=2).from_string("34" + "-" * 14).is_valid())

    def test_short_string(self):
        self.assertEqual(
            "34--------------",
            Grid(size=2).from_string("34" + "-" * 14).to_short_string(),
        )
        self.assertEqual("1234341241232341", self.puzzle.to_short_string())

    def test_solve(self) -> None:
        p = self.puzzle
        self.assertEqual((4, 4), solve(p).grid.shape)

        for i in range(6):
            p = self.puzzle.copy()
            p.unsolve(i)
            print("\n", i)
            print(p)
            solve(p)
            self.assertTrue(p.is_solved())
