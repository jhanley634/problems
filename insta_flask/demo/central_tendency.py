# Copyright 2023 John Hanley. MIT licensed.
import numpy as np


def ct_mean(x: np.ndarray):
    return sum(x) / len(x)


def ct_median(x: np.ndarray):
    return np.median(x)
