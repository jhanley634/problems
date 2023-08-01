#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/286327/generating-abelian-sandpile

from pathlib import Path
from time import time
from typing import Any

from numba import njit
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np

NaN = np.nan


@njit
def trough(
    N: np.ndarray[Any, np.dtype[np.float64]]
) -> np.ndarray[Any, np.dtype[np.float64]]:
    w, h = np.shape(N)
    Nt = np.concatenate((np.ones((w, 1)) * NaN, N, np.ones((w, 1)) * NaN), axis=1)
    Nt = np.concatenate(
        (np.ones((1, h + 2)) * NaN, Nt, np.ones((1, h + 2)) * NaN), axis=0
    )
    return Nt


@njit
def topple(
    N: np.ndarray[Any, np.dtype[np.float64]]
) -> np.ndarray[Any, np.dtype[np.float64]]:
    P = trough(N)
    sP = np.shape(P)
    while np.nanmax(P) > 3:
        for i, j in np.ndindex(sP):
            if P[i, j] > 3 and not np.isnan(P[i, j]):
                P[i, j] -= 4
                P[i + 1, j] += 1
                P[i - 1, j] += 1
                P[i, j + 1] += 1
                P[i, j - 1] += 1
    return P[1:-1, 1:-1]


def picard(m: int, n: int) -> np.ndarray[Any, np.dtype[np.float64]]:
    P1 = 6 * np.ones((m, n))
    P1 = topple(P1)
    P2 = 6 * np.ones((m, n))
    Pi = P2 - P1
    Pi = topple(Pi)
    return Pi


def main(m: int = 300, n: int = 300) -> None:
    picard(4, 4)  # warmup

    t0 = time()
    Pi = picard(m, n)
    print(f"elapsed: {time() - t0:.3f} sec")

    plt.figure()
    plt.axes(aspect="equal")
    plt.axis("off")
    plt.pcolormesh(Pi, cmap=mp.colormaps["viridis_r"])

    dim = f"{n}x{m}"
    file_name = Path("/tmp") / f"Picard_Identity-{dim}.png"
    plt.savefig(file_name)


if __name__ == "__main__":
    main()
