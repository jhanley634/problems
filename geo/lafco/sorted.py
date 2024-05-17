#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from geo.lafco.apn_report import read_google_sheet


def _get_house_num(s: str) -> int:
    return int(s.split()[0])


def _get_street(s: str) -> str:
    return " ".join(s.split()[1:])


def main() -> None:
    df = read_google_sheet()
    df["house_num"] = df.addr.apply(_get_house_num)
    df["street"] = df.addr.apply(_get_street)
    df = df.sort_values(["city", "street", "house_num"])
    df = df.drop(columns=["street", "house_num"])
    print(df)


if __name__ == "__main__":
    main()
