#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# loosely based on specification from https://codereview.stackexchange.com/questions/294778/range-exclusion-function

from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import total_ordering
from pprint import pp
from random import random

from sortedcontainers import SortedList


@dataclass
@total_ordering
class Interval:
    start: float
    end: float

    def __contains__(self, x: float) -> bool:
        return self.start <= x < self.end

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return self.start < other.start
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return self.start == other.start and self.end == other.end
        return False


@dataclass
class Intervals:
    intervals: SortedList[Interval]

    def check(self) -> None:
        """Verifies class invariant: the intervals are non-overlapping and in sorted order."""
        for i, interval in enumerate(self.intervals):
            assert interval.start < interval.end
            if i > 0:
                assert self.intervals[i - 1].end < self.intervals[i].start

    def __contains__(self, x: float) -> bool:
        i = self.intervals.bisect_left(Interval(x, x))
        if i == 0:
            return False
        return x in self.intervals[i - 1]

    def exclude(self, interval: Interval) -> None:
        i = self.intervals.bisect_left(interval)
        if i == 0:
            self.intervals.add(interval)
            return
        if interval.start < self.intervals[i - 1].end:
            raise ValueError(f"Overlap with {self.intervals[i - 1]}")
        self.intervals.add(interval)


def main() -> None:
    cur = jan1 = datetime(2024, 1, 1)
    end = jan1 + timedelta(days=3.66)
    free_intervals = Intervals(
        SortedList(
            [Interval(jan1.timestamp(), (jan1 + timedelta(days=365)).timestamp())]
        )
    )
    free_intervals.check()
    while cur < end:
        cur += timedelta(days=1 * random())
        free_intervals.exclude(
            Interval(cur.timestamp(), cur.timestamp() + 2 * random())
        )

    free_intervals.check()
    pp(free_intervals.intervals)


if __name__ == "__main__":
    main()
