# Copyright 2023 John Hanley. MIT licensed.
from typing import Self

import numpy as np


class Grid:
    """Models a Sudoku grid."""

    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.grid = np.zeros((size**2, size**2), dtype=np.uint8)

    _remove_whitespace = str.maketrans("", "", " \n")
    _empty_is_zero = str.maketrans("_-", "00")  # use zero to model "-" empty cells

    def from_string(self, s: str) -> Self:
        """Populates board from a string."""
        s = s.translate(self._remove_whitespace)
        assert len(s) == self.size**4, s
        for i, ch in enumerate(s.translate(self._empty_is_zero)):
            x = i % self.size**2
            y = i // self.size**2
            self.grid[y, x] = int(ch)
        return self

    def is_feasible(self) -> bool:
        """Returns True if grid is feasible."""
        # Sūji wa dokushin ni kagiru (数字は独身に限る),
        # "the digits must be single", limited to one occurrence.
        return False


class Solver:
    """Solves a Sudoku puzzle."""


if __name__ == "__main__":
    b = Grid(size=2).from_string("1234 5678  1234 5678")
    print(b.grid)
