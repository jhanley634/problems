#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from typing import Any

from uszipcode import SearchEngine, SimpleZipcode
import geopandas as gpd
import pandas as pd
import requests

AGERON_BASE_URL = "https://raw.githubusercontent.com/ageron/data/main"  # homl3 files

CACHE_DIR = Path("/tmp/cache")


def get_cached(url: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / Path(url).name
    if not cache_file.exists():
        resp = requests.get(url)
        resp.raise_for_status()
        cache_file.write_bytes(resp.content)

    return cache_file


def get_housing_df(filename="housing/housing.csv") -> pd.DataFrame:
    """Retrieves simplified 1990 housing data."""
    url = f"{AGERON_BASE_URL}/{filename}"
    cache_file = get_cached(url)
    assert cache_file.stat().st_size == 1_423_529

    df = pd.read_csv(cache_file)
    assert len(df) == 20_640
    assert len(df.columns) == 10

    return df[["longitude", "latitude", "median_house_value"]]


def _california_city_columns(row: SimpleZipcode) -> dict[str, Any]:
    assert row.state == "CA"
    return {
        "longitude": row.lng,
        "latitude": row.lat,
        "population": row.population,
        "pop_density": row.population_density,
        "city": row.major_city,
    }


def get_cities(limit=1600) -> pd.DataFrame:
    zip_se = SearchEngine()
    return pd.DataFrame(
        map(
            _california_city_columns,
            filter(
                lambda row: (row.population or -1) > 0,
                zip_se.by_state(
                    "CA",
                    sort_by=SimpleZipcode.population_density,
                    ascending=False,
                    returns=limit,
                ),
            ),
        )
    )


def main() -> None:
    cities = gpd.GeoDataFrame(
        df := get_cities(),
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
    )
    housing = gpd.GeoDataFrame(
        df := get_housing_df(),
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
    )
    both = gpd.sjoin_nearest(cities, housing, how="left", distance_col="dist")
    both = both.drop(columns=["longitude_left", "latitude_left"])
    print(both)
    assert len(both) == 2433


if __name__ == "__main__":
    main()
