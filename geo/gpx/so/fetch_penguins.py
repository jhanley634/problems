#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path
import datetime as dt
import re

import pandas as pd
import requests_cache

PENGUIN_URL = (
    "https://raw.githubusercontent.com/allisonhorst"
    "/esm-206-2018/master/week_6/penguins.csv"
)


def fetch_df(url: str) -> pd.DataFrame:
    cache_dir = Path("/tmp")
    cache_dir.mkdir(exist_ok=True)
    expire = dt.timedelta(days=1)
    requests_cache.install_cache(f"{cache_dir}/requests_cache", expire_after=expire)
    requests_cache.delete(expired=True)
    return pd.read_csv(url)


def fetch_penguin_df() -> pd.DataFrame:
    df = fetch_df(PENGUIN_URL)

    # Drop index, three categorical columns, and unused measurements.
    cols = "sample_number sex region study_name culmen_length flipper_length"
    df = df.drop(columns=cols.split())

    species_re = re.compile(r"^(\w+) penguin .*", re.IGNORECASE)
    df["species"] = df.species.apply(lambda s: species_re.sub(r"\1", s))
    assert 3 == df.species.nunique()
    assert 344 == len(df)

    df = df.sample(frac=1).reset_index(drop=True)  # shuffle the rows
    # Adelie & Chinstrap are indistinguishably mixed at this point.

    df["is_gentoo"] = df.species == "Gentoo"
    df = df.drop(columns="species")

    return df
