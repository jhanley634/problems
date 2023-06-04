#! /usr/bin/env python3
# Copyright 2023 John Hanley. MIT licensed.
# from slide 3 of https://dabeaz.com/python/GIL.pdf

from threading import Thread
from time import time
import sys

N = 100_000_000


def count(n):
    while n > 0:
        n -= 1


def serial_counts(n: int = N) -> float:
    t0 = time()
    count(n)
    count(n)
    return round(time() - t0, 3)


def parallel_counts(n: int = N) -> float:
    t0 = time()
    t1 = Thread(target=count, args=(n,))
    t2 = Thread(target=count, args=(n,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return round(time() - t0, 3)


if __name__ == "__main__":
    assert 0.005 == sys.getswitchinterval()
    # This produces no noticeable change in the timing figures.
    sys.setswitchinterval(0.1)

    print(serial_counts(), "seconds for sequential")
    print(parallel_counts(), "seconds for parallel")
