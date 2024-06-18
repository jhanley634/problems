#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
from pprint import pp
import io
import re

import pandas as pd
import typer

from geo.lafco.lafco_util import clean_column_names


def _get_df(in_csv: Path) -> pd.DataFrame:
    housenum_street_re = re.compile(r"^(\d+) (.+)$")
    csv = in_csv.read_text()
    csv = csv.replace("E PALO", "EAST PALO")
    csv = csv.replace(", ,", ",,")  # dropna(), roughly
    df = pd.read_csv(io.StringIO(csv))
    df = clean_column_names(df)
    df = df[["address", "mail_address", "city", "st", "zip"]]
    df = df.dropna(subset=["address"])
    for i, row in df.iterrows():
        if row.mail_address.startswith(row.address):
            if m := housenum_street_re.match(row.address):
                row["housenum"] = int(m[1])
                row["street"] = m[2]
                del row["mail_address"]
                # row.address = row.address.ljust(30)
                assert row.zip in {"94025", "94301", "94303", "94306"}
                yield row


def extract_all_customer_addrs(in_csv: Path) -> None:
    df = pd.DataFrame(_get_df(in_csv))
    df = df.sort_values(by=["city", "st", "street", "housenum"])
    df.to_csv("/tmp/resident_addr.csv", index=False)
    assert 2097 == len(df), len(df)


typer.run(extract_all_customer_addrs)
