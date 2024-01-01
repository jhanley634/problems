#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
from operator import attrgetter
from pathlib import Path

import gpxpy
import pandas as pd
import polars as pl
import pydeck as pdk
import streamlit as st

from geo.ski.dwell import get_rows


def main() -> None:
    gpx_d = Path("~/Desktop/gpx.d").expanduser()
    paths = sorted(gpx_d.glob("*.gpx"))
    filenames = list(map(str, map(attrgetter("name"), paths)))
    chosen = st.radio("gpx files", filenames)
    _display(_get_df(gpx_d / chosen))


def _get_df(in_file: Path) -> pd.DataFrame:
    with open(in_file) as fin:
        gpx = gpxpy.parse(fin)
        return pd.DataFrame(get_rows(gpx))


def _display(df: pd.DataFrame) -> None:
    print(df.describe())
    print(df.dtypes)
    # Unrecognized type: "Duration" (18)
    df = df.drop(columns=["delta_t"])

    st.pydeck_chart(_get_deck(df))
    st.dataframe(df)




def _get_deck(
    df: pd.DataFrame, start: tuple[float, float] = (37.46, -122.15)
) -> pdk.Deck:
    return pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=start[0],
            longitude=start[1],
            zoom=9,
            pitch=30,
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data=df,
                get_position="[lng, lat]",
                get_elevation=90,
                elevation_scale=1,
                radius=1,
                get_fill_color=[10, 10, "[20 * color]"],
            ),
        ],
    )


if __name__ == "__main__":
    main()
