#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://softwareengineering.stackexchange.com/questions/338730/find-k-max-integers-of-an-array-min-heap-vs-selection-algo
from array import array
from collections.abc import Generator
from random import shuffle

import pandas as pd
import typer


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


def main(n: int = 10_000_000) -> None:
    for trial in range(2):
        df = pd.DataFrame(ratchet(_get_xs(n)))
        if trial < 1:
            print(df.to_markdown(index=False, disable_numparse=True))


if __name__ == "__main__":
    typer.run(main)
