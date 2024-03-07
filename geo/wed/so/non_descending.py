#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/290899/leetcode-steps-to-make-array-non-decreasing

from collections.abc import Iterable
import math
import unittest

from beartype import beartype


@beartype
def get_non_descending_runs(a: list[int]) -> Iterable[tuple[int, int]]:
    """Yields initial value and length of each monotonic run in the input.

    The input array of integers must be nonempty.
    """
    yield from _get_non_descending_runs_at(0, a)


@beartype
def _get_non_descending_runs_at(idx: int, a: list[int]) -> Iterable[tuple[int, int]]:
    initial_value = a[idx]
    count = 1

    direction = 1
    idx += 1
    if idx < len(a):
        direction = _sgn(a[idx] - a[idx - 1])

    while idx < len(a) and direction == _sgn(a[idx] - a[idx - 1]):
        idx += 1
        count += 1

    yield initial_value, count


@beartype
def _sgn(x: int) -> int:
    return int(math.copysign(1.0, x))
    # """Returns math.copysign(1, x) for nonzero x (±1), else 0."""
    # return (x > 0) - (x < 0)


@beartype
def total_steps(a: Iterable[int]) -> int:
    total_count = count = 0
    if not a:  # not strictly needed, since input is specified to be nonempty
        return total_count

    # lowest acceptable number for remaining entries to the right
    nums = iter(a)
    lowest = next(nums)

    for val in nums:
        if val < lowest:
            count += 1  # extend a "discard" span of entries
        else:
            total_count = max(total_count, count)
            count = 0  # we're back to accepting monotonic entries

        lowest = max(lowest, val)

    return max(total_count, count)


class NonDescendingTest(unittest.TestCase):
    def test_non_descending(self) -> None:
        self.assertEqual(0, total_steps(range(0)))
        self.assertEqual(0, total_steps(()))
        self.assertEqual(0, total_steps([]))
        self.assertEqual(3, total_steps([5, 3, 4, 4, 7, 3, 6, 11, 8, 5, 11]))
        self.assertEqual(0, total_steps([4, 5, 7, 7, 13]))
        # self.assertEqual(6, total_steps([10, 1, 2, 3, 4, 5, 6, 1, 2, 3]))
        self.assertEqual(0, total_steps([3, 4]))
        self.assertEqual(1, total_steps([4, 3]))
        self.assertEqual(1, total_steps([4, 3, 5]))
        self.assertEqual(2, total_steps([4, 3, 3]))
        self.assertEqual(2, total_steps([4, 3, 3, 5]))
        self.assertEqual(1, total_steps([4, 3, 14, 13]))
        self.assertEqual(2, total_steps([4, 3, 3, 14, 13]))
        self.assertEqual(3, total_steps([4, 3, 3, 3, 14, 13]))
        self.assertEqual(3, total_steps((4, 3, 3, 3, 14, 13)))
        self.assertEqual(0, total_steps(range(1, 1_000)))
        self.assertEqual(999, total_steps(range(1_000, 0, -1)))

    def test_get_monotonic_runs(self) -> None:
        with self.assertRaises(IndexError):
            list(get_monotonic_runs([]))

        self.assertEqual([(42, 1)], list(get_monotonic_runs([42])))
        self.assertEqual([(42, 2)], list(get_monotonic_runs([42, 43])))
        self.assertEqual([(42, 2)], list(get_monotonic_runs([42, 42])))
        self.assertEqual([(42, 2)], list(get_monotonic_runs([42, 41])))
        self.assertEqual([(42, 3)], list(get_monotonic_runs([42, 41, 40])))

        self.assertEqual(
            [(10, 2)],
            list(get_monotonic_runs([10, 1, 2, 3, 4, 5, 6, 1, 2, 3])),
        )
