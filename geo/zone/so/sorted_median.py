#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from enum import Enum, auto
from random import randrange
from time import time
import unittest

import numpy as np


class ListName(Enum):
    X = auto()
    Y = auto()


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

    # In general this can certainly happen.
    # But never in the test data we generate, by construction.
    # We resolve the `name` ambiguity in favor of X.
    if xs[x_mid] == ys[y_mid]:
        return both_mid, ListName.X if x_mid >= y_mid else ListName.Y

    return both_mid, ListName.X


def _generate_list_pair(
    n: int,
) -> tuple[
    np.ndarray[int, np.dtype[np.int_]], np.ndarray[int, np.dtype[np.int_]], ListName
]:
    """Returns a pair of integer arrays, and the name of the one that contains the median.

    Contents are random.
    We ensure the median value of "both" occurs in exactly one list.
    """
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

    def test_median_of_single_list(self) -> None:
        xs = np.array(sorted(self.rand))
        med_val = np.quantile(xs, 0.5)
        i = median_idx_of_single_list(xs)
        self.assertEqual(med_val, xs[i])

    def test_median_of_list_pair(self) -> None:
        xs, ys, true_name = _generate_list_pair(len(self.rand))
        i, name = median_of_list_pair(xs, ys)
        self.assertEqual(1050, i)
        self.assertEqual(true_name, name)

    # typical array speedup is 3x:idx_ 21.764 s / 6.993 s
    def test_sort_speed_list(self) -> None:
        t0 = time()
        for _ in range(len(self.rand)):
            a = self.rand.copy()
            a.sort()
            a.sort(reverse=True)
            a.sort()
        # print(f"\n list sort: {time() - t0:.3f} sec")

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
