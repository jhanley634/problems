#! /usr/bin/env streamlit run --server.runOnSave true

# Copyright 2023 John Hanley. MIT licensed.
import streamlit as st

from geo.ski.dwell import GPX_DIR


def main():
    st.title("available files:")
    files = sorted(GPX_DIR.glob("*.gpx"))
    st.write("\n\n".join(map(str, files)))


if __name__ == "__main__":
    main()
