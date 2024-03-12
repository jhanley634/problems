#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/290899/leetcode-steps-to-make-array-non-decreasing

from collections.abc import Iterable
import unittest

from beartype import beartype


@beartype
def get_non_descending_runs(a: list[int]) -> Iterable[tuple[int, int]]:
    """Yields initial value and length of each monotonic run in the input.

    The input array of integers must be nonempty.
    """
    idx = 0
    for initial_value, count in _get_non_descending_runs_at(idx, a):
        yield initial_value, count
        idx += count


@beartype
def _get_non_descending_runs_at(idx: int, a: list[int]) -> Iterable[tuple[int, int]]:
    0


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
        # with self.assertRaises(IndexError):
        #     list(get_non_descending_runs([]))

        # self.assertEqual([(42, 1)], list(get_non_descending_runs([42])))
        self.assertEqual([(42, 2)], list(get_non_descending_runs([42, 43])))
        self.assertEqual([(42, 2)], list(get_non_descending_runs([42, 42])))
        self.assertEqual([(42, 1)], list(get_non_descending_runs([42, 41])))
        self.assertEqual([(42, 1)], list(get_non_descending_runs([42, 41, 40])))

        up_twice = [10, 1, 2, 3, 4, 5, 6, 1, 2, 3]
        self.assertEqual([(10, 1)], list(get_non_descending_runs(up_twice)))
