#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://softwareengineering.stackexchange.com/questions/338730/find-k-max-ints-of-an-array-min-heap-vs-selection
from array import array
from collections.abc import Generator
from dataclasses import asdict, dataclass
from heapq import heapify, heappop, heappushpop
from pathlib import Path
from random import shuffle
from time import time
from typing import Any

from matplotlib import pyplot as plt
from seaborn.palettes import SEABORN_PALETTES as palette
from tqdm import tqdm
import pandas as pd
import seaborn as sns


def ratchet(ranks: array[int]) -> Generator[dict[str, int], None, None]:
    """Demonstrates the speed at which we slowly ratchet up a min bound."""
    bound = ranks[0]
    prev = bound
    for i, rank in enumerate(ranks):
        if bound < rank:
            bound = rank
            yield {"idx": i, "bound": bound, "delta": bound - prev}
            prev = bound


def _get_xs(n: int) -> array[int]:
    xs = array("L", range(n))
    shuffle(xs)
    return xs


@dataclass
class Result:
    pushes: int
    elapsed: float


def experiment(n: int, k: int) -> Result:
    xs = list(_get_xs(n))
    t0 = time()
    h, xs = xs[:k], xs[k:]
    heapify(h)
    i = 0
    for x in xs:
        if x > h[0]:
            heappushpop(h, x)
            i += 1

    elapsed = round(time() - t0, 6)

    for x in range(n - k, n):
        assert x == heappop(h)

    return Result(i, elapsed)


def run_experiments() -> Generator[dict[str, float], None, None]:
    """Sweeps through a few decades of problem sizes."""
    for trial in tqdm(range(12)):
        n = 10_000
        while n <= 10_000_000:
            for k in [1, 10, 100, 1_000]:
                param = {"n": n, "k": k}
                result = experiment(**param)
                yield {**param, **asdict(result)}
            n *= 10


def main(csv: Path = Path("/tmp/heap.csv")) -> None:
    ratchet_df = pd.DataFrame(ratchet(_get_xs(int(1e7))))
    no_scientific_notation: dict[str, Any] = {"disable_numparse": True}
    print(ratchet_df.to_markdown(index=False, **no_scientific_notation))

    if not csv.exists():
        df = pd.DataFrame(run_experiments())
        df.to_csv(csv, index=False)
    df = pd.read_csv(csv)
    print(df)
    df["ratio"] = df.n / df.k
    sns.catplot(data=df, x="ratio", y="pushes", hue="k", palette=palette["bright"])
    plt.gca().set(xscale="log", yscale="log")
    plt.show()


if __name__ == "__main__":
    main()
