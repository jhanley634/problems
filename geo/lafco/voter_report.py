#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import pandas as pd

from geo.lafco.apn_report import open_workbook
from geo.lafco.lafco_util import clean_column_names, get_session
from geo.lafco.model import ApnAddress

VOTER_FORMS = "voter-forms"


def read_google_sheet(sheet_name: str = "Sheet1") -> pd.DataFrame:

    workbook = open_workbook(VOTER_FORMS)

    sheet = workbook.worksheet(sheet_name)  # type: ignore [no-untyped-call]
    values = sheet.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0])
    df = clean_column_names(df)
    return pd.concat([df.apn, df.addr, df.city, df.date_signed], axis=1)


def get_sheet_names() -> list[str]:
    workbook = open_workbook(VOTER_FORMS)
    return [sheet.title for sheet in workbook.worksheets()]


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
                    print(i, aa, row.apn, dict(row))
                    print()
                else:
                    sn = aa.situs_addr.split()[0]
                    n = row.addr.split()[0]
                    assert sn == n, (aa.apn, aa.situs_addr, row.addr)
            else:
                print(i, row)
                pfx = row.addr[:6] + "%"
                q = sess.query(ApnAddress).filter(ApnAddress.situs_addr.like(pfx))
                for result in q:
                    print(result.apn, result.situs_addr)


if __name__ == "__main__":
    while True:
        verify_apns()
        input("? ")
