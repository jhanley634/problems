#! /usr/bin/env python
from queue import PriorityQueue
import datetime as dt

import numpy as np


class GenerateCallers:
    def __init__(
        self, arrival_rate: float = 1 / 30.0  # λ: expect a call every thirty seconds
    ):
        self.arrival_rate = arrival_rate
        self.q: PriorityQueue = PriorityQueue()
        self.rng = np.random.default_rng()
        self.id_ = 0  # serial

    def gen_continuous(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        call_duration_sec: float = 20,
    ):
        t = start_time
        while t < end_time:
            # advance time to the next event
            t += dt.timedelta(seconds=self.rng.exponential(1 / self.arrival_rate))
            dur = dt.timedelta(seconds=call_duration_sec)
            self.id_ += 1
            self.q.put((t + dur, self.id_))
            yield t, dur, self.id_

    def gen_discrete(
        self,
        start: dt.datetime,
        end: dt.datetime,
        call_duration_sec: float = 20,
    ):
        one_second = dt.timedelta(seconds=1)
        t = start
        while t < end:
            # cf np.random.poisson() & np.random.exponential()
            num_events = self.rng.poisson(self.arrival_rate)
            for _ in range(num_events):
                dur = dt.timedelta(seconds=call_duration_sec)
                self.id_ += 1
                self.q.put((t + dur, self.id_))
                yield t, dur, self.id_

            t += one_second


if __name__ == "__main__":
    gen = GenerateCallers()
    for stamp, duration, id_ in gen.gen_continuous(
        dt.datetime.now(),
        dt.datetime.now() + dt.timedelta(seconds=1_200),
    ):
        print(stamp, " ", duration, " ", id_)
