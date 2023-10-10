from enum import Enum, auto
# Copyright 2023 John Hanley. MIT licensed.
from typing import Generator, Self

import numpy as np
import numpy.typing as npt


class Constraint(Enum):
    """Soduko constrains values by row, column, and block."""

    ROW = auto()
    COL = auto()
    BLK = auto()


class Grid:
    """Models a Sudoku grid."""

    def __init__(self, size: int = 3) -> None:
        self.size = size  # width of a block (also, how many blocks across in a grid)
        self.grid = np.zeros((size**2, size**2), dtype=np.uint8)

        # maps from (type, index) to the available values
        self.avail: dict[tuple[Constraint, int], list[int]] = {}

        # trivially valid, since 100% wildcards means no conflicts
        assert self.is_valid()

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

        self.avail = {}
        for i in range(self.size**2):
            self.avail[(Constraint.ROW, i)] = self._available_values(self.grid[i, :])
            self.avail[(Constraint.COL, i)] = self._available_values(self.grid[:, i])
        for i, block in enumerate(self._get_blocks()):
            self.avail[(Constraint.BLK, i)] = self._available_values(block)

        return self  # We offer a fluent API.

    def _available_values(self, vals) -> list[int]:
        return sorted(self._valid_cell_values() - set(vals[vals > 0]))

    def _valid_cell_values(self) -> set[int]:
        return set(range(1, self.size**2 + 1))

    def is_solved(self) -> bool:
        num_wildcards = len(self.grid[self.grid == 0])
        return num_wildcards == 0 and self.is_valid()

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
            if self._has_dups(block):
                return False
        return True

    @staticmethod
    def _has_dups(vals: npt.NDArray[np.uint8]) -> bool:
        actual_vals = vals[vals > 0]  # a zero wildcard is not an actual solution value
        return len(set(actual_vals)) < len(actual_vals)

    def _get_blocks(self) -> Generator[npt.NDArray[np.uint8], None, None]:
        sz = self.size
        for a in range(self.size):
            for b in range(self.size):
                i = a * sz
                j = b * sz
                yield np.array(self.grid[i : i + sz, j : j + sz]).flatten()


def solve(grid: Grid) -> Grid:
    """Solves a Sudoku puzzle."""
    assert grid.is_valid()
    if grid.is_solved():
        return grid
    return grid


if __name__ == "__main__":
    if False:
        solve(Grid(size=2).from_string("1234 1234  1234 1234"))
