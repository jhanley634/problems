#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
EPASD serves about 350 properties (about 600 registered voters) in Menlo Park.
The Menlo Park properties served by EPASD are located on
Byers, Elliot, Emma, Euclid, Falk, French Ct, Green, Menalto, Oak Ct, O’Connor, O’Keefe, and Woodland.
"""
import pandas as pd

from geo.lafco.extract.district_db import extract_all_customer_addrs

mp_streets = [
    "BYERS",
    "ELLIOT",
    "EMMA",
    "EUCLID",
    "FALK",
    "FRENCH CT",
    "GREEN",
    "MENALTO",
    "OAK CT",
    "OCONNOR",
    "OKEEFE",
    "WOODLAND",
]


def report() -> None:
    print(1)
    df = extract_all_customer_addrs()
    print(df)
    print(2)


if __name__ == "__main__":
    print(0)
    report()
