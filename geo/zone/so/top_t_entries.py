#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# based on https://codereview.stackexchange.com/questions/287745/determine-top-t-values
# cf https://stackoverflow.com/questions/52713266/most-efficient-way-to-get-the-largest-3-elements-of-an-array-using-no-comparison

from collections import Counter
import unittest

from beartype import beartype
import numpy as np

cnt = Counter()  # an event counter


@beartype
def roll_some_numbers(n: int = 1000) -> np.ndarray[int, np.dtype[np.int_]]:
    """Produces N distinct random integers that are conveniently small."""
    # Leaving room between entries deals with pigeonhole principle & birthday paradox.
    big_n = int(1.5 * n)

    a = np.random.randint(0, big_n, 2 * big_n)
    a = np.array(sorted(set(a.tolist()))[:n])
    assert len(a) == n
    return a


K = 5


@beartype
def sort_k(a: np.ndarray, start: int, k: int = K) -> None:
    """Puts K elements into descending order."""
    # The "top" elements will appear at the front.
    # This is convenient for truncated displays of large arrays.
    assert 0 <= start < len(a)
    assert 0 < k <= len(a)
    cnt["sort"] += 1

    a[start : start + k] = sorted(a[start : start + k], reverse=True)


@beartype
def find_top_t(t: int, a: np.ndarray) -> np.ndarray:
    0


class TestTopT(unittest.TestCase):
    def test_roll(self) -> None:
        a = roll_some_numbers()
        self.assertLess(a[0], a[-1])

    def test_sorted_slice(self) -> None:
        a = np.array(range(8))
        sort_k(a, 2, k=3)
        self.assertEqual([0, 1, 4, 3, 2, 5, 6, 7], a.tolist())
        sort_k(a, 2)
        self.assertEqual([0, 1, 6, 5, 4, 3, 2, 7], a.tolist())
