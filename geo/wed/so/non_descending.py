#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/290899/leetcode-steps-to-make-array-non-decreasing

import unittest


def total_steps(a: list[int]) -> int:
    total_count = count = 0
    if not a:  # not strictly needed, since input is specified to be nonempty
        return total_count

    # lowest acceptable number for remaining entries to the right
    lowest = a[0]

    i = 1
    while i < len(a):
        if a[i] < lowest:
            count += 1  # extend a "discard" span of entries
        else:
            total_count = max(total_count, count)
            count = 0  # we're back to accepting monotonic entries

        lowest = max(lowest, a[i])
        i += 1

    return max(total_count, count)


class NonDescendingTest(unittest.TestCase):
    def test_non_descending(self) -> None:
        self.assertEqual(0, total_steps([]))
        self.assertEqual(3, total_steps([5, 3, 4, 4, 7, 3, 6, 11, 8, 5, 11]))
        self.assertEqual(0, total_steps([4, 5, 7, 7, 13]))
        self.assertEqual(1, total_steps([4, 3]))
        self.assertEqual(1, total_steps([4, 3, 5]))
        self.assertEqual(2, total_steps([4, 3, 3]))
        self.assertEqual(2, total_steps([4, 3, 3, 5]))
        self.assertEqual(1, total_steps([4, 3, 14, 13]))
        self.assertEqual(2, total_steps([4, 3, 3, 14, 13]))
        self.assertEqual(3, total_steps([4, 3, 3, 3, 14, 13]))
        self.assertEqual(0, total_steps(list(range(1, 1_000))))
        self.assertEqual(999, total_steps(list(range(1_000, 0, -1))))
