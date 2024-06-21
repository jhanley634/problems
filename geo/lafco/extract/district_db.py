#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter, defaultdict
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


_housenum_street_re = re.compile(r"^(\d+) (.+)$")


def _clean_rows(df: pd.DataFrame) -> Generator[dict[str, str], None, None]:
    street_to_city = _street_to_city(df)

    for i, row in df.iterrows():
        if row.mail_address.startswith(row.address):
            if m := _housenum_street_re.match(row.address):
                row["housenum"] = int(m[1])
                row["street"] = m[2]
                del row["mail_address"]
                assert row.zip in {"94025", "94301", "94303", "94306"}, row.zip
                if row.city != street_to_city[row.street]:
                    if False:
                        print(
                            row.address.ljust(30),
                            row.city + "\t",
                            street_to_city[row.street],
                        )
                yield dict(row)
        else:
            if m := _housenum_street_re.match(row.address):
                row["housenum"] = int(m[1])
                row["street"] = m[2]
                del row["mail_address"]
                if row.street in street_to_city:
                    yield dict(row)
                    if False:
                        print(
                            row.address.ljust(30),
                            street_to_city[row.street] + "\t",
                            row.mail_address,
                            row.city,
                            row.st,
                            row.zip,
                        )


def _street_to_city(df: pd.DataFrame) -> dict[str, str]:
    """Returns a dict mapping street to city.

    We assume each street is in just one city.
    This is mostly true, but breaks down in the case of e.g.
    2208 Menalto Ave
    2177 Poplar Ave
    2189 Ralmar Ave
    2237 Dumbarton Ave
    Fortunately these are close enough that geocoding is forgiving.
    What we really care about is that a Menalto address not
    be ascribed to San Francisco or Sacramento.
    """
    city_count = defaultdict(Counter)
    for i, row in df.iterrows():
        if row.mail_address.startswith(row.address):
            if m := _housenum_street_re.match(row.address):
                street = m[2]
                city_count[street].update([row.city])
    assert 111 == len(city_count), len(city_count)
    assert city_count["GLORIA WAY"] == Counter({"EAST PALO ALTO": 15, "PALO ALTO": 2})
    return {street: city_count[street].most_common(1)[0][0] for street in city_count}


def extract_all_customer_addrs(in_csv: Path = Path("lafco/district-db.csv")) -> None:
    df = pd.DataFrame(_get_df(in_csv))
    df = df.sort_values(by=["city", "st", "street", "housenum"])
    df.to_csv("/tmp/resident_addr.csv", index=False)
    assert 4079 == len(df), len(df)


typer.run(extract_all_customer_addrs)
