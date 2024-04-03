#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.

from io import BytesIO
from pathlib import Path
from typing import Any, Generator
import datetime as dt

from gpxpy.gpx import GPX
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


def main() -> None:
    in_file = Path("~/Desktop/gpx.d/2023-12-07T22:20:02Z-willows-walk.gpx").expanduser()

    df = _get_df(in_file)
    _display(df)


def _display(df: pd.DataFrame) -> None:
    st.image(_scatterplot(df))


def _scatterplot(df: pd.DataFrame) -> BytesIO:
    sns.scatterplot(data=df, x="lat", y="lng")

    path = Path("/tmp/scatter_plot.png")
    path.unlink(missing_ok=True)
    plt.savefig(path)
    return BytesIO(path.read_bytes())


def _get_df(in_file: Path) -> pd.DataFrame:
    assert in_file.exists()
    return pd.DataFrame(_get_fn_points())


def _get_fn_points() -> Generator[dict[str, float], None, None]:
    def fn(x: float) -> float:
        return 0.01 * x**2

    for lat in range(-100, 100):
        yield dict(lat=lat, lng=fn(lat))


def _get_gpx_points(in_file: Path) -> Generator[dict[str, Any], None, None]:
    # Similar to _get_breadcrumbs()
    with open(in_file) as fin:
        gpx: GPX = gpxpy.parse(fin)
        for row in gpx.tracks:
            for segment in row.segments:
                for pt in segment.points:
                    assert pt.time
                    stamp: dt.datetime = pt.time
                    stamp = stamp.replace(tzinfo=None).astimezone(dt.timezone.utc)
                    assert pt.elevation
                    assert pt.elevation > 0, pt.elevation
                    yield dict(
                        stamp=stamp,
                        lat=round(pt.latitude, 6),
                        lng=round(pt.longitude, 6),
                        elevation=round(pt.elevation, 2),
                    )


if __name__ == "__main__":
    main()
