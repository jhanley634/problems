# Copyright 2023 John Hanley. MIT licensed.
from itertools import pairwise

from beartype import beartype
import numpy as np


@beartype
def _monotonic(a: np.ndarray[int, np.dtype[np.int_]]) -> bool:
    return bool(np.all(np.diff(a) >= 0))


class SlicedList:
    """Models a slice of a list using start and end index, with zero copies."""

    def __init__(
        self, nums: list[float], start: int = 0, end: int | None = None
    ) -> None:
        self.nums = nums
        self.start = start
        self.end = len(nums) if end is None else end

    def slice(self, start: int, end: int | None = None) -> "SlicedList":
        length = self.end - self.start
        end_i: int = length if end is None else end
        assert 0 <= start <= end_i <= length

        return SlicedList(self.nums, self.start + start, self.start + end_i)

    def __getitem__(self, i: int) -> float:
        return self.nums[self.start + i]

    def __len__(self) -> int:
        return self.end - self.start

    def __str__(self) -> str:
        return str(self.nums[self.start : self.end])

    def __repr__(self) -> str:
        return f"SlicedList({self}, {self.start}, {self.end})"


def median_general(nums: list[float]) -> float:
    return median_sorted(sorted(nums))


def median_sorted(nums: list[float]) -> float:
    """Given a sorted list of numbers, return the median in O(1) constant time."""
    n = len(nums)
    if n % 2 == 0:
        return (nums[n // 2 - 1] + nums[n // 2]) / 2
    return nums[n // 2]


def is_monotonic(nums: list[float]) -> bool:
    return all(a <= b for a, b in pairwise(nums))


def median_of_sorted_lists_slow(a: list[float], b: list[float]) -> float:
    """Given two sorted lists of numbers, return the median in O(n log n) time."""
    assert is_monotonic(a)
    assert is_monotonic(b)
    return median_sorted(sorted(a + b))


def median_of_sorted_lists(a_in: list[float], b_in: list[float]) -> float:
    """Given two sorted lists of numbers, return the median in O(log n) time."""
    n = len(a_in) + len(b_in)
    a = SlicedList(a_in)
    b = SlicedList(b_in)
    if n % 2 == 0:
        return (kth(a, b, n // 2 - 1) + kth(a, b, n // 2)) / 2
    return kth(a, b, n // 2)


def kth(a: SlicedList, b: SlicedList, k: int) -> float:  # noqa PLR0911
    """Return (list_id, idx) in O(log n) time.

    list_id: 0 for a, 1 for b, according to which contains the median value
    idx: index of the median in either list a or b.
    """
    assert 0 <= k < len(a) + len(b), f"{k}, {a}, {b}"
    if not a:
        return b[k]
    if not b:
        return a[k]
    if k == 0:
        return min(a[0], b[0])

    # binary search
    ia, ib = len(a) // 2, len(b) // 2
    if ia + ib < k:
        if a[ia] > b[ib]:
            return kth(a, b.slice(ib + 1), k - ib - 1)
        return kth(a.slice(ia + 1), b, k - ia - 1)
    if a[ia] > b[ib]:
        return kth(a.slice(0, ia), b, k)
    return kth(a, b.slice(0, ib), k)


def kth_idx(a: SlicedList, b: SlicedList, k: int) -> tuple[int, int]:  # noqa PLR0911
    """Given two sorted lists of numbers, return (list_id, idx) in O(log n) time.

    We are concerned with the kth element of the merged lists a and b.

    list_id: 0 for a, 1 for b, according to which contains the kth sorted value
    idx: index of the kth element in either list a or b
    """
    # print()
    # print("\n", a, b, k)
    assert len(a) + len(b) > 0
    assert 0 <= k < len(a) + len(b), f"{k}, {a}, {b}"
    if not a:
        return 1, k
    if not b:
        return 0, k
    if k == 0:
        return int(a[0] > b[0]), k

    # binary search
    ia, ib = len(a) // 2, len(b) // 2
    if ia + ib < k:
        if a[ia] > b[ib]:
            return kth_idx(a, b.slice(ib + 1), k - ib - 1)
        return kth_idx(a.slice(ia + 1), b, k - ia - 1)

    # print(a[ia], b[ib], a[ia] > b[ib])

    if a[ia] > b[ib]:
        return kth_idx(a.slice(0, ia), b, k)
    return kth_idx(a, b.slice(0, ib), k)


def median_idx_of_sorted_lists(a_in: list[float], b_in: list[float]) -> float:
    """Given two sorted lists of numbers, return (list_id, idx) in O(log n) time.

    list_id: 0 for a, 1 for b, according to which contains the median value
    idx: index of the median in either list a or b
    """
