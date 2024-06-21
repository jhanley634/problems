#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
import io
import re

import pandas as pd
import typer

from geo.lafco.lafco_util import clean_column_names


def _get_df(in_csv: Path) -> Generator[dict[str, str], None, None]:
    csv = in_csv.read_text()
    csv = csv.replace("E PALO", "EAST PALO")
    csv = csv.replace(", ,", ",,")  # dropna(), roughly
    df = pd.read_csv(io.StringIO(csv))
    df = clean_column_names(df)
    df = df[["address", "mail_address", "city", "st", "zip"]]
    df = df.dropna(subset=["address"])
    return _clean_rows(df)


def _clean_rows(df: pd.DataFrame) -> Generator[dict[str, str], None, None]:
    housenum_street_re = re.compile(r"^(\d+) (.+)$")
    for i, row in df.iterrows():
        if row.mail_address.startswith(row.address):
            if m := housenum_street_re.match(row.address):
                row["housenum"] = int(m[1])
                row["street"] = m[2]
                del row["mail_address"]
                # row.address = row.address.ljust(30)
                assert row.zip in {"94025", "94301", "94303", "94306"}
                yield dict(row)


def _street_to_city(df: pd.DataFrame) -> dict[str, str]:
    """Returns a dict mapping street to city.

    We assume each street is in just one city.
    """


def extract_all_customer_addrs(in_csv: Path = Path("lafco/district-db.csv")) -> None:
    df = pd.DataFrame(_get_df(in_csv))
    df = df.sort_values(by=["city", "st", "street", "housenum"])
    df.to_csv("/tmp/resident_addr.csv", index=False)
    assert 2097 == len(df), len(df)


typer.run(extract_all_customer_addrs)
