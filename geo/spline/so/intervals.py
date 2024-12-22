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
        """Verifies class invariant: the intervals are non-overlapping."""
        for i, interval in enumerate(self.intervals):
            assert interval.start < interval.end
            if i > 0:
                assert self.intervals[i - 1].end < self.intervals[i].start

    def __contains__(self, x: float) -> bool:
        i = self.intervals.bisect_left(Interval(x, x))
        if i == 0:
            return x in self.intervals[i]
        return x in self.intervals[i - 1]

    def exclude(self, interval: Interval) -> None:
        """Removes the given interval from the free intervals, by splitting it."""
        i = self.intervals.bisect_left(interval)
        if i == 0:
            return
        i -= 1
        if self.intervals[i].start < interval.start:
            self.intervals.add(Interval(self.intervals[i].start, interval.start))
        if interval.end < self.intervals[i].end:
            self.intervals.add(Interval(interval.end, self.intervals[i].end))
        self.intervals.remove(self.intervals[i])


def round3(x: float) -> float:
    return round(x, 3)


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
        cur += timedelta(days=1 * round3(random()))
        free_intervals.exclude(
            Interval(cur.timestamp(), cur.timestamp() + 2 * round3(random()))
        )

    free_intervals.check()
    pp(list(free_intervals.intervals))


if __name__ == "__main__":
    main()
