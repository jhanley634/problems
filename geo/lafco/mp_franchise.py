#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from sqlalchemy.orm import Session
import pandas as pd

from geo.lafco.geocode import Geocoder
from geo.lafco.lafco_util import LAFCO_DIR, clean_column_names, get_session
from geo.lafco.model import Owner


def _get_df() -> pd.DataFrame:
    csv = LAFCO_DIR / "2024-05-21 qry EPASD APNs Landowner Protests.csv"
    df = clean_column_names(pd.read_csv(csv))
    df = df[df.signed_protest_form]
    assert 745, 6 == df.shape
    df = df.dropna(subset=["epa_address"])
    df = df.drop(columns=["mail_address", "mail_city"])
    df = df[df.apn != "063-421-020"]  # DOCTER DANIEL PATRICK, WOODLAND AVE
    assert 734, 4 == df.shape
    assert isinstance(df, pd.DataFrame)
    return df


def menlo_park_disenfranchised(sess: Session) -> None:
    g = Geocoder()
    df = _get_df()
    for _, row in df.iterrows():
        own = sess.query(Owner).filter(Owner.apn == row.apn).one_or_none()
        assert own.address == row.epa_address
        addr = f"{own.address}, {own.city} {own.st} {own.zip}"
        print(addr)
        print(g.get_location(addr))
        print()


if __name__ == "__main__":
    with get_session() as sess:
        menlo_park_disenfranchised(sess)
