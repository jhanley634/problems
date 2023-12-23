#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/288493/comparison-of-two-excel-files-ignoring-line-order

from collections import Counter
from hashlib import sha3_224
from pathlib import Path
from typing import Generator

import openpyxl
import typer


def hash_spreadsheet(
    in_file: Path, birthday_nybbles: int = 16
) -> Generator[str, None, None]:
    """Turns rows of first sheet into hashes.

    Hang on to a long enough hash prefix to make a birthday collision unlikely;
    64 bits works fine until input sheets start having more than about four billion rows.
    https://en.wikipedia.org/wiki/Birthday_problem
    """
    wb = openpyxl.load_workbook(in_file)
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        yield sha3_224(str(row).encode()).hexdigest()[:birthday_nybbles]


def identical_sheets_sort(in_file1: Path, in_file2: Path) -> bool:
    """True if the two spreadsheets have the same rows, in any order."""
    hashes1 = " ".join(sorted(hash_spreadsheet(in_file1)))
    hashes2 = " ".join(sorted(hash_spreadsheet(in_file2)))
    return hashes1 == hashes2


def identical_sheets_multiset(in_file1: Path, in_file2: Path) -> bool:
    """True if the two spreadsheets have the same rows, in any order."""
    hashes = Counter(hash_spreadsheet(in_file1))
    hashes.subtract(hash_spreadsheet(in_file2))
    return sum(map(abs, hashes.values())) == 0


def main(in_file1: Path, in_file2: Path) -> None:
    not_ = "" if identical_sheets_multiset(in_file1, in_file2) else "n't"
    print(f"The two spreadsheets are{not_} identical.\t", in_file1, in_file2)


if __name__ == "__main__":
    typer.run(main)
