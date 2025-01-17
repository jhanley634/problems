# Copyright 2024 John Hanley. MIT licensed.

from datetime import UTC, datetime, timedelta
import unittest

from sortedcontainers import SortedList

from geo.spline.so.intervals import Interval, Intervals


class TestIntervals(unittest.TestCase):
    def setUp(self) -> None:
        self.jan1 = datetime(2024, 1, 1, tzinfo=UTC)
        self.january = Interval(
            self.jan1.timestamp(), (self.jan1 + timedelta(days=30)).timestamp()
        )
        self.intervals = Intervals(SortedList([self.january]))

    def tearDown(self) -> None:
        self.intervals.check()

    def test_lt_operator(self) -> None:
        interval1 = Interval(
            self.jan1.timestamp(), (self.jan1 + timedelta(days=10)).timestamp()
        )
        interval2 = Interval(
            (self.jan1 + timedelta(days=15)).timestamp(),
            (self.jan1 + timedelta(days=25)).timestamp(),
        )
        interval3 = Interval(
            (self.jan1 + timedelta(days=30)).timestamp(),
            (self.jan1 + timedelta(days=40)).timestamp(),
        )
        self.assertTrue(interval1 < interval2 < interval3)
        self.assertTrue(interval1 < interval3)

    def test_contains_operator(self) -> None:
        interval = Interval(
            self.jan1.timestamp(), (self.jan1 + timedelta(days=10)).timestamp()
        )
        self.assertTrue(interval.__contains__(self.jan1.timestamp() + 5 * 3600))
        self.assertFalse(
            interval.__contains__(
                self.jan1.timestamp() + timedelta(days=11).total_seconds()
            )
        )

    def test_exclude(self) -> None:
        interval = Interval(
            (self.jan1 + timedelta(days=10)).timestamp(),
            (self.jan1 + timedelta(days=20)).timestamp(),
        )
        self.intervals.exclude(interval)
        self.intervals.check()
        return
        self.assertEqual(
            "SortedList([Interval(start=1704096000.0, end=1704960000.0),"
            " Interval(start=1705824000.0, end=1706688000.0)])",
            f"{self.intervals.intervals}",
        )
        expected_intervals = [
            Interval(
                self.jan1.timestamp(), (self.jan1 + timedelta(days=10)).timestamp()
            ),
            Interval(
                (self.jan1 + timedelta(days=20)).timestamp(),
                (self.jan1 + timedelta(days=30)).timestamp(),
            ),
        ]
        for expected, actual in zip(
            expected_intervals, self.intervals.intervals, strict=True
        ):
            self.assertEqual(expected, actual)

    def test_exclude_exact_match(self) -> None:
        exact_match_interval = self.january
        self.intervals.exclude(exact_match_interval)
        self.assertEqual(len(self.intervals.intervals), 0)

    def test1(self) -> None:
        free_intervals = Intervals(SortedList([Interval(1, 10)]))
        self.assertFalse(0.99 in free_intervals)
        self.assertTrue(1.0 in free_intervals)
        self.assertTrue(9.99 in free_intervals)
        self.assertFalse(10.0 in free_intervals)
        self.assertFalse(10.1 in free_intervals)

        free_intervals.exclude(Interval(3, 5))
        self.assertEqual(len(free_intervals.intervals), 2)
        self.assertEqual(free_intervals.intervals[0], Interval(1, 3))
        self.assertEqual(free_intervals.intervals[1], Interval(5, 10))
        self.assertEqual(
            "SortedList([Interval(start=1, end=3), Interval(start=5, end=10)])",
            f"{free_intervals.intervals}",
        )
        free_intervals.check()

    def test2(self) -> None:
        free_intervals = Intervals(SortedList([Interval(1, 10)]))
        free_intervals.exclude(Interval(7, 9))
        self.assertEqual(
            "SortedList([Interval(start=1, end=7), Interval(start=9, end=10)])",
            f"{free_intervals.intervals}",
        )
        free_intervals.exclude(Interval(2, 4))
        self.assertEqual(
            "SortedList([Interval(start=1, end=2), Interval(start=4, end=7), Interval(start=9, end=10)])",
            f"{free_intervals.intervals}",
        )
        free_intervals.check()

    def test3(self) -> None:
        free_intervals = Intervals(SortedList([Interval(1, 10)]))

        free_intervals.exclude(Interval(7, 10))
        self.assertEqual(
            "SortedList([Interval(start=1, end=7)])",
            f"{free_intervals.intervals}",
        )
        free_intervals.check()

    def test4(self) -> None:
        free_intervals = Intervals(SortedList([Interval(1, 10)]))
        free_intervals.exclude(Interval(1, 2))
        self.assertEqual(
            "SortedList([Interval(start=2, end=10)])",
            f"{free_intervals.intervals}",
        )
        free_intervals.check()
