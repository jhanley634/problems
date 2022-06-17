#! /usr/bin/env python
from pathlib import Path
from shutil import copyfile

from numpy.random import default_rng
import typer


def generate_all(dest_dir: Path, num_copies: int = 1_000, length: int = 12_500):
    dest_dir.mkdir(exist_ok=True)

    rng = default_rng(seed=42)
    data = rng.uniform(0, 1, length)
    print(data.shape)

    def _fspec(i: int) -> Path:
        return Path(dest_dir / f'scan_{i:04d}.txt')

    for i in range(num_copies):
        _write_one(data, _fspec(i))

def _write_one(data, out_fspec):
    with open(out_fspec, 'w') as fout:
        for n in data:
            fout.write(f'   {3 * n:.7f}e-05  {-2 * n:.7f}e-03\n')


if __name__ == '__main__':
    typer.run(generate_all)
