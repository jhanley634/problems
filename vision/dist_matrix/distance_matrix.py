#! /usr/bin/env python

# Copyright 2022 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/74912653/how-can-i-efficiently-plot-a-distance-matrix-using-seaborn
import gc

from scipy.spatial.distance import pdist, squareform
from uszipcode import SearchEngine
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def distance_matrix(df: pd.DataFrame, metric: str = "euclidean") -> None:
    df = df[["zipcode", "lat", "lng", "population_density"]]
    df = df.sort_values(by=["zipcode"])
    print(df)
    dist = pdist(df, metric)
    dist = squareform(dist)
    sns.heatmap(dist, cmap="mako")
    print(dist)
    plt.show()
    del dist
    gc.collect()


def get_df() -> pd.DataFrame:
    search = SearchEngine(SearchEngine.SimpleOrComprehensiveArgEnum.simple)
    zips = search.by_population_density(lower=100, returns=11_000)
    df = pd.DataFrame(z.to_dict() for z in zips)
    df = df[
        [
            "zipcode",
            "post_office_city",
            "county",
            "state",
            "lat",
            "lng",
            "population",
            "population_density",
            "median_home_value",
            "median_household_income",
        ]
    ]
    df["zipcode"] = df.zipcode.astype(int)
    df = df.rename(columns={"post_office_city": "city"})
    return df


if __name__ == "__main__":
    distance_matrix(get_df())
