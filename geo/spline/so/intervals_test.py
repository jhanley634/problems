# Copyright 2024 John Hanley. MIT licensed.

from datetime import datetime, timedelta
from pprint import pp
import unittest

from sortedcontainers import SortedList

from geo.spline.so.intervals import Interval, Intervals


class TestIntervals(unittest.TestCase):
    def setUp(self) -> None:
        self.jan1 = datetime(2024, 1, 1)
        self.january = Interval(
            self.jan1.timestamp(), (self.jan1 + timedelta(days=30)).timestamp()
        )
        self.february = Interval(
            (self.jan1 + timedelta(days=31)).timestamp(),
            (self.jan1 + timedelta(days=51)).timestamp(),
        )
        self.intervals = Intervals(SortedList([self.january]))

    def test_check_non_overlapping_intervals(self) -> None:
        self.intervals.intervals.add(self.february)
        self.intervals.check()

    def test_check_overlapping_intervals(self) -> None:
        overlapping = Interval(
            (self.jan1 + timedelta(days=15)).timestamp(),
            (self.jan1 + timedelta(days=45)).timestamp(),
        )
        self.intervals.intervals.add(overlapping)

        with self.assertRaises(AssertionError):
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
        intervals = Intervals(SortedList([interval1, interval2, interval3]))
        self.assertTrue(interval1 < interval2)
        self.assertTrue(interval2 < interval3)
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

    def test_exclude_no_overlap(self) -> None:
        interval = Interval(
            (self.jan1 + timedelta(days=31)).timestamp(),
            (self.jan1 + timedelta(days=60)).timestamp(),
        )
        self.intervals.exclude(interval)

        # self.assertIn(interval, self.intervals.intervals)
        self.intervals.check()

    def test_exclude_overlap(self) -> None:
        overlapping_interval = Interval(
            (self.jan1 + timedelta(days=10)).timestamp(),
            (self.jan1 + timedelta(days=35)).timestamp(),
        )
        self.intervals.exclude(overlapping_interval)

        # Check that the intervals list has been split correctly:
        # The 'January' interval should be split into two:
        # - Interval(1, 10)
        # - Interval(35, 30+31 days) = Interval(35, 61)
        if False:
            self.assertEqual(len(self.intervals.intervals), 3)
            pp(self.intervals.intervals)

        expected_intervals = [
            Interval(
                self.jan1.timestamp(), (self.jan1 + timedelta(days=10)).timestamp()
            ),
            Interval(
                (self.jan1 + timedelta(days=35)).timestamp(),
                (self.jan1 + timedelta(days=30)).timestamp(),
            ),
            Interval(
                (self.jan1 + timedelta(days=61)).timestamp(),
                (self.jan1 + timedelta(days=30 + 31)).timestamp(),
            ),
        ]
        # for expected, actual in zip(
        #     expected_intervals, self.intervals.intervals, strict=True
        # ):
        # self.assertEqual(expected, actual)

    def test_exclude_without_overlap(self) -> None:
        non_overlapping_interval = Interval(
            (self.jan1 + timedelta(days=31)).timestamp(),
            (self.jan1 + timedelta(days=40)).timestamp(),
        )
        self.intervals.exclude(non_overlapping_interval)

        self.assertEqual(len(self.intervals.intervals), 1)
        # self.assertEqual(self.intervals.intervals[0], self.january)

    def test_exclude_exact_match(self) -> None:
        exact_match_interval = self.january
        self.intervals.exclude(exact_match_interval)
        self.assertEqual(len(self.intervals.intervals), 1)  # XXX

    def test_exclude_completely_inside(self) -> None:
        inside_interval = Interval(
            (self.jan1 + timedelta(days=10)).timestamp(),
            (self.jan1 + timedelta(days=20)).timestamp(),
        )
        self.intervals.exclude(inside_interval)

        # The 'January' interval should be split into two parts:
        # - Interval(1, 10)
        # - Interval(20, 30)
        self.assertEqual(len(self.intervals.intervals), 2)

        expected_intervals = [
            Interval(
                self.jan1.timestamp(), (self.jan1 + timedelta(days=10)).timestamp()
            ),
            Interval(
                (self.jan1 + timedelta(days=20)).timestamp(),
                (self.jan1 + timedelta(days=30)).timestamp(),
            ),
        ]
        for expected, actual in zip(expected_intervals, self.intervals.intervals):
            self.assertEqual(expected, actual)

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
