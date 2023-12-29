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
def sort_k(a: np.ndarray, start: int, k: int) -> None:
    """Puts K elements into ascending order."""
    assert 0 <= start < len(a)
    assert 0 < k <= len(a)
    cnt["sort"] += 1

    a[start : start + k] = sorted(a[start : start + k])


class TestTopT(unittest.TestCase):
    def test_sorted_slice(self) -> None:
        a = np.array(list(reversed(range(7))))
        sort_k(a, 2, 3)
        self.assertEqual([6, 5, 2, 3, 4, 1, 0], a.tolist())
