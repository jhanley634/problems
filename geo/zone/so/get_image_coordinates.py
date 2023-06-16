#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2023 John Hanley. MIT licensed.
from streamlit_image_coordinates import streamlit_image_coordinates
import streamlit as st


def main():
    default = dict(x=0, y=0)  # What we use prior to first click from user.
    d = streamlit_image_coordinates("https://placekitten.com/200/300") or default

    x, y = d["x"], d["y"]
    st.write(f"({x}, {y})")


if __name__ == "__main__":
    main()
