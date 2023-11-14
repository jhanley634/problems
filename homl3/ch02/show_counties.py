#! /usr/bin/env streamlit run --server.runOnSave true

# Copyright 2023 John Hanley. MIT licensed.

import pandas as pd
import polars as pl
import streamlit as st

from homl3.ch02.find_nearest import join_on_location


def _get_housing():
    housing_df = pd.DataFrame(join_on_location().drop(columns=["geometry"]))
    assert max(housing_df["pop_density"]) == 50_983
    mem_pandas = housing_df.memory_usage(deep=True).sum()

    housing = pl.from_pandas(housing_df)
    mem_polars = housing.estimated_size()
    print("memory ratio:", round(mem_pandas / mem_polars, 1))  # typ. 2.3
    return housing


def show_counties():
    housing = _get_housing()
    max_density = housing["pop_density"].max()
    housing = housing.with_columns(size=500.0 * housing["pop_density"] / max_density)
    drop_cols = ["median_house_value", "longitude", "latitude"]
    print(housing.drop(columns=drop_cols).describe())
    st.map(
        housing,
        size="size",
    )
    st.write(housing)


if __name__ == "__main__":
    show_counties()
