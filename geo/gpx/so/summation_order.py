#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# based on https://codereview.stackexchange.com/questions/289321/demonstrate-effects-of-summation-order

from typing import Generator, Iterable

from numpy.random import permutation, seed


def _get_nums(k: int, r: Iterable[int]) -> Generator[float, None, None]:
    for i in r:
        yield i / k


def _display(label: str, k: int, result: float) -> None:
    print(f"{label} {k:4}   {float.hex(result):22s}   {result}")


def add_doubles(n: int = 5_000_000) -> None:
    seed(42)

    # dividing by K ensures we have lots of mantissa bits set
    for k in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        expected = n * (n - 1) / 2 / k
        print()
        _display("asc", k, expected - sum(_get_nums(k, range(n))))
        _display("dec", k, expected - sum(_get_nums(k, reversed(range(n)))))
        _display("rnd", k, expected - sum(permutation(range(n)) / k))


if __name__ == "__main__":
    add_doubles()
