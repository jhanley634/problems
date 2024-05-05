#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import json
import os
import pprint
import sys

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd


def read_google_sheet() -> None:

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope
    )

    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    wks = gc.open("filled-out-forms").sheet1

    # Get all values from the first row
    values_list = wks.row_values(1)

    # Print all values
    pprint.pprint(values_list)

    # Get all values from the first column
    values_list = wks.col_values(1)

    # Print all values
    pprint.pprint(values_list)

    # Get all values from the first row
    values_list = wks.get_all_values()

    # Convert to DataFrame
    df = pd.DataFrame(values_list[1:], columns=values_list[0])

    # Print DataFrame
    print(df)


if __name__ == "__main__":
    read_google_sheet()
