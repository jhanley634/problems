# Copyright 2023 John Hanley. MIT licensed.
from enum import Enum, auto
from functools import total_ordering
from typing import Any, Generator, Self

import numpy as np
import numpy.typing as npt


@total_ordering
class Constraint(Enum):
    """Soduko constrains values by block, row, and column."""

    BLK = auto()
    ROW = auto()
    COL = auto()

    def __lt__(self, other: Any) -> bool | type(NotImplemented):
        if self.__class__ is other.__class__:
            return bool(self.value < other.value)
        return NotImplemented


class Grid:
    """Models a Sudoku grid."""

    def __init__(self, size: int = 3):
        self.size = size  # width of a block (also, how many blocks across in a grid)
        self.grid = np.zeros((size**2, size**2), dtype=np.uint8)

        # maps from (type, index) to the available values
        self.avail: dict[tuple[Constraint, int], set[int]] = {}

        # trivially valid, since 100% wildcards means no conflicts
        assert self.is_valid()

    _remove_whitespace = str.maketrans("", "", " \n")
    _empty_is_zero = str.maketrans("_-", "00")  # use zero to model "-" empty cells

    def from_string(self, s: str) -> Self:
        """Populates board from a string."""
        s = s.translate(self._remove_whitespace)
        assert len(s) == self.size**4, (len(s), self.size**4, s)
        for i, ch in enumerate(s.translate(self._empty_is_zero)):
            v = int(ch)
            assert 0 <= v <= self.size**2, (i, v)
            x = i % self.size**2
            y = i // self.size**2
            self.grid[y, x] = v

        self._update_avail()
        return self  # We offer a fluent API.

    def _update_avail(self) -> None:
        avail = {}
        for i in range(self.size**2):
            avail[(Constraint.ROW, i)] = self._available_values(self.grid[i, :])
            avail[(Constraint.COL, i)] = self._available_values(self.grid[:, i])
        for i, block in enumerate(self._get_blocks()):
            avail[(Constraint.BLK, i)] = self._available_values(block)

        tuples = [(len(v), k, v) for k, v in avail.items()]  # if v]
        self.avail = {k: v for _, k, v in sorted(tuples)}

    def _available_values(self, vals: npt.NDArray[np.uint8]) -> set[int]:
        return self._valid_cell_values() - set(vals[vals > 0])

    def _valid_cell_values(self) -> set[int]:
        return set(range(1, self.size**2 + 1))

    def __str__(self) -> str:
        sz = self.size
        ret = []
        for i in range(sz**2):
            if i % sz == 0:
                ret.append("\n")
            row_vals = "".join(map(str, self.grid[i, :]))
            rng = range(0, len(row_vals), sz)
            ret.append(" ".join(row_vals[i : i + sz] for i in rng))
            ret.append("\n")
        return "".join(ret).replace("0", "-")

    def to_short_string(self) -> str:
        return str(self).translate(self._remove_whitespace)

    def unsolve(self, n: int = 1) -> None:
        """Turns N grid values into wildcards."""
        num_wildcards = len(self.grid[self.grid == 0])
        assert num_wildcards == 0
        for _ in range(n):
            # Avoid zeroing a cell that is already zero.
            done = False
            while not done:
                i = np.random.randint(0, self.size**2)
                j = np.random.randint(0, self.size**2)
                if self.grid[i, j] > 0:
                    self.grid[i, j] = 0
                    done = True
        self._update_avail()

    def is_solved(self) -> bool:
        num_wildcards = len(self.grid[self.grid == 0])
        return num_wildcards == 0 and self.is_valid()

    def is_valid(self) -> bool:
        """Returns True if grid is feasible (no duplicates)."""
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

    def copy(self) -> "Grid":
        """Returns a deep copy."""
        cpy = Grid(size=self.size)
        cpy.grid = self.grid.copy()
        cpy._update_avail()
        return cpy


def solve(grid: Grid) -> Grid | None:
    """Solves a Sudoku puzzle."""
    assert grid.is_valid()
    if grid.is_solved():
        return grid
    num_wildcards = len(grid.grid[grid.grid == 0])
    print("\n", num_wildcards)

    # for constraint, available_values in grid.avail.items():
    #     for val in available_values:

    for i, j in np.ndindex(grid.grid.shape):
        if grid.grid[i, j] == 0:
            available_values = (
                grid.avail[(Constraint.ROW, i)]
                & grid.avail[(Constraint.COL, j)]
                & grid.avail[(Constraint.BLK, i * j // grid.size // grid.size)]
            )
            print("\n", i, j, available_values)
            for val in available_values:
                grid.grid[i, j] = val
                assert grid.is_valid()
                s = solve(grid.copy())
                if s:
                    assert s.is_valid()
                    return s
            return None  # caller will backtrack

    raise RuntimeError("no solution found")


if __name__ == "__main__":
    ...
    # solve(Grid(size=2).from_string("1234 1234  1234 1234"))
