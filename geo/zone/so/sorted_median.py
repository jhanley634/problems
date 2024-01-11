#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from dataclasses import dataclass
from enum import Enum, auto
from random import randrange
from time import time
import unittest

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


def _monotonic(a: np.ndarray[int, np.dtype[np.int_]]) -> bool:
    return bool(np.all(np.diff(a) >= 0))


def median_idx_of_single_list(xs: np.ndarray[int, np.dtype[np.int_]]) -> int:
    assert len(xs) > 0
    assert len(xs) % 2 == 1
    assert _monotonic(xs)
    mid = len(xs) // 2
    assert all(xs[i] <= xs[mid] for i in range(mid))
    assert all(xs[i] >= xs[mid] for i in range(mid, len(xs)))
    return mid


def median_of_list_pair(
    xs: np.ndarray[int, np.dtype[np.int_]],
    ys: np.ndarray[int, np.dtype[np.int_]],
) -> tuple[int, ListName]:
    assert len(xs) > 0
    assert _monotonic(xs)

    assert len(ys) > 0
    assert _monotonic(ys)

    assert (len(xs) + len(ys)) % 2 == 1  # The answer is definitely one of the elements.

    x_mid = len(xs) // 2
    y_mid = len(ys) // 2
    both_mid = x_mid + y_mid
    assert len(np.concatenate((xs, ys))) == both_mid + 1 + both_mid

    return _median2(
        (xs, ys),
        (MutRange(0, len(xs)), MutRange(0, len(ys))),
    )


def _median2(
    arrays: tuple[
        np.ndarray[int, np.dtype[np.int_]],
        np.ndarray[int, np.dtype[np.int_]],
    ],
    ranges: tuple[MutRange, MutRange],
) -> tuple[int, ListName]:
    assert len(arrays) == len(ranges) == 2
    xs, ys = arrays
    r0, r1 = ranges

    # The total of the range .start's needs to hit this target.
    # So does the total amount of .stop .. len() elements.
    target = (len(xs) + len(ys)) // 2

    # invariant: the median index is always within the ranges.
    # (A range _can_ get squished to zero length,
    # indicating the median index is within the other range.)

    while True:
        assert sum(map(len, ranges)) >= 1  # The answer is in there!

        # Two ways to win; two base cases.
        for a in range(len(arrays)):
            # A length of zero indicates that we have "squeezed out"
            # the median index from the other array.
            if len(ranges[a]) == 1 and len(ranges[1 - a]) == 0:
                return ranges[a].start, list(ListName.__members__.values())[a]

        # Haven't narrowed it down to a unique answer, yet.
        # There's more work to be done.

        # Loop variant: at least one of the two ranges _will_ shrink.
        small_val = min(
            int(xs[r0.start]),
            int(ys[r1.start]),
        )
        big_val = float("-inf")
        if len(r0) > 0 and r0.stop - 1 >= 0:
            big_val = max(big_val, int(xs[r0.stop - 1]))
        if len(r1) > 0 and r1.stop - 1 >= 0:
            big_val = max(big_val, int(ys[r1.stop - 1]))
        # print(r0, r1)
        assert big_val >= small_val

        if r0.start + r1.start < target:
            if len(r0) > 0 and xs[r0.start] == small_val:
                r0.start += 1
            if len(r1) > 0 and ys[r1.start] == small_val:
                r1.start += 1

        if (len(xs) - 1 - r0.start) + (len(ys) - 1 - r1.start) < target:
            if len(r0) > 0 and xs[r0.stop - 1] == big_val:
                r0.stop -= 1
            if len(r1) > 0 and ys[r1.stop - 1] == big_val:
                r1.stop -= 1


def _generate_list_pair(
    n: int,
) -> tuple[
    np.ndarray[int, np.dtype[np.int_]],
    np.ndarray[int, np.dtype[np.int_]],
    ListName,
]:
    """Returns a pair of integer arrays, and the name of the one that contains the median.

    Contents are random.
    We ensure the median value of "both" occurs in exactly one list.
    """
    med_val = 0.0
    xs = ys = np.zeros(1, dtype=int)
    done = False
    while not done:
        xs = np.array(sorted(randrange(int(1.5 * n)) for _ in range(n)))
        ys = np.array(sorted(randrange(int(1.5 * n)) for _ in range(n - 101)))
        both = np.array(sorted(np.concatenate((xs, ys))))
        med_val = np.quantile(both, 0.5)
        i = len(both) // 2
        assert med_val == both[i]
        if (med_val in xs) != (med_val in ys):
            done = True

    name = ListName.X if med_val in xs else ListName.Y
    return xs, ys, name


class SortedMedianTest(unittest.TestCase):
    def setUp(self, n: int = 1_101) -> None:
        self.rand = [randrange(int(1.5 * n)) for _ in range(n)]

    def test_monotonic(self) -> None:
        xs = np.array([0, 1, 1, 2, 3, 3, 3, 4, 5])
        self.assertTrue(_monotonic(xs))

        xs = np.array([0, 1, 1, 0, 5])
        self.assertFalse(_monotonic(xs))

    def test_median_of_single_list(self) -> None:
        xs = np.array(sorted(self.rand))
        med_val = np.quantile(xs, 0.5)
        i = median_idx_of_single_list(xs)
        self.assertEqual(med_val, xs[i])

    def test_median_of_list_pair(self) -> None:
        xs, ys, true_name = _generate_list_pair(len(self.rand))
        i, name = median_of_list_pair(xs, ys)
        # TODO self.assertEqual(1050, i)
        self.assertEqual(true_name, name)

    def test_enum_values(self) -> None:
        self.assertEqual(0, ListName.X.value)
        self.assertEqual(1, ListName.Y.value)

    # typical array speedup is 3x:idx_ 21.764 s / 6.993 s
    def test_sort_speed_list(self) -> None:
        t0 = time()
        for _ in range(len(self.rand)):
            a = self.rand.copy()
            a.sort()
            a.sort(reverse=True)
            a.sort()
        # print(f"\n list sort: {time() - t0:.3f} sec")
        self.assertLess(time() - t0, 0.250)

    def test_sort_speed_array(self) -> None:
        xs = np.array(self.rand)
        t0 = time()
        for _ in range(len(self.rand)):
            a = np.array(xs)
            a.sort()
            a = np.flip(a)
            a.sort()
            a.sort()
        # print(f"\n array sort: {time() - t0:.3f} sec")
        self.assertLess(time() - t0, 0.250)
