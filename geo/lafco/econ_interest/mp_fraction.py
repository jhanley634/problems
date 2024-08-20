#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
EPASD serves about 350 properties (about 600 registered voters) in Menlo Park.
The Menlo Park properties served by EPASD are located on
Byers, Elliot, Emma, Euclid, Falk, French Ct, Green, Menalto, Oak Ct, O’Connor, O’Keefe, and Woodland.
"""
from geo.lafco.extract.district_db import extract_all_customer_addrs

mp_streets = {
    "BYERS DR",
    "ELLIOT DR",
    "EMMA LN",
    "EUCLID",
    "FALK CT",
    "FRENCH CT",
    "GREEN ST",
    "MENALTO AVE",
    "OAK CT",
    "OCONNOR ST",
    "OKEEFE ST",
    "WOODLAND AVE",
}


def report() -> None:
    df = extract_all_customer_addrs().drop(columns=["housenum"])
    assert 4_123 == len(df)
    assert 470 == len(df[df.city == "MENLO PARK"])
    # print(df[df.city == "MENLO PARK"].street.value_counts())

    mp = df[df.street.isin(mp_streets)]
    assert 535 == len(mp)
    assert 442 == len(mp[mp.city == "MENLO PARK"])
    mp = mp[mp.city == "MENLO PARK"]
    print(mp)


if __name__ == "__main__":
    report()
