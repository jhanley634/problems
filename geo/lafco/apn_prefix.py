#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Datasource is CSV exports from https://gis.smcgov.org/Html5Viewer/?viewer=raster
"""
import pandas as pd

from geo.lafco.lafco_util import LAFCO_DIR, _with_dashes, clean_column_names

nearby_cities = {
    "EAST PALO ALTO",
    "FOSTER CITY",
    "MENLO PARK",
    "REDWOOD CITY",
    "SAN CARLOS",
}


def get_apn_prefix_df(pfx: str = "063-4") -> pd.DataFrame:
    df = pd.read_csv(LAFCO_DIR / f"prefix/apn-prefix-{pfx}.csv", dtype=str)
    df = clean_column_names(df)
    df["apn"] = df.apn.map(_with_dashes)
    df = df[~df.situs_addr.str.fullmatch(" , ")]  # discards 3 empty situs_city values
    df = df[~df.situs_addr.str.startswith(" ")]  # discards 16 empty address values

    print(df.situs_city.value_counts())

    for _, row in df.iterrows():
        assert row.situs_city in nearby_cities, row
        assert row.situs_addr.endswith(row.situs_city)
        assert row.uninc in ("Incorporated", "Unincorporated"), row

    return df.drop(columns=["geometry", "situs_city", "uninc"])


if __name__ == "__main__":
    df = get_apn_prefix_df("all")
    assert 5825 == len(df), len(df)
    print(df)
