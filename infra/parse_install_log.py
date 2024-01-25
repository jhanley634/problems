#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path
from typing import Generator
import re

import typer


def get_package_revs(fin: int) -> Generator[str, None, None]:
    from_re = re.compile(r"^Requirement already satisfied: .*\(from (\w+)>=(\d+\.\d+)")
    using_cached_re = re.compile(r"^\s*Using cached (\w+)-(\d+\.\d+)")
    for line in fin:
        m = from_re.search(line) or using_cached_re.search(line)
        if m:
            pkg, rev = map(str.lower, m.groups())
            yield (f"{pkg:<12} >= {rev}")


def main(log_file_in: Path) -> None:
    with open(log_file_in) as fin:
        pkg_versions = sorted(set(get_package_revs(fin)))
    print("\n".join(pkg_versions))


if __name__ == "__main__":
    typer.run(main)
