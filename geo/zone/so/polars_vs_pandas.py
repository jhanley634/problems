#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285312/streaming-parquet-file-in-chunks-for-write-operation

from io import BytesIO
from pathlib import Path
from time import sleep, strftime
from types import FunctionType
from typing import Callable
import logging

from memory_profiler import profile
import pandas as pd
import polars as pl
import requests

_CACHE_DIR = Path("/tmp")
log = logging.getLogger(__name__)


def _get_file(url: str) -> Path:
    fspec = _CACHE_DIR / Path(url).name
    if not fspec.exists():
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        fspec.write_bytes(resp.content)
    return fspec


def _get_buf(year: int) -> BytesIO:
    # url to fetch NY Taxi data from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-01.parquet"
    fspec = _get_file(url)
    return BytesIO(fspec.read_bytes())


assert isinstance(profile, FunctionType)

profile1: Callable[[Callable[..., None]], Callable[..., None]] = profile


@profile1
def fetch_ny_data(parquet_buffer: BytesIO) -> None:
    # Direct reading of parquet file using read_parquet_file leads to high memory consumption
    pause()
    log.info("1: Reading into polars")
    parquet_buffer.seek(0)
    df1 = pl.read_parquet(parquet_buffer)

    log.info("2: Reading into pandas")
    parquet_buffer.seek(0)
    df = pd.read_parquet(parquet_buffer)
    print(len(df))
    log.info("3: Done")
    parquet_buffer.seek(0)
    df1 = pl.read_parquet(parquet_buffer)
    print(df1)
    print(df1.describe())


def pause(secs: float = 0.2) -> None:
    sleep(secs)


def logging_basic_config(level: int = logging.INFO) -> None:
    tz = strftime("%z")
    fmt = f"%(asctime)s.%(msecs)03d{tz} %(levelname)s %(relativeCreated)d %(name)s  %(message)s"
    logging.basicConfig(level=level, datefmt="%Y-%m-%d %H:%M:%S", format=fmt)


if __name__ == "__main__":
    logging_basic_config()
    log.info("starting")

    buf = _get_buf(2022)
    for _ in range(3):
        fetch_ny_data(buf)

    log.info("done")
    pause()
