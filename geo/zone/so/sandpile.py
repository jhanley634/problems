#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/286327/generating-abelian-sandpile
from pathlib import Path
from time import time
from typing import Any

from numba import njit
from numpy.typing import NDArray
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np

NaN = np.nan


@njit  # type: ignore [misc]
def trough(n: NDArray[np.float64]) -> NDArray[np.float64]:
    w, h = np.shape(n)
    nt = np.concatenate((np.ones((w, 1)) * NaN, n, np.ones((w, 1)) * NaN), axis=1)
    nt = np.concatenate(
        (np.ones((1, h + 2)) * NaN, nt, np.ones((1, h + 2)) * NaN), axis=0
    )
    assert isinstance(nt, np.ndarray)
    return nt


@njit  # type: ignore [misc]
def topple(n: NDArray[np.float64]) -> NDArray[np.float64]:
    p = trough(n)
    s_p = np.shape(p)
    while np.nanmax(p) > 3:
        for i, j in np.ndindex(s_p):
            if p[i, j] > 3 and not np.isnan(p[i, j]):
                p[i, j] -= 4
                p[i + 1, j] += 1
                p[i - 1, j] += 1
                p[i, j + 1] += 1
                p[i, j - 1] += 1
    assert isinstance(p, np.ndarray)
    return p[1:-1, 1:-1]


def picard(m: int, n: int) -> np.ndarray[Any, np.dtype[np.float64]]:
    p1 = 6 * np.ones((m, n))
    p1 = topple(p1)
    p2 = 6 * np.ones((m, n))
    p_i = p2 - p1
    p_i = topple(p_i)
    return p_i


def main(m: int = 300, n: int = 300) -> None:
    picard(4, 4)  # warmup

    t0 = time()
    p_i = picard(m, n)
    print(f"elapsed: {time() - t0:.3f} sec")

    plt.figure()
    plt.axes(aspect="equal")
    plt.axis("off")
    plt.pcolormesh(p_i, cmap=mp.colormaps["viridis_r"])

    dim = f"{n}x{m}"
    file_name = Path("/tmp") / f"Picard_Identity-{dim}.png"
    plt.savefig(file_name)


if __name__ == "__main__":
    main()
