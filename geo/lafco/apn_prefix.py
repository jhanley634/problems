#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Datasource is CSV exports from https://gis.smcgov.org/Html5Viewer/?viewer=raster
"""
import pandas as pd

from geo.lafco.lafco_util import LAFCO_DIR, clean_column_names


def _with_dashes(apn: str) -> str:
    """
    >>> _with_dashes("063492490")
    '063-492-490'
    """
    assert apn.startswith("063"), apn
    assert 9 == len(apn), apn
    return f"{apn[:3]}-{apn[3:6]}-{apn[6:]}"


def get_apn_prefix_df(pfx: str = "063-4") -> pd.DataFrame:
    df = pd.read_csv(LAFCO_DIR / f"apn-prefix-{pfx}.csv", dtype=str)
    df = clean_column_names(df).drop(columns=["geometry"])
    df["apn"] = df.apn.map(_with_dashes)
    df = df[~df.situs_addr.str.fullmatch(" , ")]  # discards 3 empty situs_city values
    df = df[~df.situs_addr.str.startswith(" ")]  # discards 16 empty address values
    assert 680 == len(df), df

    for i, row in df.iterrows():
        assert row.situs_addr.endswith(row.situs_city)
        assert row.uninc == "Incorporated"

    return df.drop(columns=["situs_city", "uninc"])


if __name__ == "__main__":
    print(get_apn_prefix_df())
