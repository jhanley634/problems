#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import pandas as pd

from geo.lafco.apn_report import get_sheet_names, read_google_sheet


def _get_house_num(s: str) -> int:
    return int(s.split()[0])


def _get_street(s: str) -> str:
    return " ".join(s.split()[1:])


def main() -> None:
    names = get_sheet_names()
    df = pd.concat([read_google_sheet(name) for name in names])
    df["house_num"] = df.addr.apply(_get_house_num)
    df["street"] = df.addr.apply(_get_street)
    df = df.sort_values(["city", "street", "house_num"])
    df = df.drop(columns=["street", "house_num"])
    print(df)


if __name__ == "__main__":
    main()
