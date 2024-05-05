#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
The excel file has 4273 parcels listed.
There are fewer owners.
Can you parse out the succinct number of owners?
"""
from pathlib import Path
import re

import pandas as pd

csv = Path("~/Desktop/lafco/EPS093KO.xlsx").expanduser()


def clean(name: str) -> str:
    """Converts raw multi-word column name to a clean identifier."""
    xlate = str.maketrans(" .", "__")
    name = name.replace("$", "").strip().translate(xlate).lower()
    name = name.replace("1st_owner", "first_owner")
    assert re.search(r"^[a-z_]+$", name), name
    return name


def distinct_owner_report() -> None:
    df = pd.read_excel(csv)
    df = df.rename(columns={col: clean(col) for col in df.columns})
    assert 4272 == len(df), len(df)
    assert 3594 == df["first_owner"].nunique()

    # trim_trust_synonyms = re.compile(r" (TR|TRS|TRUST)$")

    for i, row in df.iterrows():
        print(row.first_owner)  # pipe to | sort | uniq -c
        # print(trim_trust_synonyms.sub("", row.first_owner))


if __name__ == "__main__":
    distinct_owner_report()
