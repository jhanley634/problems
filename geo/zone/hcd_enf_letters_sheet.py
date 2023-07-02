#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path

import pandas as pd
import polars as pl
import streamlit as st

DESKTOP = Path("~/Desktop").expanduser()


def read_sheet(
    infile: Path = DESKTOP / "enforcement-letters-issued.xlsx",
) -> pl.DataFrame:
    df = pl.from_dataframe(pd.read_excel(infile, skiprows=1))
    df = df.with_columns(
        [df[col].map_dict({"x": "x", None: ""}) for col in df.columns if "x" in df[col]]
    )
    return _rename_columns(df)


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


def main() -> None:
    df = read_sheet()
    print(df.drop("hcd_letter_date").to_pandas().describe())
    # print(df.to_pandas().info())  # gives dtype, and a non-null count for each column
    st.write(df.to_pandas())


if __name__ == "__main__":
    main()
