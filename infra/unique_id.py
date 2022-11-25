#! /usr/bin/env python
from pprint import pp
from random import randrange
import datetime as dt

from cluster.jutland.dataset import Dataset


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
    print(f"{day}   {n:04d}\n")
    pp(dict(day=day, n=n), width=16)


if __name__ == "__main__":
    assert Dataset().get_df().shape == (25431, 4)  # cols are: osm_id, lon, lat, alt
    main()
