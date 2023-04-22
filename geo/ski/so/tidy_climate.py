#! /usr/bin/env SQLALCHEMY_WARN_20=1 python

# Copyright 2023 John Hanley. MIT licensed.
# https://codereview.stackexchange.com/questions/284557/mysql-creating-this-table-got-nasty

from pathlib import Path
from typing import Any, Generator
from urllib.parse import urlparse
import datetime as dt
import logging

import pandas as pd
import requests
import sqlalchemy as sa


class OriginalClimate:
    """Downloads and reads the original climate data, keeping its messy format."""

    BASE_URL = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv"
    FILE_PREFIX = "climdiv"
    DATA_ELEMENTS = [
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
        self.log = logging.getLogger(self.__class__.__name__)

    def get_urls(self) -> Generator[str, None, None]:
        yield from map(self.url_for, self.DATA_ELEMENTS)

    def url_for(self, suffix: str) -> str:
        return f"{self.BASE_URL}/{self.FILE_PREFIX}-{suffix}-{self.FILE_VERSION}"

    def _path_for_url(self, url: str) -> Path:
        url_path = urlparse(url).path
        return self.temp / (url_path.split("/")[-1] + ".csv")

    def _fetch(self, url: str) -> Path:
        """Fetches the raw data of the given URL, possibly enjoying a local cache hit."""
        csv = self._path_for_url(url)
        if not csv.exists():
            self.log.info(f"Saving {csv}")
            resp = requests.get(url)
            resp.raise_for_status()
            with open(csv, "w") as fout:
                fout.write(resp.text)
        return Path(csv)

    def read_dataset(self, url: str) -> pd.DataFrame:
        names = ["id"] + self.MONTHS
        preserve = {0: str}  # ID starts with state code; preserve leading "0".
        csv = self._fetch(url)  # Neither a .CSV nor a .TSV, but close enough.
        df = pd.read_csv(csv, names=names, converters=preserve, delim_whitespace=True)

        # 1st column is numeric state code (contiguous US, not FIPS)
        # 2nd column is FIPS county code
        pat = r"^(?P<state>\d{2})(?P<county>\d{3})(?P<elt>\d{2})(?P<year>\d{4})$"
        df = df.assign(**df.id.str.extract(pat))

        # data element should be a constant within a given file
        assert min(df.elt) == max(df.elt)

        df = df.drop(columns=["id", "elt"])
        df["year"] = df["year"].astype(int)
        return df

    def download_datasets(self) -> Generator[str, None, None]:
        for url in self.get_urls():
            self.read_dataset(url)  # drags remote data into local cache
            yield url


def read_tidy_dataset(oc: OriginalClimate, col_name: str) -> pd.DataFrame:
    messy = oc.read_dataset(oc.url_for(col_name))
    tidy = pd.DataFrame(_get_monthly_rows(messy, col_name))
    return tidy


def _get_monthly_rows(
    df: pd.DataFrame,
    col_name: str,
) -> Generator[dict[str, Any], None, None]:
    for _, row in df.iterrows():
        place = dict(state=row.state, county=row.county)
        for month_num, month in enumerate(OriginalClimate.MONTHS):
            yield {
                **place,
                "stamp": dt.datetime(row.year, 1 + month_num, 1),
                col_name: row[month],
            }
        return


class TidyClimate:
    """Maintains tidy versions of climate datasets in DB tables."""

    TEMP_DIR = OriginalClimate().temp
    DB_PATH = TEMP_DIR / "climate.db"

    def __init__(self, db_url: str = f"sqlite:///{DB_PATH}"):
        self.engine = sa.create_engine(db_url)
        self.metadata = sa.MetaData()
        self.oc = OriginalClimate()

    def populate_tables(self) -> None:
        con = self.engine.connect()
        con.begin()
        for elt in self.oc.DATA_ELEMENTS:
            con.execute(sa.text(f"DROP TABLE  IF EXISTS  {elt}"))
            con.execute(self._get_create(elt))

            df: pd.DataFrame = read_tidy_dataset(self.oc, elt)
            df.to_sql(elt, self.engine, index=False, if_exists="append")

    @staticmethod
    def _get_create(elt: str) -> sa.text:
        """Arrange for a compound primary key."""
        return sa.text(
            f"""
            CREATE TABLE {elt} (
                state TEXT,
                county TEXT,
                stamp DATETIME,
                {elt} FLOAT,
                PRIMARY KEY (state, county, stamp)
            )
        """
        )


if __name__ == "__main__":
    pd.options.display.max_rows = 7
    logging.basicConfig(level=logging.INFO)

    TidyClimate().populate_tables()
