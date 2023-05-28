#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# cf https://stackabuse.com/kernel-density-estimation-in-python-using-scikit-learn

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_data(seed=17):
    rng = np.random.RandomState(seed)
    x = []
    dat = rng.lognormal(0, 0.3, 1000)
    x = np.concatenate((x, dat))
    dat = rng.normal(3, 1, 1000)
    x = np.concatenate((x, dat))
    return x


if __name__ == "__main__":
    df = pd.DataFrame()
    df["x"] = generate_data()

    # sns.displot(df, x="x", kind="kde")
    df.plot.density()
    plt.show()
