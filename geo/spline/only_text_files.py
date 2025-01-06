#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# usage:
#    find . | sort | only_text_files.py | xargs grep ...

from pathlib import Path
import re
import sys

import magic


def filter_path_names() -> None:

    exclude_re = re.compile(r"/\.git/|/\.venv/|/__pycache__/")

    for line in sys.stdin:
        if exclude_re.search(line):
            continue
        file = Path(line.rstrip())
        if file.suffix == ".json" or not file.is_file():
            continue

        if " text" in magic.from_file(f"{file}"):
            print(file)


if __name__ == "__main__":
    filter_path_names()
