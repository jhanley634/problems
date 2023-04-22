#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# https://codereview.stackexchange.com/questions/284557/mysql-creating-this-table-got-nasty

from pathlib import Path
from typing import Generator
from urllib.parse import urlparse
import datetime as dt
import logging

import pandas as pd
import requests
import sqlalchemy as sa

logging.basicConfig()
logger = logging.getLogger(__name__)


class OriginalClimate:
    """Downloads and reads the original climate data, keeping its messy format."""

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

    def get_urls(self) -> Generator[str, None, None]:
        yield from map(self._url_for, self.FILE_SUFFIXES)

    def _url_for(self, suffix: str) -> str:
        return f"{self.BASE_URL}/{self.FILE_PREFIX}-{suffix}-{self.FILE_VERSION}"

    def _path_for_url(self, url: str) -> Path:
        url_path = urlparse(url).path
        return self.temp / (url_path.split("/")[-1] + ".csv")

    def _fetch(self, url: str) -> Path:
        """Fetches the raw data of the given URL, possibly enjoying a local cache hit."""
        csv = self._path_for_url(url)
        if not csv.exists():
            logger.info(f"Saving {csv}")
            resp = requests.get(url)
            resp.raise_for_status()
            with open(csv, "w") as fout:
                fout.write(resp.text)
        return Path(csv)

    def read_dataset(self, url: str) -> pd.DataFrame:
        names = ["id"] + self.MONTHS
        csv = self._fetch(url)
        df = pd.read_csv(csv, names=names, converters={0: str}, delim_whitespace=True)

        # 1st column is numeric state code (contiguous US, not FIPS)
        # 2nd column is FIPS county code
        pat = r"^(?P<state>\d{2})(?P<county>\d{3})(?P<elt>\d{2})(?P<year>\d{4})$"
        df = df.assign(**df.id.str.extract(pat))

        # data element should be a constant within a given file
        assert min(df.elt) == max(df.elt)

        df = df.drop(columns=["id", "elt"])
        return df

    def download_datasets(self) -> None:
        for url in self.get_urls():
            self.read_dataset(url)  # drags remote data into local cache


if __name__ == "__main__":
    pd.options.display.max_rows = 7
    OriginalClimate().download_datasets()
