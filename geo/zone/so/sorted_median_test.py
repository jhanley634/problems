# Copyright 2024 John Hanley. MIT licensed.
import unittest

from hypothesis import given
from hypothesis import strategies as st

from geo.zone.so.sorted_median import (
    SlicedList,
    is_monotonic,
    kth_idx,
    median_general,
    median_of_sorted_lists,
    median_of_sorted_lists_slow,
)

# easily fits within FP 53-bit significand
BIG = 2**52
ST_FINITE_INTEGERS = st.integers(min_value=-BIG, max_value=BIG)


class MedianTest(unittest.TestCase):

    def test_sliced_list(self) -> None:
        a = SlicedList([0, 1, 2, 3, 4])
        self.assertEqual(5, len(a))
        a = a.slice(1)
        self.assertEqual(4, len(a))
        self.assertEqual(4, len(a))
        self.assertEqual(2, a[1])
        self.assertEqual(3, a[2])

        a = a.slice(0, 4)
        self.assertEqual(4, len(a))
        a = a.slice(0, 3)
        self.assertEqual(3, len(a))
        self.assertEqual(3, a[2])
        self.assertEqual([0, 1, 2, 3, 4], a.nums)

        five_primes = [2, 3, 5, 7, 11.0]
        self.assertEqual("[3, 5]", f"{SlicedList(five_primes).slice(1).slice(0, 2)}")
        self.assertEqual("[3, 5]", f"{SlicedList(five_primes).slice(1, 3)}")

    def test_is_monotonic(self) -> None:
        self.assertTrue(is_monotonic([1, 1, 1, 1, 1, 1, 1]))
        self.assertTrue(is_monotonic([1, 1, 2, 2, 3, 4, 4]))
        self.assertTrue(is_monotonic([1, 2, 3, 4, 5, 6, 7]))

    def test_median(self) -> None:
        median = median_general
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([3, 1, 2, 5, 3]), 3)
        self.assertEqual(median([1, 300, 2, 200, 1]), 2)
        self.assertEqual(median([3, 6, 20, 99, 10, 15]), 12.5)

    def test_median_of_sorted_lists_slow(self) -> None:
        self.assertEqual(median_of_sorted_lists_slow([], [1]), 1)

    def test_median_of_sorted_lists(self) -> None:
        median_two = median_of_sorted_lists  # _slow
        self.assertEqual(median_two([], [1]), 1)
        self.assertEqual(median_two([2], []), 2)
        self.assertEqual(median_two([1, 3], [2]), 2)
        self.assertEqual(median_two([0, 0], [0, 0]), 0)
        self.assertEqual(median_two([1, 2], [3, 4]), 2.5)

    def test_using_hypothesis(self) -> None:
        test_median_two()


@given(
    st.lists(
        st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=300
    ),
    st.lists(
        st.floats(allow_nan=False, allow_infinity=False), min_size=0, max_size=300
    ),
)
def test_median_two(
    a: list[float],
    b: list[float],
) -> None:
    if (len(a) + len(b)) % 2 == 0:
        a.append(0)
    a.sort()
    b.sort()
    assert median_of_sorted_lists(a, b) == sorted(a + b)[len(a + b) // 2]


class TestKthIdx(unittest.TestCase):

    def test_case_too_short(self) -> None:
        k = 0
        a = SlicedList([])
        b = SlicedList([])
        with self.assertRaises(AssertionError):
            kth_idx(a, b, k)

    def test_case_length_1(self) -> None:
        k = 0
        a = SlicedList([0])
        b = SlicedList([])
        self.assertEqual((0, 0), kth_idx(a, b, k))
        self.assertEqual((1, 0), kth_idx(b, a, k))

    def test_case_length_2(self) -> None:
        k = 0
        a = SlicedList([0])
        b = SlicedList([1])
        self.assertEqual((0, 0), kth_idx(a, b, k))
        self.assertEqual((1, 0), kth_idx(b, a, k))

    def test_case_length_3(self) -> None:
        k = 0
        a = SlicedList([0, 1])
        b = SlicedList([2])
        self.assertEqual((0, 0), kth_idx(a, b, k))
        self.assertEqual((1, 0), kth_idx(b, a, k))
        k = 1
        self.assertEqual((0, 1), kth_idx(a, b, k))
        self.assertEqual((1, 1), kth_idx(b, a, k))
        k = 2
        self.assertEqual((1, 0), kth_idx(a, b, k))
        self.assertEqual((0, 0), kth_idx(b, a, k))

        a = SlicedList([0, 2])
        b = SlicedList([1])
        k = 0
        self.assertEqual((0, 0), kth_idx(a, b, k))
        self.assertEqual((1, 0), kth_idx(b, a, k))
        k = 1
        self.assertEqual((1, 0), kth_idx(a, b, k))
        self.assertEqual((0, 0), kth_idx(b, a, k))
        k = 2
        self.assertEqual((0, 1), kth_idx(a, b, k))
        self.assertEqual((1, 1), kth_idx(b, a, k))

    def test_case_length_4(self) -> None:
        k = 0
        a = SlicedList([0, 1])
        b = SlicedList([2, 3])
        self.assertEqual((0, 0), kth_idx(a, b, k))
        self.assertEqual((1, 0), kth_idx(b, a, k))
        k = 1
        self.assertEqual((0, 1), kth_idx(a, b, k))
        self.assertEqual((1, 1), kth_idx(b, a, k))
        k = 2
        self.assertEqual((1, 0), kth_idx(a, b, k))
        self.assertEqual((0, 0), kth_idx(b, a, k))
        k = 3
        self.assertEqual((1, 1), kth_idx(a, b, k))
        self.assertEqual((0, 1), kth_idx(b, a, k))

        a = SlicedList([0, 3])
        b = SlicedList([1, 2])
        self.assertEqual((0, 1), kth_idx(a, b, k))
        self.assertEqual((1, 1), kth_idx(b, a, k))

    def test_case_length_9(self) -> None:
        k = 1
        a = SlicedList([3, 4])
        b = SlicedList([])
        self.assertEqual((0, 1), kth_idx(a, b, k))

        k = 4
        a = SlicedList([0, 1, 2, 3, 4])
        b = SlicedList([5])

        self.assertEqual(k + 1, len(a))

        print("\n\n----------")
        # self.assertEqual((0, 4), kth_idx(a, b, k))
        # self.assertEqual((1, 4), kth_idx(b, a, k))
