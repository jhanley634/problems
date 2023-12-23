#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from random import randrange
from time import time
import unittest

import numpy as np


def _monotonic(a: np.ndarray[int, np.dtype[np.int_]]) -> bool:
    return bool(np.all(np.diff(a) >= 0))


def median_idx_of_one_list(xs: np.ndarray[int, np.dtype[np.int_]]) -> int:
    assert len(xs) > 0
    assert len(xs) % 2 == 1
    assert _monotonic(xs)
    mid = len(xs) // 2
    assert all(xs[i] <= xs[mid] for i in range(mid))
    assert all(xs[i] >= xs[mid] for i in range(mid, len(xs)))
    return mid


def median_of_two_lists(
    xs: np.ndarray[int, np.dtype[np.int_]],
    ys: np.ndarray[int, np.dtype[np.int_]],
) -> int:
    assert len(xs) > 0
    assert len(xs) % 2 == 1
    assert _monotonic(xs)

    assert len(ys) > 0
    assert len(ys) % 2 == 1
    assert _monotonic(ys)

    mid = len(xs) // 2
    return mid


class SortedMedianTest(unittest.TestCase):
    def setUp(self, n: int = 1_001) -> None:
        self.rand = [randrange(int(1.5 * n)) for _ in range(n)]

    def test_median_of_one_list(self) -> None:
        xs = np.array(sorted(self.rand))
        med_val = np.quantile(xs, 0.5)
        i = median_idx_of_one_list(xs)
        self.assertEqual(med_val, xs[i])

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
