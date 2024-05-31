#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Shows recent CR changes.
"""
from collections import namedtuple
from collections.abc import Generator

from tabulate import tabulate
import pandas as pd

from geo.lafco.so.mech_soup.ddg import get_browser

CRResult = namedtuple("CRResult", "title modified")


def scrape(
    site: str = "https://codereview.stackexchange.com/",
) -> Generator[CRResult, None, None]:
    browser = get_browser()
    browser.open(site)

    assert browser.page
    posts = browser.page.find_all("div", class_="s-post-summary--content")
    for post in posts:
        title, mod = "", ""
        for a in post.find_all("a", class_="s-link", href=True):
            if "s-link__muted" not in a["class"]:
                title = a.text
            else:
                mod = a.text
        assert title
        assert mod
        yield CRResult(title, mod)


def report() -> None:
    df = pd.DataFrame(scrape())
    print(tabulate(df.to_records(index=False), maxcolwidths=98))
    # with option_context("display.max_colwidth", 80):


if __name__ == "__main__":
    report()
