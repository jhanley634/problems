#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
import gspread
import pandas as pd


def read_google_sheet() -> None:
    gc: Client = gspread.auth.service_account()
    assert isinstance(gc, Client)

    wkbk: Spreadsheet = gc.open("completed-forms")
    assert isinstance(wkbk, Spreadsheet)
    assert [["completed forms"]] == wkbk.sheet1.get("A1")

    sandy = wkbk.worksheet("sandy-2024-04-29")  # type: ignore [no-untyped-call]
    values = sandy.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    print(df)


if __name__ == "__main__":
    read_google_sheet()
