#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_df():
    # df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df = pd.DataFrame(
        columns=["stamp", "close"],
        data=[
            ["2024-01-02 16:00", 110],
            ["2024-01-03 16:00", 110],
            ["2024-01-04 16:00", 110],
            ["2024-01-05 16:00", 120],
            ["2024-01-08 16:00", 120],
            ["2024-01-09 16:00", 120],
        ],
    )
    df["stamp"] = pd.to_datetime(df["stamp"])
    return df


def main():
    df = get_df()
    sns.lineplot(x="stamp", y="close", data=df)
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()
