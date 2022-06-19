#! /usr/bin/env python
from pathlib import Path

from rust_fast import load_txt
import typer


def main(in_folder: Path = '/tmp/loadtxt.d'):
    for f in sorted(in_folder.glob('*.txt')):
        n = load_txt(str(f))
        print(type(n))
        print(len(n))
        print(type(n[0]))
        assert 42 == n, n
    print(f)


if __name__ == '__main__':
    typer.run(main)
