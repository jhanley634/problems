#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75348436/get-an-evenly-distributed-subset-of-combinations-without-repetition
from pprint import pp
import random

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


def main(n: int = 1_000_000):
    opt = Options(list("ABCDEFGH"))
    demo = list(opt.choose_many_options(3))
    pp(demo, width=22)

    df = pd.DataFrame(opt.choose_many_options(n), columns=["opt"])
    df["cnt"] = 1
    with pd.option_context("display.min_rows", 16):
        print(df.groupby("opt").sum())
    cnts = df.groupby("opt").sum().cnt.tolist()
    plt.plot(range(len(cnts)), cnts)
    plt.plot(range(len(cnts)), sorted(cnts))
    plt.gca().set_xlim((0, 1700))
    plt.gca().set_ylim((0, None))
    plt.gca().set_xlabel("combination of options")
    plt.gca().set_ylabel("number of occurrences")
    plt.show()


if __name__ == "__main__":
    typer.run(main)
