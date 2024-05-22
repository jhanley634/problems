#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
#
#
from pathlib import Path

import pandas as pd
import streamlit as st

csv = Path("/tmp/sorted.csv")


def display_houses(in_file=csv):
    st.title("EPASD landowners that signed")
    st.markdown("----")
    df = pd.read_csv(in_file).drop(columns=["date_signed"])
    st.map(df, size=2)
    st.write(df)


if __name__ == "__main__":
    display_houses()
