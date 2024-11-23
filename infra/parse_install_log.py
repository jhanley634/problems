#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Generator
from io import TextIOWrapper
from pathlib import Path
import re

import typer


def get_package_revs(fin: TextIOWrapper) -> Generator[str]:
    from_re = re.compile(r"^Requirement already satisfied: .*\(from (\w+)>=(\d+\.\d+)")
    using_cached_re = re.compile(r"^\s*Using cached (\w+)-(\d+\.\d+)")
    for line in fin:
        m = from_re.search(line) or using_cached_re.search(line)
        if m:
            pkg, rev = map(str.lower, m.groups())
            yield f"{pkg:<12} >= {rev}"


def main(log_file_in: Path) -> None:
    with open(log_file_in, encoding="utf8") as fin:
        pkg_versions = sorted(set(get_package_revs(fin)))
    print("\n".join(pkg_versions))


if __name__ == "__main__":
    # infra/parse_install_log.py  /tmp/req7-pip-install-log.txt
    typer.run(main)
