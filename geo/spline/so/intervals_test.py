# Copyright 2024 John Hanley. MIT licensed.

from datetime import datetime, timedelta
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

    def test_exclude_method_no_overlap(self) -> None:
        interval = Interval(
            (self.jan1 + timedelta(days=31)).timestamp(),
            (self.jan1 + timedelta(days=60)).timestamp(),
        )
        self.intervals.exclude(interval)

        self.assertIn(interval, self.intervals.intervals)
        self.intervals.check()

    def test_exclude_method_overlap(self) -> None:
        overlapping_interval = Interval(
            (self.jan1 + timedelta(days=10)).timestamp(),
            (self.jan1 + timedelta(days=35)).timestamp(),
        )
        with self.assertRaises(ValueError):
            self.intervals.exclude(overlapping_interval)
