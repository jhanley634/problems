#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from csv import DictReader
from typing import Generator

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

from infra.blood_pressure import get_bp_table


def _to_int(s: str) -> int | str:
    """Converts to an int, if possible.

    Date strings are returned as-is."""
    if s.isnumeric():
        return int(s)
    return s


def _get_rows() -> Generator[dict[str, int], None, None]:
    for row in DictReader(get_bp_table().splitlines()):
        row = {k.strip(): _to_int(v.strip()) for k, v in row.items()}
        yield row


def main(meas: str = "measurement") -> None:
    df = pd.DataFrame(_get_rows())
    df["time"] = pd.to_datetime(df.time)
    df = df.drop(columns="pulse")
    tidy = df.melt("time", var_name=meas, value_name="value")

    sns.scatterplot(data=tidy, x="time", y="value", hue=meas)
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()
