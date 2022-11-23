#! /usr/bin/env python
from queue import PriorityQueue
import datetime as dt

import numpy as np


class GenerateCalls:
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

        self.q: PriorityQueue = PriorityQueue()
        self.rng = np.random.default_rng()
        self.id_ = 0  # serial

    def gen_continuous(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
    ):
        t = start_time
        while t < end_time:
            t += dt.timedelta(seconds=self.rng.exponential(1 / self.arrival_rate))
            yield self._produce_event(t)

    def gen_discrete(
        self,
        start: dt.datetime,
        end: dt.datetime,
    ):
        one_second = dt.timedelta(seconds=1)
        t = start
        while t < end:
            # cf np.random.poisson() & np.random.exponential()
            num_events = self.rng.poisson(self.arrival_rate)
            for _ in range(num_events):
                yield self._produce_event(t)
            t += one_second

    def _produce_event(self, t: dt.datetime):
        sec = self.rng.normal(self.call_duration, self.variance)
        sec = max(5, sec)  # call length cannot be super short, definitely not negative
        sec += 1e-6
        dur = dt.timedelta(seconds=sec)
        self.id_ += 1
        self.q.put((t + dur, self.id_))
        return t, dur, self.id_


def max_occupancy():
    events = []
    gen = GenerateCalls()
    for stamp, _, _ in gen.gen_continuous(
        dt.datetime.now(),
        dt.datetime.now() + dt.timedelta(seconds=1_200),
    ):
        events.append((stamp, 1))  # arrival will increment occupancy

    while len(gen.q.queue) > 0:
        stamp, _ = gen.q.get()
        events.append((stamp, -1))  # and a departure decrements it

    max_occ = occ = 0
    for _, delta in sorted(events):
        occ += delta
        max_occ = max(max_occ, occ)

    print(f"maximum occupancy was {max_occ}")


if __name__ == "__main__":
    max_occupancy()
