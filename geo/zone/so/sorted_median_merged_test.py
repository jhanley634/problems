# Copyright 2024 John Hanley. MIT licensed.
import unittest

from geo.zone.so.sorted_median_merged import Elt, Merged, s_m_merged_median_index


def _get_a() -> list[int]:
    return [4, 6]


def _get_b() -> list[int]:
    return [1, 3, 5]


class SortedMedianMergedTest(unittest.TestCase):
    def test_merged(self) -> None:
        m = Merged(_get_a(), _get_b())
        assert m

    def test_median(self) -> None:
        self.assertEqual(
            Elt(3, 1, 1),
            s_m_merged_median_index(_get_a(), _get_b()),
        )

        m = Merged(_get_a(), _get_b())
        self.assertEqual(
            m.merged[len(m) // 2],
            s_m_merged_median_index(_get_a(), _get_b()),
        )
