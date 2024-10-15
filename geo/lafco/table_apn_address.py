#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Datasource is CSV exports from https://gis.smcgov.org/Html5Viewer/?viewer=raster .
"""

from sqlalchemy import Engine, MetaData

from geo.lafco.apn_prefix import get_apn_prefix_df
from geo.lafco.lafco_util import get_engine, get_session
from geo.lafco.model import ApnAddress


def create_table_apn_address() -> Engine:
    df = get_apn_prefix_df("all")
    assert 5825 == len(df), len(df)
    df = df.drop_duplicates(subset=["apn"])
    assert 5479 == len(df), len(df)

    engine = get_engine()
    assert isinstance(engine, Engine)
    metadata = MetaData()
    metadata.create_all(engine, tables=[ApnAddress.__table__])
    with get_session() as sess:
        sess.query(ApnAddress).delete()
        sess.commit()
    df.to_sql("apn_address", engine, if_exists="append", index=False)
    return engine


if __name__ == "__main__":
    create_table_apn_address()
