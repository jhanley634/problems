#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# https://codereview.stackexchange.com/questions/283558/processing-a-very-long-single-line-of-comma-separated-FPs
from collections.abc import Generator
from pathlib import Path
import json

import typer


def svg_json_to_gnuplot(infile: str) -> None:
    assert infile.endswith(".json")
    infile1 = Path(infile).expanduser()
    outfile = infile1.with_suffix(".dat")
    with open(infile) as fin, open(outfile, "w") as fout:
        d = json.load(fin)
        for path in sorted(d.keys()):
            fout.writelines(f"{x}, {y}\n" for x, y in _pairs(d[path]))


def _pairs(nums: list[int]) -> Generator[tuple[int, ...]]:
    for i in range(0, len(nums), 2):
        yield tuple(nums[i : i + 2])


if __name__ == "__main__":
    typer.run(svg_json_to_gnuplot)
