#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# based on https://codereview.stackexchange.com/questions/287745/determine-top-t-values
# cf https://stackoverflow.com/questions/52713266/most-efficient-way-to-get-the-largest-3-elements-using-no-comparison
from collections import Counter
from collections.abc import Generator
from contextlib import contextmanager
from functools import partial
from random import shuffle
import unittest

from beartype import beartype
from hypothesis import given
from hypothesis import strategies as st
from numpy.typing import NDArray
import numpy as np

cnt: Counter[str] = Counter()  # an event counter


@contextmanager
def count_sort_calls() -> Generator[Counter[str], None, None]:
    cnt["sort"] = 0
    yield cnt


@beartype
def roll_some_numbers(n: int = 1000) -> NDArray[np.int_]:
    """Produces N distinct random integers that are conveniently small."""
    # Leaving room between entries deals with pigeonhole principle & birthday paradox.
    big_n = int(1.5 * n)

    a = np.random.randint(0, big_n, 2 * big_n)
    a = np.array(sorted(set(a.tolist()))[:n])
    assert len(a) == n
    return a


K = 5


@beartype
def sort_k(a: NDArray[np.int_], start: int, k: int) -> None:
    """Puts K elements into descending order."""
    # The "top" elements will appear at the front.
    # This is convenient for truncated displays of large arrays.
    assert 0 <= start < len(a)
    cnt["sort"] += 1

    a[start : start + k] = sorted(a[start : start + k], reverse=True)


@beartype
def find_top_t(t: int, a: NDArray[np.int_], k: int = K) -> NDArray[np.int_]:
    assert t < K
    assert t <= len(a)
    tombstone = a.min() - 1  # sentinel value
    assert tombstone not in a  # true by construction

    if len(a) <= t:
        sort_k(a, 0, t)
    while len(a) > t:
        for i in range(0, len(a), k):
            sort_k(a, i, k)
            a[i + t : i + k] = tombstone
        # Now coalesce the survivors, shrinking the array of candidate answer values.
        a = np.array(list(filter(lambda x: x != tombstone, a)))

    return a[:t]


T = 3

_moderately_large = 2**63 - 1
# The set of all integers is very, very large,
# and cPython can model a pretty big subset of them.
# Let's restrict the ambitions of `hypothosis` to something more reasonable.
_small_integers = partial(
    st.integers,
    min_value=-_moderately_large,
    max_value=_moderately_large,
)


@beartype
def shuffled(a: list[int]) -> list[int]:
    b = a.copy()
    shuffle(b)
    return b


@beartype
class TestTopT(unittest.TestCase):
    """Verifies that the Right Thing happens, in less than a second."""

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

    def test_top_t(self, t: int = T) -> None:
        a = roll_some_numbers(10)
        with count_sort_calls() as cnt:
            xs = find_top_t(t, a.copy()).tolist()
        self.assertEqual(5, cnt["sort"])
        self.assertEqual(xs, sorted(xs, reverse=True))
        self.assertEqual(xs, sorted(a, reverse=True)[:t])

    def test_with_dups(self, t: int = T, n: int = 10_000) -> None:
        a = np.random.randint(0, n // 2, n)
        self.assertLess(len(set(a)), len(a) / 2)
        xs = find_top_t(t, a.copy()).tolist()
        self.assertEqual(xs, sorted(xs, reverse=True))
        self.assertEqual(xs, sorted(a, reverse=True)[:t])

    def test_imbalanced(self, t: int = T, num_distractors: int = 10_000) -> None:
        with count_sort_calls() as cnt:
            a = np.array(shuffled([1] * t + [0] * num_distractors))
            self.assertEqual([1] * t, find_top_t(t, a).tolist())
        self.assertEqual(num_distractors / 2 + 12, cnt["sort"])

        with count_sort_calls() as cnt:
            a = np.array(shuffled([1] * (t - 1) + [0] * num_distractors))
            self.assertEqual([1] * (t - 1) + [0], find_top_t(t, a).tolist())
        self.assertEqual(num_distractors / 2 + 12, cnt["sort"])

    def test_010(self) -> None:
        a = np.array([0, 1, 0])  # This input vector was surfaced by hypothesis.
        self.assertEqual([1, 0, 0], find_top_t(T, a).tolist())

    @given(st.lists(_small_integers(), min_size=T, max_size=100))
    def test_with_hypothesis(self, lst: list[int]) -> None:
        a = np.array(lst)
        xs = find_top_t(T, a.copy()).tolist()
        self.assertEqual(xs, sorted(xs, reverse=True))
        self.assertEqual(xs, sorted(a, reverse=True)[:T])
