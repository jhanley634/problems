#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from collections import namedtuple
from collections.abc import Generator
from queue import PriorityQueue
import datetime as dt

import numpy as np
import pandas as pd


class CallGenerator:
    def __init__(
        self,
        arrival_rate: float = 1 / 30.0,  # expect a call every thirty seconds
        call_duration: float = 28,  # almost one Erlang of call traffic
        variance: float = 15,
    ):
        """Generate call events at random times.

        arrival_rate: λ, in event per second, expect a call every 1 / λ seconds
        call_duration: expected call length, in seconds
        variance: standard deviation of call length, in seconds
        """
        self.arrival_rate = arrival_rate
        self.call_duration = call_duration
        self.variance = variance

        self.q: PriorityQueue[tuple[dt.datetime, int]] = PriorityQueue()
        self.rng = np.random.default_rng()
        self.id_ = 0  # serial

    def gen_continuous(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
    ) -> Generator[tuple[dt.datetime, dt.timedelta, int], None, None]:
        t = start_time
        while t < end_time:
            t += dt.timedelta(seconds=self.rng.exponential(1 / self.arrival_rate))
            yield self._produce_event(t)

    def gen_discrete(
        self,
        start: dt.datetime,
        end: dt.datetime,
    ) -> Generator[tuple[dt.datetime, dt.timedelta, int], None, None]:
        one_second = dt.timedelta(seconds=1)
        t = start
        while t < end:
            # cf np.random.poisson() & np.random.exponential()
            num_events = self.rng.poisson(self.arrival_rate)
            for _ in range(num_events):
                yield self._produce_event(t)
            t += one_second

    def _produce_event(self, t: dt.datetime) -> tuple[dt.datetime, dt.timedelta, int]:
        sec = self.rng.normal(self.call_duration, self.variance)
        sec = max(5, sec)  # call length cannot be super short, definitely not negative
        sec += 1e-6
        dur = dt.timedelta(seconds=sec)
        self.id_ += 1
        self.q.put((t + dur, self.id_))
        return t, dur, self.id_


def _get_gen() -> (
    tuple[CallGenerator, Generator[tuple[dt.datetime, dt.timedelta, int], None, None]]
):
    generator = CallGenerator()
    return generator, generator.gen_continuous(
        dt.datetime.now(),
        dt.datetime.now() + dt.timedelta(seconds=1_200),
    )


def max_occupancy() -> int:
    generator, gen = _get_gen()
    events = [(stamp, 1) for stamp, _, _ in gen]  # arrival will increment occupancy
    while len(generator.q.queue) > 0:
        stamp, _ = generator.q.get()
        events.append((stamp, -1))  # and a departure decrements it

    max_occ = occ = 0
    for _, delta in sorted(events):
        occ += delta
        max_occ = max(max_occ, occ)

    return max_occ


def _get_start_and_end(
    events: pd.DataFrame,
) -> Generator[tuple[dt.datetime, int], None, None]:
    Pair = namedtuple("Pair", ["stamp", "delta"])
    for _, row in events.iterrows():
        yield Pair(row.stamp, 1)  # arrival increment
        yield Pair(row.end, -1)  # departure decrement


def _get_events_dataframe() -> pd.DataFrame:
    Call = namedtuple("Call", "stamp, duration, id_")
    _, gen = _get_gen()
    events = pd.DataFrame([Call(*row) for row in gen])
    events["end"] = events.stamp + events.duration
    events = events[["stamp", "end"]]
    return events


# Compute same thing, in a slightly different way.
def pandas_occ() -> int:
    events = _get_events_dataframe()
    df = pd.DataFrame(sorted(_get_start_and_end(events)))
    df["occupancy"] = df.delta.cumsum()
    return int(df.occupancy.max())


# Compute same thing, avoiding row-by-row iteration.
def pandas_occ2() -> int:
    ev = _get_events_dataframe()
    df = pd.concat([ev.stamp.to_frame(), ev.end.to_frame()])

    df["delta"] = np.where(~df.stamp.isnull(), 1, 0)
    df.delta += np.where(~df.end.isnull(), -1, 0)

    df["stamp"] = df.stamp.combine_first(df.end)
    df = df.sort_values(["stamp"])

    df["occupancy"] = df.delta.cumsum()
    return int(df.occupancy.max())


if __name__ == "__main__":
    print(f"maximum occupancy was {max_occupancy()}")
    print(f"maximum occupancy was  {pandas_occ()}")
    print(f"maximum occupancy was   {pandas_occ2()}")
