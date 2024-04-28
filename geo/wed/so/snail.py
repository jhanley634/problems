#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291672/create-a-snail-matrix

from typing import Generator

import numpy as np
import numpy.typing as npt

# type Matrix = list[list[int]]

cw_direction = [
    # ESWN
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]
ccw_direction = [
    # SENW
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def get_rect_spiral_coords(m: int, n: int) -> Generator[tuple[int, int], None, None]:
    x, y = 0, 0
    yield (x, y)
    dir_idx = 0

    dx, dy = cw_direction[dir_idx]
    x += dx
    y += dy

    m -= 1
    for _ in range(m):
        dx, dy = cw_direction[dir_idx]
        x += dx
        y += dy
        yield (x, y)
    dir_idx = (dir_idx + 1) % len(cw_direction)

    n -= 1
    for _ in range(n):
        dx, dy = cw_direction[dir_idx]
        print(f"down ({x}, {y}), delta ({dx}, {dy}), direction {dir_idx}", n)
        x += dx
        y += dy
        yield (x, y)
    dir_idx = (dir_idx + 1) % len(cw_direction)


def get_rect_spiral_array(m: int, n: int) -> npt.NDArray[np.int_]:
    a = np.zeros((m, n), dtype=int)
    count = 1
    for coord in get_rect_spiral_coords(m, n):
        a[coord] = count
        count += 1
    print(a, coord)
    return a


def get_square_spiral_matrix(size: int) -> list[list[int]]:
    """Create a size x size matrix arranged in a snail pattern."""
    m = get_rect_spiral_array(size, size)
    print(m, 7)
    ret = []
    for row in m.tolist():  # Grrr, mypy thinks m.tolist() is Any
        ret.append([int(cell) for cell in row])
    return ret


square = get_square_spiral_matrix
