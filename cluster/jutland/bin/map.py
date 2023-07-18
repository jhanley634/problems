#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
from palettable.colorbrewer import qualitative
import pandas as pd
import pydeck as pdk
import streamlit as st

from cluster.jutland.dataset import Dataset


@st.cache
def _get_points(only_show_favorites: bool = False) -> pd.DataFrame:
    df = Dataset.get_df()

    # These are simply the first couple, in sorted order.
    favorite_roads = {
        144552912,  # Svingelbjerg
        93323205,  # Vidstrup
    }
    if only_show_favorites:
        df = df[df.osm_id.isin(favorite_roads)]

    colors = qualitative.Paired_12.colors
    df["road_hash"] = pd.util.hash_array(df.osm_id.apply(str)) % len(colors)

    # In https://discuss.streamlit.io/t/tooltip-and-labels-in-pydeck-chart/1727
    # godot63 suggests we may need an annoying 3 (r,g,b) color columns.
    df["color"] = df.road_hash

    return df


AALBORG = (57.050, 9.917)


def column_layer(df: pd.DataFrame) -> None:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=AALBORG[0],
                longitude=AALBORG[1],
                zoom=9,
                pitch=30,
            ),
            layers=[
                pdk.Layer(
                    "ColumnLayer",
                    data=df,
                    get_position="[lon, lat]",
                    get_elevation=90,
                    elevation_scale=1,
                    radius=20,
                    get_fill_color=[10, 10, "[20 * color]"],
                ),
            ],
        )
    )


if __name__ == "__main__":
    st.markdown("# DK roads")
    st.map(_get_points())
    column_layer(_get_points())

    st.dataframe(_get_points())
