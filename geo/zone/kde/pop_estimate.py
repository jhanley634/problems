#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# cf https://stackabuse.com/kernel-density-estimation-in-python-using-scikit-learn
from collections.abc import Callable

from numpy.typing import NDArray
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_1d_bimodal_random_data(seed: int = 17) -> NDArray[np.float64]:
    rng = np.random.RandomState(seed)
    dat = rng.lognormal(0, 0.3, 1000)
    x = dat
    dat = rng.normal(3, 1, 1000)
    x = np.concatenate((x, dat))
    return x


def sparse_population_data() -> NDArray[np.int64]:
    a = np.array([0, 0, 0, 0, 0, 0, 6, 16, 8, 0, 0, 0, 5, 15, 35, 5, 0, 0, 0, 0])
    assert 20 == len(a)
    return a


def estimate_1d_data(
    generator: Callable[[], NDArray[np.int_]] = sparse_population_data
) -> None:
    df = pd.DataFrame()
    df["x"] = generator()
    df.plot.density()

    x_train = np.array(df.x).reshape(-1, 1)
    x_test = np.linspace(-1, 20, len(df.x))[:, np.newaxis]

    model = KernelDensity()
    model.fit(x_train)
    log_dens = model.score_samples(x_test)
    plt.scatter(x_test, np.exp(log_dens), c="cyan")

    _grid_search(x_train, x_test)

    plt.show()


def _grid_search(
    x_train: NDArray[np.float64],
    x_test: NDArray[np.float64],
) -> None:
    bandwidth = np.arange(0.05, 2, 0.05)
    kde = KernelDensity(kernel="gaussian")
    grid = GridSearchCV(kde, {"bandwidth": bandwidth})
    grid.fit(x_train)

    kde = grid.best_estimator_
    log_dens = kde.score_samples(x_test)
    plt.fill(x_test, np.exp(log_dens), c="green")
    plt.title("Optimal estimate with Gaussian kernel")
    plt.show()
    print("optimal bandwidth: " + "{:.2f}".format(kde.bandwidth))


if __name__ == "__main__":
    estimate_1d_data()
