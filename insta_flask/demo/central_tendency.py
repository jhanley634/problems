# Copyright 2023 John Hanley. MIT licensed.

import numpy as np
import numpy.typing as npt


def ct_mean(x: npt.NDArray[np.float64]) -> float:
    return sum(x) / len(x)


def ct_median(x: npt.NDArray[np.float64]) -> np.float64:
    return np.median(x)
