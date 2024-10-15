#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

from rust_fast import load_txt
from tqdm import tqdm
import numpy as np
import typer


def main(in_folder: Path = "/tmp/loadtxt.d") -> None:
    for in_file in tqdm(sorted(in_folder.glob("*.txt")), smoothing=0.002):
        vals = load_txt(in_file.as_posix())
        a = np.array(vals)

        assert (12_500,) == a.shape
        assert np.float64 == a.dtype
        if vals[0] == -0.0015479121:
            assert vals[1] == -0.0008777569


if __name__ == "__main__":
    typer.run(main)
