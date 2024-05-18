#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


from gspread.auth import READONLY_SCOPES
import gspread
import pandas as pd

from geo.lafco.lafco_util import clean_column_names, get_session
from geo.lafco.model import ApnAddress

workbook_name = "completed-forms"


def read_google_sheet(sheet_name: str = "through-100") -> pd.DataFrame:
    # sheet_name="sandy-2024-04-29"
    # sheet_name="laura-2024-05-05"
    # sheet_name="chuck-2024-05-12"
    gc = gspread.auth.service_account(scopes=READONLY_SCOPES)
    workbook = gc.open(workbook_name)
    assert [["completed forms"]] == workbook.sheet1.get("A1")

    sheet = workbook.worksheet(sheet_name)  # type: ignore [no-untyped-call]
    values = sheet.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    df = clean_column_names(df)
    return pd.concat([df.apn, df.addr, df.city, df.date_signed], axis=1)
    # drop_cols = ["form_type", "apn2", "addr2", "color", "form_changes"]


def get_sheet_names() -> list[str]:
    gc = gspread.auth.service_account(scopes=READONLY_SCOPES)
    workbook = gc.open(workbook_name)
    return [sheet.title for sheet in workbook.worksheets()][1:]


odd_apns = {
    "114-370-020",
    # "113-740-080",
}


def verify_apns() -> None:
    df = read_google_sheet()
    print(df)
    with get_session() as sess:
        for i, row in df.iterrows():
            if not row.addr:
                continue
            if row.apn:
                assert 11 == len(row.apn), row
                aa = sess.get(ApnAddress, row.apn)
                # Just compare the house numbers, to avoid e.g. Bayshore != E Bayshore
                if aa is None:
                    if row.apn not in odd_apns:
                        print(i, aa, row.apn, dict(row))
                        print()
                else:
                    sn = aa.situs_addr.split()[0]
                    n = row.addr.split()[0]
                    assert sn == n, (aa.apn, aa.situs_addr, row.addr)
            else:
                print(i, row)
                pfx = row.addr[:5] + "%"
                q = sess.query(ApnAddress).filter(ApnAddress.situs_addr.like(pfx))
                for result in q:
                    print(result.apn, result.situs_addr)


if __name__ == "__main__":
    while True:
        verify_apns()
        input("? ")
