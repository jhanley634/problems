#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/77817417/how-to-add-a-column-in-a-csv-file-to-count-the-amount-of-classes
from collections.abc import Generator
import datetime as dt

from pytz import timezone
import pandas as pd


def _get_df() -> pd.DataFrame:
    zone = timezone("America/Los_Angeles")
    start = dt.datetime(2021, 5, 23, 7, 0, tzinfo=zone)
    df = pd.DataFrame(
        {
            "stamp": [start + dt.timedelta(hours=-i) for i in range(7)],
            "class_id": list("AAACBBC"),
        }
    )
    df["count"] = list(_get_counts(df.class_id))
    return df


def _get_counts(s: "pd.Series[str]") -> Generator[int, None, None]:
    prev = None
    count = 1
    for val in s:
        if val == prev:
            count += 1
        else:
            count = 1
        yield count
        prev = val


if __name__ == "__main__":
    print(_get_df())
