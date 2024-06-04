#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import re

import pandas as pd

from geo.lafco.voter.voter_report import clean_column_names

URL = "https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies"


def _get_df(
    url: str = URL,
    focus_country: str = "United States",
) -> pd.DataFrame:
    tables = pd.read_html(url)
    penultimate = -2
    df = clean_column_names(tables[penultimate])
    df = df[df.country_countries.str.contains(focus_country)]
    df = df.rename(columns={"valuation_us_billions": "valuation"})
    df = df.drop(columns=["valuation_date", "country_countries"])
    df["valuation"] = df.valuation.str.replace(r"Undisclosed", "1.2")
    df["valuation"] = df.valuation.str.replace(r"\+$", "", regex=True)
    df["valuation"] = df.valuation.str.replace(r"-\d+$", "", regex=True).astype(float)
    df = df.sort_values(
        ["industry", "valuation", "company"],
        ascending=[True, False, True],
    )
    return df


def unicorn_report(url: str = URL) -> None:
    df = _get_df()
    df.to_csv("/tmp/k/unicorns.csv", index=False)
    with pd.option_context("display.max_rows", None):
        print(df.drop(columns=["founders"])[df.valuation >= 1])


if __name__ == "__main__":
    unicorn_report()
