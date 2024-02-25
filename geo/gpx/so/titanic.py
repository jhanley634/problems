#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

import pandas as pd
import polars as pl

# 'https://raw.githubusercontent.com/simak-Olga/sem11/main/titanic.csv'
url = "https://raw.githubusercontent.com/Geoyi/Cleaning-Titanic-Data/master/titanic_original.csv"


def main() -> None:
    df = pd.read_csv(url)
    # print(df.describe())
    # print(df.info())

    df = pl.DataFrame(df)
    print(df)
    print(df.describe())


if __name__ == "__main__":
    main()
