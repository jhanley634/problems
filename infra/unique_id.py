#! /usr/bin/env python
from random import randrange
import datetime as dt


def int_to_mm_dd(n: int):
    assert 0 <= n < 365, n
    jan1 = dt.date.toordinal(dt.date(1970, 1, 1))
    day = dt.date.fromordinal(jan1 + n)
    return day.strftime("%m-%d")


def main():
    assert int_to_mm_dd(0) == "01-01"
    assert int_to_mm_dd(364) == "12-31"

    day = int_to_mm_dd(randrange(365))
    n = randrange(int(1e4))
    print(f"{day}   {n:04d}")


if __name__ == "__main__":
    main()
