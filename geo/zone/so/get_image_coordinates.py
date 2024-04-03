#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path

from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import requests
import streamlit as st

KITTEN = "https://placekitten.com/200/300"


def main() -> None:
    default = dict(x=0, y=0)  # What we use prior to first click from user.
    d = streamlit_image_coordinates(KITTEN) or default

    x, y = d["x"], d["y"]
    st.write(f"({x}, {y})")


def get_ellipse_coords(
    point: tuple[float, float],
    dx: int = 20,
    dy: int = 10,
) -> tuple[tuple[float, float], tuple[float, float]]:
    x, y = point
    return (x - dx, y - dy), (x + dx, y + dy)


def fetch_image(url: str, cached_fspec: str = "/tmp/kitten.jpg") -> Path:
    fspec = Path(cached_fspec)
    if not fspec.exists():
        resp = requests.get(url)
        resp.raise_for_status()
        with open(fspec, "wb") as fout:
            fout.write(resp.content)
    return fspec


def remember_multiple_points() -> None:
    # https://image-coordinates.streamlit.app/dynamic_update

    with Image.open(fetch_image(KITTEN)) as img:
        draw = ImageDraw.Draw(img)

        if "points" not in st.session_state:
            st.session_state["points"] = set()

        for point in st.session_state["points"]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="red")

        value = streamlit_image_coordinates(img, key="pil")
        if value is not None:
            point = value["x"], value["y"]
            if point not in st.session_state["points"]:
                st.session_state["points"].add(point)
                st.experimental_rerun()


if __name__ == "__main__":
    remember_multiple_points()
