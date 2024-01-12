#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from typing import Generator
import csv

import pandas as pd
import polars as pl

FOLDER = Path("~/Desktop").expanduser()
IN_FILE = list(FOLDER.glob("Your Requested OMRON Report from *.csv"))[0]


def _get_rows(in_file: Path) -> Generator[dict[str, str | int], None, None]:
    df = pl.read_csv(in_file)
    expected = "Date|Time|Systolic (mmHg)|Diastolic (mmHg)|Pulse (bpm)|Symptoms|Consumed|TruRead|Notes"
    assert expected == "|".join(df.columns), df.columns

    with open(in_file) as fin:
        sheet = csv.reader(fin)
        next(sheet)  # skip headers
        for row in sheet:
            if not row:
                continue  # ignore final blank line
            stamp = row[0] + " " + row[1]
            s, d, p = map(int, row[2:5])
            yield dict(time=stamp, systolic=s, diastolic=d, pulse=p)


def main(in_file: Path = IN_FILE) -> None:
    df = pd.DataFrame(list(_get_rows(in_file)))
    df["time"] = pd.to_datetime(df.time)
    print(df)
    print(df.dtypes)
    print(df.describe())


if __name__ == "__main__":
    main()
