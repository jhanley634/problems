#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from gspread.auth import READONLY_SCOPES
import gspread
import pandas as pd

from geo.lafco.lafco_util import clean_column_names


def read_google_sheet() -> pd.DataFrame:
    gc = gspread.auth.service_account(scopes=READONLY_SCOPES)
    workbook = gc.open("completed-forms")
    assert [["completed forms"]] == workbook.sheet1.get("A1")

    sandy = workbook.worksheet("sandy-2024-04-29")  # type: ignore [no-untyped-call]
    values = sandy.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    df = clean_column_names(df)
    return pd.concat([df.apn, df.addr, df.city, df.date_signed], axis=1)
    # drop_cols = ["form_type", "apn2", "addr2", "color", "form_changes"]


def verify_apns() -> None:
    df = read_google_sheet()
    print(df)
    for i, row in df.iterrows():
        if not row.addr:
            continue
        assert 11 == len(row.apn), row


if __name__ == "__main__":
    verify_apns()
