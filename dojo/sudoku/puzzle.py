# Copyright 2023 John Hanley. MIT licensed.
from typing import Generator, Self

import numpy as np
import numpy.typing as npt


class Grid:
    """Models a Sudoku grid."""

    def __init__(self, size: int = 3) -> None:
        self.size = size  # width of a block (also, how many blocks across in a grid)
        self.grid = np.zeros((size**2, size**2), dtype=np.uint8)

    _remove_whitespace = str.maketrans("", "", " \n")
    _empty_is_zero = str.maketrans("_-", "00")  # use zero to model "-" empty cells

    def from_string(self, s: str) -> Self:
        """Populates board from a string."""
        s = s.translate(self._remove_whitespace)
        assert len(s) == self.size**4, s
        for i, ch in enumerate(s.translate(self._empty_is_zero)):
            v = int(ch)
            assert 0 <= v <= self.size**2, (i, v)
            x = i % self.size**2
            y = i // self.size**2
            self.grid[y, x] = v
        return self

    def is_valid(self) -> bool:
        """Returns True if grid is feasible (no dups)."""
        # Sūji wa dokushin ni kagiru (数字は独身に限る),
        # "the digits must be single", limited to one occurrence.
        for i in range(self.size**2):
            if self._has_dups(self.grid[i, :]):  # row
                return False
            if self._has_dups(self.grid[:, i]):  # column
                return False
        for block in self._get_blocks():
            print("\n", block)
            if self._has_dups(block):
                return False
        return True

    @staticmethod
    def _has_dups(vals: npt.NDArray[np.uint8]) -> bool:
        vals = list(filter(None, vals))
        return len(set(vals)) < len(vals)

    def _get_blocks(self) -> Generator[npt.NDArray[np.uint8], None, None]:
        for a in range(self.size):
            for b in range(self.size):
                yield from self._get_block(a, b)

    def _get_block(self, a, b) -> Generator[npt.NDArray[np.uint8], None, None]:
        sz = self.size
        i = a * sz
        j = b * sz
        yield np.array(self.grid[i : i + sz, j : j + sz]).flatten()


class Solver:
    """Solves a Sudoku puzzle."""


if __name__ == "__main__":
    b = Grid(size=2).from_string("1234 1234  1234 1234")
