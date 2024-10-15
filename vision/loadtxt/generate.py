#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path
from shutil import copyfile

from numpy.random import default_rng
from tqdm import tqdm
import typer


def generate_all(dest_dir: Path, num_copies: int = 7_000, length: int = 12_500) -> None:
    """Generates example data for a timing comparison.

    Question originally posed in
    https://stackoverflow.com/questions/72611636/optimise-cython-speed-in-for-loop
    """
    dest_dir.mkdir(exist_ok=True)

    rng = default_rng(seed=42)
    data = rng.uniform(0, 1, length)
    print(data.shape)

    def _fspec(i: int) -> Path:
        return Path(dest_dir / f"scan_{i:04d}.txt")

    file0 = _fspec(0)
    with open(file0, "w") as fout:
        for n in data:
            fout.write(f"   {3 * n:.7f}e-05  {-2 * n:.7f}e-03\n")

    for i in tqdm(range(1, num_copies), mininterval=0.2):
        copyfile(file0, _fspec(i))


if __name__ == "__main__":
    typer.run(generate_all)
