#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path
import datetime as dt
import re

from pandas.plotting import register_matplotlib_converters
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pytz
import seaborn as sns

matplotlib.use("Agg")

DESKTOP = Path("~/Desktop").expanduser()


def plot(df: pd.DataFrame) -> None:
    register_matplotlib_converters()
    sns.set()

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.scatter(df.stamp, df.range)
    ax2.scatter(df.stamp, df.odometer)
    fig.autofmt_xdate()

    # g = sns.relplot(x='stamp', y='range', kind='line', data=df)
    # g = sns.relplot(x='odometer', y='range', kind='line', data=df)
    # g.fig.autofmt_xdate()

    plt.savefig(DESKTOP / "charge.png")


def read_csv() -> pd.DataFrame:
    stamp_miles_re = re.compile(r"^<(\d{4}-\d+-\d+ \w{3} \d+:\d+)>\s*(\d+)\s+(\d+)")
    telsa = Path("~/repo/sector6-infra/documents/tesla/").expanduser()
    pac = pytz.timezone("US/Pacific")
    rows = []
    with open(telsa / "charge.txt") as fin:
        for line in fin:
            m = stamp_miles_re.search(line)
            if m:
                stamp, odometer, range_ = m.groups()
                stamp = pac.localize(dt.datetime.strptime(stamp, "%Y-%m-%d %a %H:%M"))
                rows.append(
                    {
                        "stamp": stamp,
                        "odometer": int(odometer),
                        "range": int(range_),
                    }
                )
    out_file = str(DESKTOP / "charge.csv")
    columns = list(rows[0].keys())
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(out_file, columns=columns, index=False)
    return df


if __name__ == "__main__":
    plot(read_csv())
