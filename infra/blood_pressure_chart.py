#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from csv import DictReader
from enum import Enum, auto
from typing import Generator

from beartype import beartype
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

from infra.blood_pressure import get_bp_table


class BpCategory(Enum):
    NORMAL = auto()
    ELEVATED = auto()
    STAGE1 = auto()
    STAGE2 = auto()
    HYPERTENSIVE_CRISIS = auto()

    def __str__(self) -> str:
        return f"{self.value * 10}"


@beartype
def get_bp_category(systole: int, diastole: int) -> BpCategory:
    # https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings
    if systole > 180 or diastole > 120:
        return BpCategory.HYPERTENSIVE_CRISIS

    if systole > 140 or diastole > 90:
        return BpCategory.STAGE2

    if systole > 130 or diastole > 80:
        return BpCategory.STAGE1

    if systole > 120:
        return BpCategory.ELEVATED

    return BpCategory.NORMAL


def _to_int(s: str) -> int | str:
    """Converts to an int, if possible.

    Date strings are returned as-is."""
    if s.isnumeric():
        return int(s)
    return s


def _get_rows() -> Generator[dict[str, int], None, None]:
    for row in DictReader(get_bp_table().splitlines()):
        row = {k.strip(): _to_int(v.strip()) for k, v in row.items()}
        row["category"] = get_bp_category(row["systolic"], row["diastolic"]).value * 10
        yield row


def main(meas: str = "measurement") -> None:
    df = pd.DataFrame(_get_rows())
    df["time"] = pd.to_datetime(df.time)
    df = df.drop(columns="pulse")
    df = df.sort_values("time")
    tidy = df.melt("time", var_name=meas, value_name="value")

    sns.scatterplot(data=tidy, x="time", y="value", hue=meas)
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()
