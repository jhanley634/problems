#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


from random import randrange
from time import time
import unittest

from beartype import beartype
from hypothesis import Verbosity, given, settings
from hypothesis import strategies as st
from numpy.typing import NDArray
import numpy as np

from geo.zone.so.sorted_median import (
    ListName,
    _monotonic,
    median_idx_of_single_list,
    median_of_list_pair,
)

# easily fits within FP 53-bit signficand
BIG = 2**52
ST_FINITE_INTEGERS = st.integers(min_value=-BIG, max_value=BIG)


@beartype
def _generate_list_pair(
    n: int,
) -> tuple[
    np.ndarray[int, np.dtype[np.int_]],
    np.ndarray[int, np.dtype[np.int_]],
    ListName,
    float,
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

    assert med_val in xs or med_val in ys
    assert not (med_val in xs and med_val in ys)  # (XOR)
    name = ListName.X if med_val in xs else ListName.Y
    return xs, ys, name, float(med_val)


@beartype
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
        def check(x_in: NDArray[np.int_], y_in: NDArray[np.int_]) -> None:
            i, name = median_of_list_pair(x_in, y_in)
            zs = [x_in, y_in][name.value]
            self.assertEqual(med_val, zs[i])
            self.assertEqual(true_name, name)

        xs, ys, true_name, med_val = _generate_list_pair(len(self.rand))
        check(xs, ys)

        both = xs.tolist() + ys.tolist()
        small = np.array([min(both) - 1] * (1 + len(both)))
        med_val = np.quantile(small.tolist() + xs.tolist(), 0.5)
        assert med_val == small[0]
        true_name = ListName.X
        check(small, xs)

        small.resize(len(small) - 1)
        check(small, ys)

        small.resize(0)
        med_val = np.quantile(xs.tolist(), 0.5)
        check(xs, small)
        true_name = ListName.Y
        check(small, xs)
        with self.assertRaisesRegex(AssertionError, "empty input not allowed"):
            check(small, small)

        big = np.array([max(both) + 1] * (1 + len(both)))
        med_val = np.quantile(big.tolist() + xs.tolist(), 0.5)
        assert med_val == big[0]
        true_name = ListName.X
        check(big, xs)

        big.resize(len(big) - 1)
        check(big, ys)

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

    @settings(max_examples=500, verbosity=Verbosity.quiet)
    @given(
        xs=st.lists(ST_FINITE_INTEGERS, min_size=1, max_size=70),
        ys=st.lists(ST_FINITE_INTEGERS, min_size=1, max_size=70),
    )
    def test_with_hypothesis(self, xs: list[int], ys: list[int]) -> None:
        if (len(xs) + len(ys)) % 2 == 0:
            xs.append(0)
        xs.sort()
        ys.sort()

        both = np.array(sorted(np.concatenate((xs, ys))))
        med_val = int(np.quantile(both, 0.5))
        assert med_val in both

        idx, name = median_of_list_pair(np.array(xs), np.array(ys))
        if name == ListName.X:
            assert xs[idx] == med_val
        else:
            assert ys[idx] == med_val
