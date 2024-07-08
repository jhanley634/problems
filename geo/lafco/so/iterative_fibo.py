#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from functools import cache

from linetimer import CodeTimer
import typer


def iterative_fibo(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@cache
def recursive_fibo(n: int) -> int:
    if n < 2:
        return n
    return recursive_fibo(n - 1) + recursive_fibo(n - 2)


def binet_fibo(n: int) -> int:
    phi = (1 + 5**0.5) / 2
    return int((phi**n - (-phi) ** -n) / 5**0.5)


def main(n: int, reps: int = 2) -> None:
    for _ in range(reps):
        run(n)


def run(n: int) -> None:
    with CodeTimer(f"iterative {n}"):
        iterative_fibo(n)

    with CodeTimer(f"recursive {n}"):
        recursive_fibo(n)


def compare_timings() -> None:
    answer = 280571172992510140037611932413038677189525

    with CodeTimer("iterative"):
        assert answer == iterative_fibo(200)

    with CodeTimer("recursive"):
        assert answer == recursive_fibo(200)

    # Alas, FP is no match for BigInt.
    for n in range(72):
        assert binet_fibo(n) == iterative_fibo(n)
    for n in range(86):
        assert binet_fibo(n) - iterative_fibo(n) < 1000
    n = 72
    assert binet_fibo(n) == iterative_fibo(n) + 1
    n -= 1
    with CodeTimer("analytic "):
        assert binet_fibo(n) == iterative_fibo(n)


if __name__ == "__main__":
    typer.run(main)
