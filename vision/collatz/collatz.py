#! /usr/bin/env python
from functools import lru_cache


def collatz(n):
    if n == 1:
        return n
    elif n % 2 == 0:
        return 1 + collatz(n // 2)
    else:
        return 1 + collatz(3 * n + 1)
