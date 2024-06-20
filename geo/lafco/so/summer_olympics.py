#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
import re

import pandas as pd
import requests


def _get_rows() -> Generator[str, None, None]:
    url = "https://en.wikipedia.org/wiki/Summer_Olympic_Games"
    html = requests.get(url).content
    dfs = pd.read_html(html)
    df = dfs[2]
    assert df.Sport[0] == "3x3 Basketball"

    current_re = re.compile(r"since|all|2024")

    for _, row in df.iterrows():
        if current_re.search(row.Years.lower()):
            yield row.Sport


def sport_names() -> None:
    df = pd.DataFrame(_get_rows())
    print(df)


if __name__ == "__main__":
    sport_names()
