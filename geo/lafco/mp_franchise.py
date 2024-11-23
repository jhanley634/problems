#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path

from sqlalchemy.orm import Session
import pandas as pd
import streamlit as st

from geo.lafco.geocode import Geocoder
from geo.lafco.lafco_util import LAFCO_DIR, clean_column_names, get_session
from geo.lafco.model import Owner


def _get_df() -> pd.DataFrame:
    csv = LAFCO_DIR / "2024-05-21 qry EPASD APNs Landowner Protests.csv"
    csv = Path(f"{csv}".replace(" ", "_"))
    df = clean_column_names(pd.read_csv(csv))
    df = df[df.signed_protest_form]
    assert 745, 6 == df.shape
    df = df.dropna(subset=["epa_address"])
    df = df.drop(columns=["mail_address", "mail_city"])
    df = df[df.apn != "063-421-020"]  # DOCTER DANIEL PATRICK, WOODLAND AVE
    assert 734, 4 == df.shape
    assert isinstance(df, pd.DataFrame)
    return df


def _street_num(addr: str) -> str:
    """Supports geographic sort order."""
    house, w1, w2 = addr.replace("'", "").split()[:3]
    n = int(house)
    return f"{w1} {w2} {n:06d}"


GREEN = (0, 255, 0, 255)


def menlo_park_disenfranchised(sess: Session) -> Generator[dict[str, str]]:
    g = Geocoder()
    for _, row in _get_df().iterrows():
        own = sess.query(Owner).filter(Owner.apn == row.apn).one_or_none()
        assert own.address == row.epa_address
        addr = f"{own.address}, {own.city} {own.st} {own.zip}".replace("'", "")
        if own.city == "MENLO PARK" and own.st == "CA":
            loc = g.get_location(addr)
            assert addr == loc.addr, (own, loc)
            if loc.lat > 37.464 or loc.lon > -122.139:
                continue
            yield {
                "apn": own.apn,
                "first_owner": own.first_owner.ljust(30),
                "addr": own.address.replace("'", ""),
                "street_num": _street_num(own.address),
                "lat": loc.lat,
                "lon": loc.lon,
            }


if __name__ == "__main__":
    with get_session() as sess:
        df = pd.DataFrame(menlo_park_disenfranchised(sess))
        df = df.sort_values(by=["street_num", "first_owner", "apn"])
        df = df.drop(columns=["street_num"])
        print(df)
        print(df.describe())
        out_file = Path("/tmp/menlo_park_disenfranchised_protesters.csv")
        df.to_csv(out_file, index=False)
        print(out_file)
        st.title("EPASD landowners that signed")
        st.markdown("----")
        st.map(df, size=4, color=GREEN)
