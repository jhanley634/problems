#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python

# Copyright 2023 John Hanley. MIT licensed.
import datetime as dt

import polars as pl
import requests
import typer


def get_wx_stats(date: dt.date, station: str = "KSJC:9:US") -> pl.DataFrame:
    """Obtains daily weather data from Wunderground."""
    api_key = "e1f10a1e78da46f5b10a1e78da96f525"
    url = f"https://api.weather.com/v1/location/{station}/observations/historical.json?apiKey={api_key}&units=e&startDate=20220201&endDate=20220228"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    _verify_metadata(data["metadata"])
    return _filter_columns(pl.DataFrame(data["observations"]))


def _verify_metadata(meta: dict[str, str]) -> None:
    assert meta["language"] == "en-US"
    assert meta["version"] == "1"
    assert meta["units"] == "e"
    assert meta["location_id"] == "KSJC:9:US"


def _filter_columns(df: pl.DataFrame) -> pl.DataFrame:
    assert (df["class"] == "observation").all()
    drops = [
        "class",  # constant across all stations
        "obs_id",  # constant station identifier, e.g. KSJC
        "obs_name",  # constant station name, e.g. San Jose
        "day_ind",  # "N" -> night, "D" -> day
        "wx_icon",
        "icon_extd",
        "heat_index",
        "pressure_tend",  # 0..2 inclusive
        "pressure_desc",  # one of ['Falling', 'Falling Rapidly', 'Rising', 'Rising Rapidly', 'Steady']
        "wc",  # wind chill
        "wdir_cardinal",  # e.g. "NNW", "VAR" or "CALM"
        "wdir",  # wind direction, in degrees, congruent to zero mod ten
        "gust",
        "uv_index",  # 0..5 inclusive
        "uv_desc",  # e.g. "Low", "Moderate"
        "feels_like",  # perceived temperature
        "clds",  # cloud cover, one of ['BKN', 'CLR', 'FEW', 'OVC', 'SCT']
        "precip_total",
    ]
    df = df.drop(drops)

    for col_name in ["expire_time_gmt", "valid_time_gmt"]:
        df = df.with_columns(
            (pl.col(col_name) * 1e3).cast(pl.Datetime).dt.with_time_unit("ms")
        )

    return _discard_uninformative_columns(df)


def _discard_uninformative_columns(df: pl.DataFrame) -> pl.DataFrame:
    # Remove columns containing just null values.
    counts = df.null_count().rows()[0]
    useless_cols = [k for k, v in zip(df.columns, counts) if v == len(df)]
    return df.drop(useless_cols)


def main(start_day: dt.datetime) -> None:
    start_date = start_day.date()
    df = get_wx_stats(start_date)

    pl.Config.set_tbl_cols(50)
    pl.Config.set_tbl_rows(100)
    print(df)


if __name__ == "__main__":
    typer.run(main)
