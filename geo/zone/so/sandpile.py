#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/286327/generating-abelian-sandpile

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np

NaN = np.nan


def trough(N):
    i, j = np.shape(N)
    Nt = np.concatenate((np.ones((i, 1)) * NaN, N, np.ones((i, 1)) * NaN), axis=1)
    Nt = np.concatenate(
        (np.ones((1, j + 2)) * NaN, Nt, np.ones((1, j + 2)) * NaN), axis=0
    )
    return Nt


def topple(N):
    P = trough(N)
    sP = np.shape(P)
    while np.nanmax(P) > 3:
        for i, j in np.ndindex(sP):
            if P[i, j] > 3 and np.isnan(P[i, j]) == False:
                P[i, j] -= 4
                P[i + 1, j] += 1
                P[i - 1, j] += 1
                P[i, j + 1] += 1
                P[i, j - 1] += 1
    return P[1:-1, 1:-1]


def Picard(m, n):
    P1 = 6 * np.ones((m, n))
    P1 = topple(P1)
    P2 = 6 * np.ones((m, n))
    Pi = P2 - P1
    Pi = topple(Pi)
    return Pi


M = 500
N = 500
Pi = Picard(M, N)

cmap = cm.get_cmap("viridis_r")

plt.figure()
plt.axes(aspect="equal")
plt.axis("off")
plt.pcolormesh(Pi, cmap=cmap)

dim = str(N) + "x" + str(M)
file_name = "Picard_Identity-" + dim + ".png"

plt.savefig(file_name)
