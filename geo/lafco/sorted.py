#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from typing import Any

from gspread.auth import DEFAULT_SCOPES
from pandas import Series
import pandas as pd

from geo.lafco.apn_report import get_sheet_names, open_workbook, read_google_sheet
from geo.lafco.geocode import Geocoder


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
    df = df.drop_duplicates(subset=["apn"])
    print(df)
    df[["lat", "lon"]] = df.apply(_get_point, axis=1, result_type="expand")
    df.to_csv("/tmp/sorted.csv", index=False)


geocoder = Geocoder()


def _get_point(row: "Series[Any]") -> tuple[float, float]:
    loc = geocoder.get_location(f"{row.addr}, {row.city} CA")
    print(loc)
    return loc.lat, loc.lon


def _replace_sheet(df: pd.DataFrame, sheet_name: str = "combined-and-sorted") -> None:
    workbook = open_workbook(scopes=DEFAULT_SCOPES)
    sheet = workbook.worksheet(sheet_name)
    sheet.batch_clear("A2:D7")


if __name__ == "__main__":
    main()
