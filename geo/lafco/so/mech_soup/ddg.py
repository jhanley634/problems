#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Obtains Mechanical Soup resources from a popular search engine.
"""
from collections import namedtuple
from collections.abc import Generator

from bs4.element import Tag
from mechanicalsoup import StatefulBrowser
import pandas as pd

Result = namedtuple("Result", "url title")


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"


def get_browser() -> StatefulBrowser:
    return StatefulBrowser(user_agent=UA, raise_on_404=True)


def search(
    query: str = "mechanical soup",
    engine: str = "https://lite.duckduckgo.com/lite/",
) -> Generator[Result, None, None]:
    browser = get_browser()
    browser.open(engine)
    assert browser.url == engine
    browser.select_form()
    assert isinstance(browser.get_current_form().form, Tag)
    browser.form.set_input({"q": query})
    browser.submit_selected()

    tables = browser.page.find_all("table")
    table = tables[2]
    for a in table.find_all("a", class_="result-link", href=True):
        yield Result(a["href"], a.text)


def report() -> None:
    df = pd.DataFrame(search("mechanical soup"))
    print(df)


if __name__ == "__main__":
    report()
