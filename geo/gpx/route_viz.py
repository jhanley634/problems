#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
from operator import attrgetter
from pathlib import Path

import gpxpy
import pandas as pd
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
        df = pd.DataFrame(get_rows(gpx))
        return df


def _display(df: pd.DataFrame) -> None:
    # Unrecognized type: "Duration" (18)
    df["delta_t"] = df.delta_t.apply(attrgetter("seconds"))

    em = int(round(df.elapsed.max() / 60))
    begin, end = map(int, (em * 0.25, em * 0.75))
    begin, end = st.slider("elapsed_minutes", 0, em, (begin, end))
    # And now back to seconds:
    begin *= 60
    end *= 60
    displayed_df = df[(begin <= df.elapsed) & (df.elapsed <= end)].reset_index()
    st.pydeck_chart(_get_deck(begin, end, df))
    st.dataframe(displayed_df)


def _get_deck(begin, end, df: pd.DataFrame) -> pdk.Deck:
    initial_lat = df.lat.iloc[0]
    initial_lng = df.lng.iloc[0]
    displayed_df = df[(begin <= df.elapsed) & (df.elapsed <= end)].reset_index()
    return pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=initial_lat,
            longitude=initial_lng,
            zoom=14,
            pitch=30,
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data=displayed_df,
                get_position="[lng, lat]",
                get_elevation=4,
                color="purple",
                radius=1,
                get_fill_color=[10, 10, "[20 * color]"],
            ),
        ],
    )


if __name__ == "__main__":
    main()
