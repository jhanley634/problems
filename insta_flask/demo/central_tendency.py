# Copyright 2023 John Hanley. MIT licensed.
import numpy as np


def ct_mean(x):
    return sum(x) / len(x)


def ct_median(x):
    return np.median(x)
