#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter, defaultdict
from collections.abc import Generator
from hashlib import file_digest, sha3_224
from pathlib import Path
import io
import re

import pandas as pd
import typer

from geo.lafco.lafco_util import clean_column_names

_housenumber_missing = {
    " BAY RD",
    " DEMETER ST",
    " DONOHOE ST",
    " GARDEN ST",
    " GREEN ST",
    " MENALTO AVE",
    " OAKDALE",
    " RUNNYMEDE ST",
    " ST",
    " TARA RD",
    " VACANT LAND",
    " WEEKS ST",
    " WOODLAND AVE",
    "1958.5 MENALTO AVE",
    "1960.5 MENALTO AVE",
    "2033A PULGAS AVE",
    "2192A COOLEY AVE",
    "222A OAK CT",
    "2325A CLARKE AVE",
    "575A BELL ST",
    "877-A DONOHOE ST",
    "877-B DONOHOE ST",
    "877-C DONOHOE ST",
    "8881/2 GREEN ST",
}


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
        if m := _housenum_street_re.match(row.address):
            row["housenum"] = int(m[1])
            row["street"] = m[2]
            if row.mail_address.startswith(row.address):
                assert row.zip in {"94025", "94301", "94303", "94306"}, row.zip
                del row["mail_address"]
                yield dict(row)
            else:
                if row.street in street_to_city:
                    row["city"] = street_to_city[row.street]
                    row["st"] = "CA"
                    row["zip"] = "94303"
                    del row["mail_address"]
                    yield dict(row)
        else:
            assert row.address in _housenumber_missing, row.address


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
    city_count: dict[str, Counter[str]] = defaultdict(Counter)
    for street in [
        "BLUE JAY CT",
        "DEMETER ST",
        "JAMIE LN",
        "MANHATTAN AVE",
        "NEWELL CT",
        "PULGAS AV",
        "SCOFIELD AVE",
        "TARA RD",
    ]:
        city_count[street].update(["EAST PALO ALTO"])

    for i, row in df.iterrows():
        if row.mail_address.startswith(row.address):
            if m := _housenum_street_re.match(row.address):
                street = m[2]
                city_count[street].update([row.city])
    assert 119 == len(city_count), len(city_count)
    assert city_count["GLORIA WAY"] == Counter({"EAST PALO ALTO": 15, "PALO ALTO": 2})
    return {street: city_count[street].most_common(1)[0][0] for street in city_count}


desktop = Path("~/Desktop").expanduser()


def extract_all_customer_addrs(
    in_csv: Path = desktop / "lafco/district-db.csv",
) -> pd.DataFrame:
    assert (670417, "38d34a95") == fingerprint(in_csv)
    df = pd.DataFrame(_get_df(in_csv))
    df = df.sort_values(by=["city", "st", "street", "housenum"])
    df.to_csv("/tmp/resident_addr.csv", index=False)
    assert 4123 == len(df), len(df)
    return df


def fingerprint(in_file: Path, nybbles: int = 8) -> tuple[int, str]:
    """Returns the given file's size along with a truncated SHA3 hash,
    so we know we have the expected file version.
    """
    with open(in_file, "rb") as fin:
        digest = file_digest(fin, sha3_224)
    return in_file.stat().st_size, digest.hexdigest()[:nybbles]


if __name__ == "__main__":
    typer.run(extract_all_customer_addrs)
