#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from subprocess import run
from typing import Generator
import csv
import io

import polars as pl

FOLDER = Path("~/Desktop").expanduser()
# Grab the most recent observations.
IN_FILE = list(FOLDER.glob("Your Requested OMRON Report from *.csv"))[-1]
OUT_FILE = FOLDER / "blood_pressure.csv"


def _get_rows(in_file: Path) -> Generator[dict[str, str | int], None, None]:
    df = pl.read_csv(in_file)
    expected = "Date|Time|Systolic (mmHg)|Diastolic (mmHg)|Pulse (bpm)|Symptoms|Consumed|TruRead|Notes"
    assert expected == "|".join(df.columns), df.columns

    with open(in_file, encoding="utf8") as fin:
        sheet = csv.reader(fin)
        next(sheet)  # skip headers
        for row in sheet:
            if not row:
                continue  # ignore final blank line
            stamp = row[0] + " " + row[1]
            s, d, p = map(int, row[2:5])
            yield {"time": stamp, "systolic": s, "diastolic": d, "pulse": p}


def get_bp_table(in_file: Path = IN_FILE, out_file: Path = OUT_FILE) -> str:
    df = pl.DataFrame(list(_get_rows(in_file)))
    df = df.with_columns(pl.col("time").str.to_datetime("%b %d %Y %I:%M %p"))
    df = df.with_columns(df["time"].dt.strftime("%Y-%m-%dT%H:%M"))

    buf = io.BytesIO()
    df.write_csv(buf)
    txt = buf.getvalue().decode().replace(",", ", ")  # now we have words

    p = run(["column", "-t"], input=txt, capture_output=True, text=True, check=True)
    result = p.stdout.replace("T", " ")  # turns timestamp into two words
    out_file.write_text(result)
    return result


if __name__ == "__main__":
    print(get_bp_table())
