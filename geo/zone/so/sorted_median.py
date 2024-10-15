# Copyright 2023 John Hanley. MIT licensed.

from dataclasses import dataclass
from enum import Enum, auto

from beartype import beartype
import numpy as np


class ListName(Enum):
    X = 0
    Y = auto()


@dataclass
class MutRange:
    """Models a mutable `range`, with .start and .stop attributes."""

    # I may get around to implementing __iter__, if calling code ever needs that.
    # We remedy the chief disadvantage of the builtin `range`: its immutability.

    start: int
    stop: int
    # `step` is always unity.

    def __len__(self) -> int:
        assert self.stop >= self.start
        return self.stop - self.start


@beartype
def _monotonic(a: np.ndarray[int, np.dtype[np.int_]]) -> bool:
    return bool(np.all(np.diff(a) >= 0))


@beartype
def median_idx_of_single_list(xs: np.ndarray[int, np.dtype[np.int_]]) -> int:
    assert len(xs) > 0
    assert len(xs) % 2 == 1
    assert _monotonic(xs)
    mid = len(xs) // 2
    assert all(xs[i] <= xs[mid] for i in range(mid))
    assert all(xs[i] >= xs[mid] for i in range(mid, len(xs)))
    return mid


@beartype
def median_of_list_pair(
    xs: np.ndarray[int, np.dtype[np.int_]],
    ys: np.ndarray[int, np.dtype[np.int_]],
) -> tuple[int, ListName]:
    assert _monotonic(xs)
    assert _monotonic(ys)
    assert len(xs) + len(ys) > 0, "empty input not allowed"
    assert (len(xs) + len(ys)) % 2 == 1  # The answer is definitely one of the elements.

    return _median1(
        (xs, ys),
        (MutRange(0, len(xs)), MutRange(0, len(ys))),
    )


# ruff: noqa: C901


@beartype
def _median1(
    arrays: tuple[
        np.ndarray[int, np.dtype[np.int_]],
        np.ndarray[int, np.dtype[np.int_]],
    ],
    ranges: tuple[MutRange, MutRange],
) -> tuple[int, ListName]:
    xs, ys = arrays
    r0, r1 = ranges

    assert len(xs) == len(r0)
    assert len(ys) == len(r1)

    # If an entry has been eliminated, it is ruled out as a median candidate.
    left_elim = right_elim = 0
    # The total of the range .start's needs to hit this target.
    # So does the total amount of .stop .. len() elements.
    target = (len(r0) + len(r1)) // 2

    # invariant: the median index is always within the ranges.
    # (A range _can_ get squished to zero length,
    # indicating the median index is within the other range.)

    while len(r0) + len(r1) > 1:
        # Loop variant: at least one of the two ranges _will_ shrink.

        # One of the ranges has been exhausted, so squish the other.
        if left_elim < target and len(r0) > 0 and len(r1) == 0:
            m = min(max(1, len(r0) // 2), target - left_elim, len(r0))  # midpoint
            r0.start += m
            left_elim += m

        if left_elim < target and len(r0) == 0 and len(r1) > 0:
            m = min(max(1, len(r1) // 2), target - left_elim, len(r1))
            r1.start += m
            left_elim += m

        if right_elim < target and len(r0) > 0 and len(r1) == 0:
            m = min(max(1, len(r0) // 2), target - right_elim, len(r0))
            r0.stop -= m
            right_elim += m

        if right_elim < target and len(r0) == 0 and len(r1) > 0:
            m = min(max(1, len(r1) // 2), target - right_elim, len(r1))
            r1.stop -= m
            right_elim += m

        # While feasible, squish both ranges.
        if (
            left_elim < target
            and len(r0) > 0
            and len(r1) > 0
            and xs[r0.start] <= ys[r1.start]
        ):  # min_y
            r0.start += 1
            left_elim += 1

        if (
            left_elim < target
            and len(r0) > 0
            and len(r1) > 0
            and ys[r1.start] <= xs[r0.start]
        ):  # min_x
            r1.start += 1
            left_elim += 1

        if (
            right_elim < target
            and len(r0) > 0
            and len(r1) > 0
            and xs[r0.stop - 1] >= ys[r1.stop - 1]
        ):  # max_y
            r0.stop -= 1
            right_elim += 1

        if (
            right_elim < target
            and len(r0) > 0
            and len(r1) > 0
            and ys[r1.stop - 1] >= xs[r0.stop - 1]
        ):  # max_x
            r1.stop -= 1
            right_elim += 1

    assert len(r0) + len(r1) == 1  # Found it!

    if len(r0) == 1:
        return r0.start, ListName.X
    return r1.start, ListName.Y
