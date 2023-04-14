#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path
from typing import Any, Generator

from gpxpy.gpx import GPXTrackSegment
import gpxpy
import pandas as pd
import pydeck as pdk
import streamlit as st


def _expect(expected: Any, actual: Any) -> None:
    assert expected == actual, actual


def _get_df(in_file: str = "/tmp/10-Jul-2022-1714.gpx") -> pd.DataFrame:
    in_file_ = Path(in_file).expanduser()
    with open(in_file_) as fin:
        gpx = gpxpy.parse(fin)
        _expect(1, len(gpx.tracks))
        _expect(1, len(gpx.tracks[0].segments))
        return pd.DataFrame(_get_points(gpx.tracks[0].segments[0]))


def _get_points(segment: GPXTrackSegment) -> Generator[dict[str, Any], None, None]:
    for pt in segment.points:
        yield dict(
            time=pt.time, lat=pt.latitude, lon=pt.longitude, elevation=pt.elevation
        )


def _get_deck(start: tuple[float, float] = (37.46, -122.15)) -> pdk.Deck:
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
                data=_get_df(),
                get_position="[lon, lat]",
                get_elevation=90,
                elevation_scale=1,
                radius=20,
                get_fill_color=[10, 10, "[20 * color]"],
            ),
        ],
    )


if __name__ == "__main__":
    st.markdown("# route")
    st.pydeck_chart(_get_deck())
    st.write(_get_df())
