#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path

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
    return df[["longitude", "latitude", "median_house_value"]]


if __name__ == "__main__":
    print(get_housing_df().head())
