#! /usr/bin/env streamlit run --server.runOnSave true

# Copyright 2023 John Hanley. MIT licensed.

from functools import lru_cache
from hashlib import sha3_224

import pandas as pd
import polars as pl
import streamlit as st

from homl3.ch02.find_nearest import join_on_location


def _get_housing() -> pl.DataFrame:
    housing_df = pd.DataFrame(join_on_location().drop(columns=["geometry"]))
    assert max(housing_df["pop_density"]) == 50_983
    mem_pandas = housing_df.memory_usage(deep=True).sum()

    housing = pl.from_pandas(housing_df)
    mem_polars = housing.estimated_size()
    print("memory ratio:", round(mem_pandas / mem_polars, 1))  # typ. 2.3
    return housing


@lru_cache
def _color_of(county: str, alpha=0.2) -> tuple[float, float, float, float]:
    """Returns an RGBA color, including alpha transparency."""
    return (
        _hash("R", county),
        _hash("G", county),
        _hash("B", county),
        alpha,
    )


@lru_cache
def _hash(color: str, county: str) -> float:
    """Used for mapping a county to a fixed, arbitrary color."""
    text = bytes(f"{color}{county}", "utf-8")
    digest_byte: int = sha3_224(text).digest()[0]
    return digest_byte / 256.0


def show_counties() -> None:
    housing = _get_housing().to_pandas()  # Turns out we need pandas, for color support.
    housing["color"] = housing["county"].apply(_color_of)
    housing["size"] = 5.0 * housing.pop_density / housing.pop_density.max()
    drop_cols = ["median_house_value", "longitude", "latitude"]
    print(housing.drop(columns=drop_cols).describe())
    st.map(
        housing,
        color="color",
        size="size",
    )
    st.write(housing)


if __name__ == "__main__":
    show_counties()
