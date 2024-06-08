#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Datasource is the EPS093KO spreadsheet
(from O'Connor Water?)
"""

from sqlalchemy import Engine, MetaData

from geo.lafco.lafco_util import get_engine, get_session
from geo.lafco.model import Owner
from geo.lafco.parcel_owner import get_owner

_drop_columns = [
    "charge",
    "rate",
    "location",
    "premis",
    "prevwtr",
    "water",
    "prev",
    "comment",
    "tra",
    "exemptions",
    "care_of",
    "mail_address",
]


def create_table_owner() -> Engine:
    df = get_owner()
    df = df.drop(columns=_drop_columns)
    df = df.drop_duplicates(subset=["apn"])  # discard ~ 50 dup rows
    engine = get_engine()
    metadata = MetaData()
    metadata.create_all(engine, tables=[Owner.__table__])
    with get_session() as sess:
        sess.query(Owner).delete()
        sess.commit()
    # print(df)
    # print(df.info())
    df.to_sql("owner", engine, if_exists="append", index=False)
    return engine


if __name__ == "__main__":
    create_table_owner()
