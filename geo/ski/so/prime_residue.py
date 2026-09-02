#! /usr/bin/env python

from collections.abc import Generator
from math import sqrt
from pathlib import Path

TEMP = Path("/tmp/k")
TEMP.mkdir(exist_ok=True)
OUTFILE = TEMP / "primes.txt"

_primes = [2]


def gen_primes(max_n: int) -> Generator[int]:
    assert max_n >= 3
    yield 2

    for n in range(3, max_n + 1, 2):
        if _is_prime(n):
            _primes.append(n)
            yield n


def _is_prime(n: int) -> bool:

    root = sqrt(n)

    for p in _primes:
        if p > root:
            return True
        if n % p == 0:
            return False

    return True


def write_primes(max_n: int = 1_000_000, outfile: Path = OUTFILE) -> None:
    with open(outfile, "w") as fout:
        fout.writelines(f"{prime}\n" for prime in gen_primes(max_n))


if __name__ == "__main__":
    write_primes()
