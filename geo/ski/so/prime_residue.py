#! /usr/bin/env python

from collections.abc import Generator
from math import sqrt
from pathlib import Path

TEMP = Path("/tmp/k")
TEMP.mkdir(exist_ok=True)
OUTFILE = TEMP / "primes.txt"


def gen_primes(max_n: int) -> Generator[int]:
    assert max_n >= 3
    primes = [2]
    yield 2

    for n in range(3, max_n + 1, 2):
        is_prime = True
        root = int(sqrt(n)) + 1

        for p in primes:
            if p > root:
                break
            if n % p == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(n)
            yield n  # Found a prime!


def write_primes(max_n: int = 1_000_000, outfile: Path = OUTFILE) -> None:
    with open(outfile, "w") as fout:
        fout.writelines(f"{prime}\n" for prime in gen_primes(max_n))


if __name__ == "__main__":
    write_primes()
