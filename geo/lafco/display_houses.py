#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path

from pandas import Series
from typing_extensions import Any
import numpy as np
import pandas as pd
import streamlit as st

from geo.lafco.geocode import Geocoder

csv = Path("~/Desktop/lafco/2024-05-21 qry EPASD APNs Landowner Protests.csv")


def display_houses(in_file: Path = csv) -> None:
    st.title("EPASD landowners that signed")
    st.markdown("----")
    in_file = in_file.expanduser()
    df = pd.read_csv(in_file)
    df = df.dropna(subset=["EPA Address"])
    df[["lat", "lon", "dot_size", "color"]] = df.apply(
        _get_point, axis=1, result_type="expand"
    )
    df = df.dropna(subset=["lat"])
    df["dot_size"] = df.dot_size.astype(int)
    st.map(df, size="dot_size", color="color")
    st.write(df)


good_cities = {
    "E PALO ALTO",
    "EAST PALO ALTO",
    "MENLO PARK",
}
WILLOW_RD_LON = -122.1577

geocoder = Geocoder()

BLACK = (0, 0, 0, 0)
RED = (255, 0, 0, 50)
GREEN = (0, 255, 0, 255)
# PURPLE = (128, 0, 128, 255)


def _get_point(
    row: "Series[Any]",
) -> tuple[float, float, int, tuple[int, int, int, int]]:
    mail_city = row["Mail City"]
    if mail_city not in good_cities:
        return np.NaN, np.NaN, 0, BLACK
    city = mail_city if mail_city in good_cities else "EAST PALO ALTO"
    addr = f'{row["EPA Address"]}, {city} CA'
    loc = geocoder.get_location(addr)
    if addr == "480 OKEEFE ST, MENLO PARK CA":
        return np.NaN, np.NaN, 0, BLACK
    if loc.lon < WILLOW_RD_LON:
        return np.NaN, np.NaN, 0, BLACK
    dot_size = 4 if row["Signed Protest Form?"] else 1
    color = GREEN if row["Signed Protest Form?"] else RED
    return loc.lat, loc.lon, dot_size, color


if __name__ == "__main__":
    display_houses()
