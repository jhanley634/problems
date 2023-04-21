#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# https://codereview.stackexchange.com/questions/284557/mysql-creating-this-table-got-nasty

from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

from typing_extensions import reveal_type
import pandas as pd
import requests
import sqlalchemy as sa


class TidyClimate:
    BASE_URL = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv"
    FILE_PREFIX = "climdiv"
    FILE_SUFFIXES = [
        "sp01dv",
        "sp24dv",
        "tmaxcy",
        "tmincy",
        "tmpccy",
    ]
    FILE_VERSION = "v1.0.0-20230406"

    def __init__(self, temp: str = "/tmp/climate"):
        self.temp = Path(temp)
        self.temp.mkdir(exist_ok=True)

    def _get_urls(self) -> Generator[str, None, None]:
        for suffix in self.FILE_SUFFIXES:
            yield self._url_for(suffix)

    def _url_for(self, suffix: str) -> str:
        return f"{self.BASE_URL}/{self.FILE_PREFIX}-{suffix}-{self.FILE_VERSION}.csv"

    def _path_for_url(self, url: str) -> Path:
        url_path = urlparse(url).path
        return self.temp / url_path.split("/")[-1]

    def download_dataset(self) -> None:
        for url in self._get_urls():
            csv = self._path_for_url(url)
            if not csv.exists():
                print(f"Downloading {url} to {csv}")
                resp = requests.get(url)
                resp.raise_for_status()
                with open(csv, "w") as fout:
                    fout.write(resp.text)
                df = pd.read_csv(csv)
                print(df.head(3))

if __name__ == '__main__':
    TidyClimate().download_dataset()
