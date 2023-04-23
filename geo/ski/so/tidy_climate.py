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
import sqlalchemy.orm as orm

TEMP_DIR = Path("/tmp/climate")  # We store things like cached CSV's here.
DB_URL = f"sqlite:///{TEMP_DIR / 'climate.db'}"


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

    def __init__(self, temp_dir: Path = TEMP_DIR):
        self.folder = temp_dir
        self.folder.mkdir(exist_ok=True)
        self.log = logging.getLogger(self.__class__.__name__)

    def get_urls(self) -> Generator[str, None, None]:
        yield from map(self.url_for, self.DATA_ELEMENTS)

    def url_for(self, suffix: str) -> str:
        return f"{self.BASE_URL}/{self.FILE_PREFIX}-{suffix}-{self.FILE_VERSION}"

    def _path_for_url(self, url: str) -> Path:
        url_path = urlparse(url).path
        return self.folder / (url_path.split("/")[-1] + ".csv")

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


class TidyClimate:
    """Maintains tidy versions of climate datasets in DB tables."""

    def __init__(self, db_url: str = DB_URL):
        self.engine = sa.create_engine(db_url)
        self.oc = OriginalClimate()

    def populate_tables(self) -> None:
        """ETL, from original web data to tidy DB tables."""
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
                {elt} FLOAT  NOT NULL,
                PRIMARY KEY (state, county, stamp)
            )
        """
        )


class PastAndRecentClimate:
    """Aggregate reporting for recent and past historic intervals."""

    PAST = range(1895, 1931)  # half-open interval
    RECENT = range(1991, 2100)  # half-open interval

    def __init__(self, db_url: str = DB_URL):
        self.engine = sa.create_engine(db_url).execution_options(stream_results=True)
        self.meta = sa.MetaData()
        self.log = logging.getLogger(self.__class__.__name__)

    def _get_table(self, table_name: str) -> sa.Table:
        return sa.Table(table_name, self.meta, autoload_with=self.engine)

    def _get_session(self) -> orm.Session:
        return orm.sessionmaker(bind=self.engine)()

    def report(self) -> None:
        lo = self._get_table("tmincy")
        mpc = self._get_table("tmpccy")  # mean per county?
        hi = self._get_table("tmaxcy")
        with self._get_session() as session:
            q = (
                session.query(lo, mpc.c.tmpccy, hi.c.tmaxcy)
                .join(
                    mpc,
                    (mpc.c.state == lo.c.state)
                    & (mpc.c.county == lo.c.county)
                    & (mpc.c.stamp == lo.c.stamp),
                )
                .join(
                    hi,
                    (hi.c.state == lo.c.state)
                    & (hi.c.county == lo.c.county)
                    & (hi.c.stamp == lo.c.stamp),
                )
            )
            insert = sa.text(f"INSERT INTO temperatures  {q}")
            session.begin()
            session.execute(sa.text("DROP TABLE  IF EXISTS  temperatures"))
            session.execute(self._get_create_temperatures())
            session.execute(insert)
            return

            for row in q:
                d = row._asdict()
                d["stamp"] = d["stamp"].strftime("%Y-%m-%d")
                print("\t".join(map(str, d.values())))
                breakpoint()

    @staticmethod
    def _get_create_temperatures() -> sa.text:
        return sa.text("""
            CREATE TABLE IF NOT EXISTS temperatures (
                state   TEXT,
                county  TEXT,
                stamp   TIMESTAMP,
                tmincy  REAL  NOT NULL,
                tmpccy  REAL  NOT NULL,
                tmaxcy  REAL  NOT NULL,
                PRIMARY KEY (state, county, stamp)
            )
        """)


if __name__ == "__main__":
    pd.options.display.max_rows = 7
    logging.basicConfig(level=logging.INFO)

    PastAndRecentClimate().report()
