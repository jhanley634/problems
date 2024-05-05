#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Datasource is CSV exports from https://gis.smcgov.org/Html5Viewer/?viewer=raster
"""
from pathlib import Path

from sqlalchemy import MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
import sqlalchemy as sa

from geo.lafco.apn_prefix import get_apn_prefix_df
from geo.lafco.model import ApnAddress

_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    db_file = Path("/tmp/apn.db")
    _engine = _engine or sa.create_engine(f"sqlite:///{db_file}")
    return _engine


def get_session() -> Session:
    return Session(get_engine())


def create_table() -> None:
    df = get_apn_prefix_df("063")
    engine = get_engine()
    metadata = MetaData()
    metadata.create_all(engine, tables=[ApnAddress.__table__])
    with get_session() as sess:
        sess.query(ApnAddress).delete()
        sess.commit()
    df.to_sql("apn_address", engine, if_exists="append", index=False)


if __name__ == "__main__":
    create_table()
