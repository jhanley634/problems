#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75348436/get-an-evenly-distributed-subset-of-combinations-without-repetition
# cf https://math.stackexchange.com/questions/2245194/what-is-the-standard-deviation-of-dice-rolling
from pprint import pp
import random

from numpy.random import default_rng
import matplotlib.pyplot as plt
import pandas as pd
import typer


class Options:
    def __init__(self, all_options, k=4):
        self.all_options = all_options
        self.k = k

    def new_deck(self):
        deck = self.all_options.copy()
        random.shuffle(deck)
        return deck

    def choose_options(self):
        return self.new_deck()[: self.k]

    def choose_many_options(self, n):
        for _ in range(n):
            yield "".join(self.choose_options())


def main(n: int = 1_000_000, lo: int = 0, hi: int = 1000, shuffle: bool = False):
    opt = Options(list("ABCDEFGH"))
    demo = list(opt.choose_many_options(3))
    pp(demo, width=22)

    rng = default_rng()
    plot_randint_counts(pd.DataFrame(rng.integers(lo, hi, size=n), columns=["val"]))

    if shuffle:
        plot_shuffle_combination_counts(
            pd.DataFrame(opt.choose_many_options(n), columns=["opt"])
        )

    plt.show()


def plot_randint_counts(df, verbose=False):
    df["cnt"] = 1
    df_summary = df.groupby("val").sum()
    if verbose:
        with pd.option_context("display.min_rows", 16):
            print(df_summary)
    counts = df_summary.cnt.tolist()
    plt.plot(range(len(counts)), counts)
    plt.plot(range(len(counts)), sorted(counts))
    plt.gca().set_ylim((0, None))
    plt.gca().set_xlabel("rolled dice value")
    plt.gca().set_ylabel("number of occurrences")

    print(df_summary.query("cnt < 920"))
    print(df_summary.query("cnt > 1080"))

    print("mean:", round(df.val.mean(), 3), "std:", round(df.val.std(), 3))
    with pd.option_context("display.float_format", "{:.3f}".format):
        print(df_summary.describe())


def plot_shuffle_combination_counts(df):
    df["cnt"] = 1
    counts = df.groupby("opt").sum().cnt.tolist()
    plt.plot(range(len(counts)), counts)
    plt.plot(range(len(counts)), sorted(counts))
    plt.gca().set_xlim((0, 1700))
    plt.gca().set_ylim((0, None))
    plt.gca().set_xlabel("combination of options")
    plt.gca().set_ylabel("number of occurrences")


if __name__ == "__main__":
    typer.run(main)
