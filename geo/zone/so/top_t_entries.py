#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# based on https://codereview.stackexchange.com/questions/287745/determine-top-t-values
# cf https://stackoverflow.com/questions/52713266/most-efficient-way-to-get-the-largest-3-elements-of-an-array-using-no-comparison

from collections import Counter
from contextlib import contextmanager
from functools import partial
import unittest

from beartype import beartype
from hypothesis import given
from hypothesis import strategies as st
import numpy as np

cnt: Counter = Counter()  # an event counter


@contextmanager
def count_sort_calls():
    cnt["sort"] = 0
    yield cnt


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
def sort_k(a: np.ndarray, start: int, k: int) -> None:
    """Puts K elements into descending order."""
    # The "top" elements will appear at the front.
    # This is convenient for truncated displays of large arrays.
    assert 0 <= start < len(a)
    cnt["sort"] += 1

    a[start : start + k] = sorted(a[start : start + k], reverse=True)


@beartype
def find_top_t(t: int, a: np.ndarray, k: int = K) -> np.ndarray:
    assert t < K
    assert t <= len(a)
    tombstone = a.min() - 1  # sentinel value
    assert tombstone not in a  # true by construction

    while len(a) > t:
        for i in range(0, len(a), k):
            sort_k(a, i, k)
            a[i + t : i + k] = tombstone
        # Now coalesce the survivors, shrinking the array of candidate answer values.
        a = np.array(list(filter(lambda x: x != tombstone, a)))

    return a[:t]


T = 3

_big = 2**63 - 1
_small_integers = partial(st.integers, min_value=-_big, max_value=_big)


class TestTopT(unittest.TestCase):
    def test_roll(self) -> None:
        a = roll_some_numbers()
        self.assertLess(a[0], a[-1])

    def test_sorted_slice(self) -> None:
        a = np.array(range(8))

        sort_k(a, 2, k=3)
        self.assertEqual([0, 1, 4, 3, 2, 5, 6, 7], a.tolist())

        sort_k(a, 2, K)
        self.assertEqual([0, 1, 6, 5, 4, 3, 2, 7], a.tolist())

        a.sort()
        sort_k(a, 6, K)  # Partial sort, at end of array, works as expected.
        self.assertEqual([0, 1, 2, 3, 4, 5, 7, 6], a.tolist())

    def test_top_t(self, t=T) -> None:
        a = roll_some_numbers(10)
        with count_sort_calls() as cnt:
            xs = find_top_t(t, a.copy()).tolist()
        self.assertEqual(5, cnt["sort"])
        self.assertEqual(sorted(xs, reverse=True), xs)
        self.assertEqual(sorted(a, reverse=True)[:t], xs)

    @given(st.lists(_small_integers(), min_size=T, max_size=100))
    def test_with_hypothesis(self, lst: list[int]) -> None:
        a = np.array(lst)
        xs = find_top_t(T, a.copy()).tolist()
        self.assertEqual(xs, sorted(xs, reverse=True))
        self.assertEqual(xs, sorted(a, reverse=True)[:T])
