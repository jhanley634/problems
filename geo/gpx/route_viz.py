#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
from io import BytesIO
from operator import attrgetter
from pathlib import Path
from typing import TYPE_CHECKING

from beartype import beartype
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

from geo.ski.dwell import get_rows


def main() -> None:
    _display(_get_df(_get_chosen_gpx_path()))


def _get_chosen_gpx_path() -> Path:
    gpx_d = Path("~/Desktop/gpx.d").expanduser()
    paths = sorted(gpx_d.glob("*.gpx"))
    filenames = list(map(str, map(attrgetter("name"), paths)))
    chosen = st.radio("gpx files", filenames)
    assert chosen
    return gpx_d / chosen


def _get_df(in_file: Path, ssf_filter: bool = False) -> pd.DataFrame:
    with open(in_file) as fin:
        gpx = gpxpy.parse(fin)
        df = pd.DataFrame(get_rows(gpx))

        if ssf_filter:
            ssf = 37.75
            df = df[df.lat > ssf]
            df["elapsed"] = df.elapsed - df.elapsed.min()

        return df


@beartype
def _display(df: pd.DataFrame, verbose: bool = False) -> None:
    df["delta_t"] = df.delta_t.apply(attrgetter("seconds"))

    elapsed_minutes = df.elapsed.max() / 60
    begin_mn, end_mn = map(int, (elapsed_minutes * 0.25, elapsed_minutes * 0.75))
    begin_mn, end_mn = st.slider(
        "elapsed_minutes", 0, int(elapsed_minutes), (begin_mn, end_mn)
    )
    # nnd switch from minutes back to seconds
    begin = 60 * begin_mn
    end = 60 * end_mn
    st.image(_get_scatter_plot(begin, end, df))
    if verbose:
        st.pydeck_chart(_get_deck(begin, end, df))
        disp = df[(begin <= df.elapsed) & (df.elapsed <= end)].reset_index()
        st.dataframe(disp)


@beartype
@st.cache_data
def _get_scatter_plot(begin: int, end: int, df: pd.DataFrame) -> BytesIO:
    legend = "brief"
    if not TYPE_CHECKING:
        legend = None
    df["hue"] = ((df.elapsed % (5 * 60)) / 60).astype(int)

    disp = _get_scatter_plot_display_df(begin, end, df)

    sns.scatterplot(data=disp, x="lng", y="lat", legend=legend, hue="hue")

    path = Path("/tmp/scatter_plot.png")
    path.unlink(missing_ok=True)
    plt.savefig(path)
    return BytesIO(path.read_bytes())


def _get_scatter_plot_display_df(
    begin: int, end: int, df: pd.DataFrame
) -> pd.DataFrame:
    disp = df[(begin <= df.elapsed) & (df.elapsed <= end)].reset_index()

    # Keep a stable (lat, lng) bbox around the figure, even when filtering on `elapsed`.
    disp = pd.concat(
        [
            disp,
            df.head(1),
            df.tail(1),
            df[df.lat == df.lat.min()],
            df[df.lat == df.lat.max()],
            df[df.lng == df.lng.min()],
            df[df.lng == df.lng.max()],
        ]
    )
    # Visually de-emphasize, by making the four bbox points a light hue.
    disp["hue"] = disp.hue.where(disp.lat > disp.lat.min(), 0)
    disp["hue"] = disp.hue.where(disp.lat < disp.lat.max(), 0)
    disp["hue"] = disp.hue.where(disp.lng > disp.lng.min(), 0)
    disp["hue"] = disp.hue.where(disp.lng < disp.lng.max(), 0)
    return disp


def _get_deck(begin: int, end: int, df: pd.DataFrame) -> pdk.Deck:
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
