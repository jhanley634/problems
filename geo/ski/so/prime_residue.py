#! /usr/bin/env python

from pathlib import Path

from sympy import isprime

TEMP = Path("/tmp/k")
TEMP.mkdir(exist_ok=True)
OUTFILE = TEMP / "primes.txt"


def gen_primes(max_n: int = 1_000_000, outfile: Path = OUTFILE) -> None:
    with open(outfile, "w") as fout:
        for n in range(max_n):
            if isprime(n):
                fout.write(f"{n}\n")


if __name__ == "__main__":
    gen_primes()
