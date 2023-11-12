#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from typing import Any

from beartype import beartype
from geopandas.array import GeometryArray
from uszipcode import SearchEngine, SimpleZipcode
import geopandas as gpd
import numpy as np
import pandas as pd
import requests

AGERON_BASE_URL = "https://raw.githubusercontent.com/ageron/data/main"  # homl3 files

CACHE_DIR = Path("/tmp/cache")


@beartype
def get_cached(url: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / Path(url).name
    if not cache_file.exists():
        resp = requests.get(url)
        resp.raise_for_status()
        cache_file.write_bytes(resp.content)

    return cache_file


@beartype
def get_housing_df(filename="housing/housing.csv") -> pd.DataFrame:
    """Retrieves simplified 1990 housing data."""
    url = f"{AGERON_BASE_URL}/{filename}"
    cache_file = get_cached(url)
    assert cache_file.stat().st_size == 1_423_529

    df = pd.read_csv(cache_file)
    assert len(df) == 20_640
    assert len(df.columns) == 10

    return df[["longitude", "latitude", "median_house_value"]]


@beartype
def _california_city_columns(row: SimpleZipcode) -> dict[str, Any]:
    assert row.state == "CA"
    return {
        "lng": row.lng,
        "lat": row.lat,
        "population": row.population,
        "pop_density": row.population_density,
        "city": row.major_city,
    }


@beartype
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


@beartype
def _points_from_xy(lng: pd.Series, lat: pd.Series, eps=1e-9) -> GeometryArray:
    assert len(lng) == len(lat)
    size = len(lng)
    return gpd.points_from_xy(
        lng + np.random.uniform(-eps, eps, size=size),
        lat + np.random.uniform(-eps, eps, size=size),
    )


@beartype
def join_on_location() -> gpd.GeoDataFrame:
    housing = gpd.GeoDataFrame(
        df := get_housing_df(),
        geometry=_points_from_xy(df.longitude, df.latitude),
    )
    cities = gpd.GeoDataFrame(
        df := get_cities(),
        geometry=_points_from_xy(df.lng, df.lat),
    )
    both = gpd.sjoin_nearest(housing, cities, how="left", distance_col="dist")
    both = both.drop(columns=["longitude", "latitude", "lng", "lat", "index_right"])
    # assert 21_286 == len(both), len(both)
    assert 20_640 == len(both), len(both)
    return both


if __name__ == "__main__":
    print(join_on_location())
