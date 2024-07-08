#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def main(in_csv=Path("/tmp/fibo.csv")) -> None:
    sns.set_theme()
    df = pd.read_csv(in_csv)
    print(df[df.type == "recursive"].drop(columns=["type"]))
    # sns.boxplot(data=df, x="n", y="msec")
    sns.catplot(data=df, x="n", y="msec", hue="type")
    plt.xticks(rotation=70)
    plt.show()


if __name__ == "__main__":
    main()
