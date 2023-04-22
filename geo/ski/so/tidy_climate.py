#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# https://codereview.stackexchange.com/questions/284557/mysql-creating-this-table-got-nasty

from pathlib import Path
from typing import Generator
from urllib.parse import urlparse
import datetime as dt
import sys

from typing_extensions import reveal_type
import pandas as pd
import requests
import sqlalchemy as sa


class TidyClimate:
    BASE_URL = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv"
    FILE_PREFIX = "climdiv"
    FILE_SUFFIXES = [
        # "sp01dv",
        # "sp24dv",  # Standardized Precipitation uses "division", not "county"
        "tmaxcy",
        "tmincy",
        "tmpccy",
    ]
    FILE_VERSION = "v1.0.0-20230406"

    MONTHS = [dt.date(2023, i, 1).strftime("%b").lower() for i in range(1, 13)]

    def __init__(self, temp: str = "/tmp/climate"):
        self.temp = Path(temp)
        self.temp.mkdir(exist_ok=True)

    def _get_urls(self) -> Generator[str, None, None]:
        for suffix in self.FILE_SUFFIXES:
            yield self._url_for(suffix)

    def _url_for(self, suffix: str) -> str:
        return f"{self.BASE_URL}/{self.FILE_PREFIX}-{suffix}-{self.FILE_VERSION}"

    def _path_for_url(self, url: str) -> Path:
        url_path = urlparse(url).path
        return self.temp / (url_path.split("/")[-1] + ".csv")

    def _read_url(self, url: str) -> pd.DataFrame:
        csv = self._path_for_url(url)
        df = pd.read_csv(csv, delim_whitespace=True, names=["id"] + self.MONTHS)
        df["state"] = self._get_column(df.id, r"^(\d{2})\d{8}$")
        df["div"] = self._get_column(df.id, r"^\d{2}(\d{2})")
        elt = self._get_column(df.id, r"^\d{4}(\d{2})").astype(int)  # element code
        df["year"] = self._get_column(df.id, r"(\d{4})$").astype(int)
        assert min(elt) == max(elt)  # should be a constant within a given file
        return df

    @staticmethod
    def _get_column(s: pd.Series, regex: str) -> pd.Series:
        return s.astype(str).str.extract(regex)

    def download_dataset(self) -> None:
        for url in self._get_urls():
            csv = self._path_for_url(url)
            if not csv.exists():
                print(f"Saving {csv}")
                resp = requests.get(url)
                resp.raise_for_status()
                with open(csv, "w") as fout:
                    fout.write(resp.text)

            df = self._read_url(url)
            print(df.head())
            sys.exit(0)


if __name__ == "__main__":
    TidyClimate().download_dataset()
