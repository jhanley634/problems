#! /usr/bin/env python

# https://stackoverflow.com/questions/74912653/how-can-i-efficiently-plot-a-distance-matrix-using-seaborn
import gc

from scipy.spatial.distance import pdist, squareform
from uszipcode import SearchEngine
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def distance_matrix(df: pd.DataFrame, metric: str = "euclidean"):
    df = df[["zipcode", "lat", "lng", "population", "population_density"]]
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
    zips = search.by_coordinates(37.46, -122.15, radius=100, returns=10)
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


distance_matrix(get_df())
