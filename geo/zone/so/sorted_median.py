#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from dataclasses import dataclass
from enum import Enum, auto
from random import randrange
from time import time
import unittest

from beartype import beartype
from hypothesis import Verbosity, given, settings
from hypothesis import strategies as st
import numpy as np

# easily fits within FP 53-bit signficand
BIG = 2**52
ST_FINITE_INTEGERS = st.integers(min_value=-BIG, max_value=BIG)


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
        if left_elim < target and len(r0) > 0 and len(r1) > 0:
            if xs[r0.start] <= ys[r1.start]:  # min_y
                r0.start += 1
                left_elim += 1

        if left_elim < target and len(r0) > 0 and len(r1) > 0:
            if ys[r1.start] <= xs[r0.start]:  # min_x
                r1.start += 1
                left_elim += 1

        if right_elim < target and len(r0) > 0 and len(r1) > 0:
            if xs[r0.stop - 1] >= ys[r1.stop - 1]:  # max_y
                r0.stop -= 1
                right_elim += 1

        if right_elim < target and len(r0) > 0 and len(r1) > 0:
            if ys[r1.stop - 1] >= xs[r0.stop - 1]:  # max_x
                r1.stop -= 1
                right_elim += 1

    assert len(r0) + len(r1) == 1  # Found it!

    if len(r0) == 1:
        return r0.start, ListName.X
    else:
        return r1.start, ListName.Y


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
    return xs, ys, name, med_val


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
        def check(x_in, y_in):
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
