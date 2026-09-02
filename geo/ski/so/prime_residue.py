#! /usr/bin/env python

from collections.abc import Generator
from pathlib import Path

from sympy import isprime

TEMP = Path("/tmp/k")
TEMP.mkdir(exist_ok=True)
OUTFILE = TEMP / "primes.txt"


def gen_primes(max_n: int) -> Generator[int]:
    for n in range(max_n):
        if isprime(n):
            yield n


def write_primes(max_n: int = 1_000_000, outfile: Path = OUTFILE) -> None:
    with open(outfile, "w") as fout:
        fout.writelines(f"{prime}\n" for prime in gen_primes(max_n))


if __name__ == "__main__":
    write_primes()
