#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

from numpy import loadtxt
from tqdm import tqdm
import typer


def read_files(in_folder: Path = "/tmp/loadtxt.d") -> None:
    # Uses loadtxt() to read a thousand files in 46.2s, at rate of 22.3 it/s.
    # In contrast .readlines() takes 1.8s, at a rate of 855 it/s,
    # readlines + split takes 4.6s at rate of 253 it/s,
    # and readlines + split + float parse takes 5.8s at rate of 191 it/s.
    assert in_folder.is_dir(), in_folder
    for fspec in tqdm(sorted(in_folder.glob("*.txt"))):
        read_file1(fspec)


def read_file1(fspec) -> None:
    a = loadtxt(fspec)
    assert (12500, 2) == a.shape


def read_file4(fspec) -> None:
    with open(fspec) as fin:
        a = [float(y) for x, y in map(str.split, fin.readlines())]

    assert 12_500 == len(a)


if __name__ == "__main__":
    typer.run(read_files)
