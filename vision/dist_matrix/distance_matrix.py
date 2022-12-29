#! /usr/bin/env python

# https://stackoverflow.com/questions/74912653/how-can-i-efficiently-plot-a-distance-matrix-using-seaborn
import gc

from scipy.spatial.distance import pdist, squareform
import pandas as pd
import seaborn as sns


# distance matrix
def distance_matrix(df_labeled, metric="euclidean"):
    df_labeled.sort_values(by=["cluster"], inplace=True)
    dist = pdist(df_labeled, metric)
    dist = squareform(dist)
    sns.heatmap(dist, cmap="mako")
    print(dist)
    del dist
    gc.collect()


final_df = pd.DataFrame([dict(a=1, b=2)])

distance_matrix(final_df)
