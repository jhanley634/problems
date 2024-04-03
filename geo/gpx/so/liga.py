#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# from https://stackoverflow.com/questions/77949670/scraping-data-using-python-and-requests-and-export-in-excel-file

from typing import Generator

from beartype import beartype
from requests_html import HTMLResponse, HTMLSession
import pandas as pd

matchlink = "https://www.betexplorer.com/football/serbia/prva-liga/results/"


@beartype
def _get_rows(url: str) -> Generator[dict[str, str], None, None]:
    session = HTMLSession()

    r = session.get(matchlink)
    assert isinstance(r, HTMLResponse)

    allmatch = r.html.find(".in-match")
    results = r.html.find(".h-text-center a")
    # search for elements containing "data-odd" attribute
    matchodds = r.html.find("[data-odd]")

    odds = [matchodd.attrs["data-odd"] for matchodd in matchodds]

    idx = 0
    for match, res in zip(allmatch, results):
        if res.text == "POSTP.":
            continue

        print(f"{match.text} Z {res.text} {', '.join(odds[idx:idx+3])}")
        yield {
            "match": match.text,
            "result": res.text,
            "odds": ", ".join(odds[idx : idx + 3]),
        }

        idx += 3


if __name__ == "__main__":
    df = pd.DataFrame(_get_rows(matchlink)).set_index("match")
    print(df)
