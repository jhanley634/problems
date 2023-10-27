# Copyright 2023 John Hanley. MIT licensed.
#
# from https://codereview.stackexchange.com/questions/287649/given-an-array-remove-zero-or-more-elements-to-maximize-the-reduction

import unittest

from beartype import beartype
from nptyping import Int, NDArray, Shape
import numpy as np
import numpy.typing as npt

NDArrayInt = npt.NDArray[np.int_]


def old_loop(vals: list[int]) -> None:
    acc0 = acc1 = 0
    sums = np.zeros((2, len(vals)), dtype=int)

    for i in range(len(vals) - 1, -1, -1):
        acc0 += vals[i] * (-1) ** i
        sums[0][i] = acc0

        acc1 += vals[i] * (-1) ** i * -1
        sums[1][i] = acc1


def sum_of1(vals: list[int]) -> int:
    acc = 0
    factor = 1
    for val in vals:
        acc += val * factor
        factor *= -1
    return acc


@beartype
def sum_of(vals: list[int]) -> int:
    return sum(val * (-1) ** i for i, val in enumerate(vals))


@beartype
def get_sums(vals: list[int]) -> NDArray[Shape["2, *"], Int]:
    acc = np.zeros(2)
    sums = np.zeros((2, len(vals)), dtype=int)  # cumulative sums
    for i in range(len(vals) - 1, -1, -1):
        for j in range(2):
            acc[j] += vals[i] * (-1) ** (i + j)
            sums[j][i] = acc[j]
    return sums


@beartype
def get_best(vals: list[int]) -> list[int]:
    # decision variables: should we drop this element?
    dvs = np.zeros(len(vals), dtype=bool)
    sums = get_sums(vals)
    # So far we have deleted an even number of elements (zero elements),
    # which means we're playing ATM by the "even index is positive" rule.
    j = 0

    # greedy grab:
    for i in range(len(vals) - 1):
        if sums[1 - j][i] < sums[j][i]:
            dvs[i + 1] = True

    return [val for i, val in enumerate(vals) if not dvs[i]]


@beartype
class TestRemovalForMax(unittest.TestCase):
    def test_sum_of(self) -> None:
        self.assertEqual(2, sum_of([4, 1, 2, 3]))
        self.assertEqual(6, sum_of([4, 1, 3]))

    def test_get_best(self) -> None:
        self.assertEqual([4, 2, 3], get_best([4, 1, 2, 3]))
        self.assertEqual(5, sum_of(get_best([4, 1, 2, 3])))
