#! /usr/bin/env python
# Copyright 2025 John Hanley. MIT licensed.

from collections.abc import Generator
from pathlib import Path

from pdftotext import PDF


def get_lines(file: Path) -> Generator[str]:
    preamble = True
    with open(file, "rb") as fin:
        for page in PDF(fin):
            for line in page.splitlines():
                if line and not preamble:
                    yield line
                if line.startswith("AUTOMATIC PAYMENT - THANK YOU"):
                    preamble = False


def report(file: Path, year: int = 2024) -> None:
    gl = get_lines(file)
    next(gl)
    line = next(gl)
    assert "PURCHASE" == line, line
    while True:
        day = next(gl)
        vendor = next(gl)
        amt = next(gl)
        print(day, amt, "\t", vendor)


def main() -> None:
    desktop = Path("~/Desktop").expanduser()
    yymm = "????"
    nnn = "0??"
    glob = f"????-202?{yymm}-Statement-{nnn}.pdf"
    for file in sorted(desktop.glob(glob)):
        report(file)


if __name__ == "__main__":
    main()
