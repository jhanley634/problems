#! /usr/bin/env python

# Copyright 2022 John Hanley. MIT licensed.
from functools import lru_cache


@lru_cache(maxsize=500)
def collatz(n: int) -> int:
    if n == 1:
        return n
    if n % 2 == 0:
        return 1 + collatz(n // 2)
    return 1 + collatz(3 * n + 1)
