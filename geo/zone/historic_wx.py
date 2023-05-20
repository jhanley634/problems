#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import datetime as dt

import polars as pl
import requests
import typer


def get_wx_stats(date: dt.date) -> pl.DataFrame:
    """Obtains daily weather data from Wunderground."""
    url = "https://api.weather.com/v1/location/KSJC:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate=20220201&endDate=20220228"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    _verify_metadata(data["metadata"])
    return pl.DataFrame(data["observations"])


def _verify_metadata(meta: dict[str, str]) -> None:
    assert meta["language"] == "en-US"
    assert meta["version"] == "1"
    assert meta["units"] == "e"
    assert meta["location_id"] == "KSJC:9:US"


def main(start_day: dt.datetime) -> None:
    start_date = start_day.date()
    print(get_wx_stats(start_date))


if __name__ == "__main__":
    typer.run(main)
