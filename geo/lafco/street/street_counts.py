#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from collections.abc import Generator
from pprint import pp
import io

import pandas as pd

from geo.gpx.so.word_publisher import get_document


def _get_geocoded_df() -> pd.DataFrame:
    url = (
        "https://raw.githubusercontent.com/jhanley634/dojo-2024-06-18-geocode/main"
        "/geocoding/data/geocoded.csv"
    )
    text = io.StringIO(get_document(url))
    df = pd.read_csv(text)
    cols = "address city st zip housenum  street lat lon".split()
    assert cols == df.columns.tolist(), df.columns
    return df


def _get_streets() -> Generator[str, None, None]:
    for row in _get_geocoded_df().itertuples():
        yield f"{row.street} {row.city}"


def report() -> None:
    c = Counter(_get_streets())
    print(c)
    pp(c.most_common(500))


if __name__ == "__main__":
    report()
