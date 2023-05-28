#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# cf https://stackabuse.com/kernel-density-estimation-in-python-using-scikit-learn

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_1d_bimodal_random_data(seed=17):
    rng = np.random.RandomState(seed)
    x = []
    dat = rng.lognormal(0, 0.3, 1000)
    x = np.concatenate((x, dat))
    dat = rng.normal(3, 1, 1000)
    x = np.concatenate((x, dat))
    return x


def estimate_1d_data():
    df = pd.DataFrame()
    df["x"] = generate_1d_bimodal_random_data()
    df.plot.density()

    x_train = np.array(df.x).reshape(-1, 1)
    x_test = np.linspace(-1, 7, 2000)[:, np.newaxis]

    model = KernelDensity(bandwidth=0.1)
    model.fit(x_train)
    log_dens = model.score_samples(x_test)
    plt.fill(x_test, np.exp(log_dens), c="cyan")
    plt.show()


if __name__ == "__main__":
    estimate_1d_data()
