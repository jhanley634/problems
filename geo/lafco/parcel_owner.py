#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
The excel file has 4273 parcels listed.

There are fewer owners.
Can you parse out the succinct number of owners?
"""
import pandas as pd

from geo.lafco.lafco_util import LAFCO_DIR, clean_column_names


def get_owner() -> pd.DataFrame:
    csv = LAFCO_DIR / "EPS093KO.xlsx"  # the District Database
    df = pd.read_excel(csv)
    df = clean_column_names(df)
    df = df.rename(columns={"1st_owner": "first_owner"})
    df["units"] = df.units.fillna(1).astype(int)
    assert 4272 == len(df), len(df)
    assert 3594 == df["first_owner"].nunique()
    return df


def distinct_owner_report() -> None:  # pragma: no cover

    # trim_trust_synonyms = re.compile(r" (TR|TRS|TRUST)$")

    df = get_owner()

    for _, row in df.iterrows():
        print(row.first_owner)  # pipe to | sort | uniq -c
        # print(trim_trust_synonyms.sub("", row.first_owner))


if __name__ == "__main__":
    distinct_owner_report()
