#! /usr/bin/env python
from queue import PriorityQueue
import datetime as dt

import numpy as np


class GenerateCallers:
    def __init__(
        self, arrival_rate: float = 1 / 30.0  # λ: expect a call every thirty seconds
    ):
        self.arrival_rate = arrival_rate
        self.q = PriorityQueue()
        self.rng = np.random.default_rng()
        self.id_ = 1  # serial

    def gen_discrete(
        self, start: dt.datetime, end: dt.datetime, call_duration_sec: float = 20
    ):
        one_second = dt.timedelta(seconds=1)
        t = start
        while t < end:
            # cf np.random.poisson() & np.random.exponential()
            num_events = self.rng.poisson(self.arrival_rate)
            for _ in range(num_events):
                dur = dt.timedelta(seconds=call_duration_sec)
                self.q.put((t + dur, self.id_))
                yield t, dur

            t += one_second


if __name__ == "__main__":
    gen = GenerateCallers()
    for stamp, duration in gen.gen_discrete(
        dt.datetime.now(),
        dt.datetime.now() + dt.timedelta(seconds=1_200),
    ):
        print(stamp, " ", duration)
