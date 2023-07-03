#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
import re

from polars import Utf8
import pandas as pd
import polars as pl
import streamlit as st

DESKTOP = Path("~/Desktop").expanduser()


# https://www.hcd.ca.gov/planning-and-community-development/accountability-and-enforcement
# https://www.hcd.ca.gov/sites/default/files/docs/planning-and-community/enforcement-letters-issued.xlsx
def read_sheet(
    infile: Path = DESKTOP / "enforcement-letters-issued.xlsx",
) -> pl.DataFrame:
    df = pl.from_dataframe(pd.read_excel(infile, skiprows=1))
    df = _rename_columns(df)
    df = df.with_columns(df["hcd_letter_type"].apply(_clean_letter_type))
    df = df.with_columns([_cast_if_boolean(df[col]) for col in df.columns])
    return df


def _clean_letter_type(type_: str) -> str:
    type_re = re.compile(r" Letter$")
    return type_re.sub("", type_.strip())


def _cast_if_boolean(series: pl.Series) -> pl.Series:
    if set(series.unique()) == {None, "x"}:
        assert series.dtype == Utf8
        series = series.map_dict({"x": True, None: False})
        return series.cast(pl.Boolean)
    return series


def _rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.rename(dict(zip(df.columns, map(_rename_column, df.columns))))


def _rename_column(name: str) -> str:
    name = " ".join(name.split())
    name = name.replace(" / Agency", "")
    name = name.replace(" Response", "")
    name = name.replace("State ", "")
    name = name.replace("Accountability", "Acct")
    name = name.replace("Housing", "H")
    name = name.replace(" ", "_")
    return name.lower()


def summarize_letter_types(df: pl.DataFrame, thresh_count: int = 1) -> pl.DataFrame:
    keys = ["count", "hcd_letter_type"]
    df_ltr_typ = df.groupby("hcd_letter_type").count().sort(by=keys, descending=True)
    df_ltr_typ = df_ltr_typ.filter(pl.col("count") > thresh_count)
    return df_ltr_typ


def main() -> None:
    df = read_sheet()
    print(df.drop("hcd_letter_date").to_pandas().describe())
    # print(df.to_pandas().info())  # gives dtype, and a non-null count for each column
    st.write(df.to_pandas())

    st.dataframe(summarize_letter_types(df), hide_index=True)


if __name__ == "__main__":
    main()
