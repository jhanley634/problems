#! /usr/bin/env streamlit run --server.runOnSave true

# Copyright 2023 John Hanley. MIT licensed.

import pandas as pd
import polars as pl
import streamlit as st

from homl3.ch02.find_nearest import join_on_location


def show_counties():
    housing = pd.DataFrame(join_on_location().drop(columns=["geometry"]))
    mem_pandas = housing.memory_usage(deep=True).sum()

    housing = pl.from_pandas(housing)
    mem_polars = housing.estimated_size()
    print("memory ratio:", round(mem_pandas / mem_polars, 2))
    st.write(housing)


if __name__ == "__main__":
    show_counties()
