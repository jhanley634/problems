#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


from collections.abc import Generator
from pathlib import Path
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

desktop = Path("~/Desktop").expanduser()


def _get_rows(
    in_file: Path, thresh: float = 2000.0
) -> Generator[dict[str, dt.date | float], None, None]:
    with open(in_file) as fin:
        date: dt.date | None = None
        for orig_line in fin:
            line = orig_line.rstrip()
            if "/" in line and " " not in line:
                offset = " +0000"
                date = dt.datetime.strptime(line + offset, "%m/%d/%y %z").date()
            if line.startswith("$"):
                assert date
                charge = float(line[1:].replace(",", ""))
                if charge < thresh:
                    yield {"date": date, "charge": charge}
                date = None


def report(in_file: Path = desktop / "pge_bill.txt") -> None:
    df = pd.DataFrame(_get_rows(in_file))
    df["date"] = pd.to_datetime(df.date)
    print(df.dtypes)
    print(df.describe())

    out_file = in_file.with_suffix(".csv")
    df.to_csv(out_file, index=False)

    sns.scatterplot(data=df, x="date", y="charge")
    plt.ylim([0, None])
    plt.show()


if __name__ == "__main__":
    report()
