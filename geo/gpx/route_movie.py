#! /usr/bin/env python
#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path
from typing import Generator
import datetime as dt

from geopy import Point
from gpxpy.gpx import GPX
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    in_file = Path("~/Desktop/gpx.d/2023-12-07T22:20:02Z-willows-walk.gpx").expanduser()

    df = _get_df(in_file)
    print(df)
    _display(df)


def _display(df: pd.DataFrame) -> None:
    sns.scatterplot(data=df, x="lat", y="lng")
    plt.show()


def _get_df(in_file: Path) -> pd.DataFrame:
    return pd.DataFrame(_get_fn_points())


def _get_fn_points() -> Generator[Point, None, None]:
    def fn(lat):
        return 0.01 * lat**2

    for lat in range(-100, 100):
        yield dict(lat=lat, lng=fn(lat))


def _get_gpx_points(in_file: Path) -> Generator[Point, None, None]:
    # Similar to _get_breadcrumbs()
    with open(in_file) as fin:
        gpx: GPX = gpxpy.parse(fin)
        for row in gpx.tracks:
            for segment in row.segments:
                for pt in segment.points:
                    stamp: dt.datetime = pt.time
                    stamp = stamp.replace(tzinfo=None).astimezone(dt.timezone.utc)
                    yield dict(
                        stamp=stamp,
                        lat=round(pt.latitude, 6),
                        lng=round(pt.longitude, 6),
                        elevation=round(pt.elevation, 2),
                    )


if __name__ == "__main__":
    main()
