#! /usr/bin/env python
# Copyright 2025 John Hanley. MIT licensed.

from pathlib import Path

from pdftotext import PDF


def report(fin: Path) -> None:
    for page in PDF(fin):
        print(type(page), page)


def main() -> None:
    desktop = Path("~/Desktop").expanduser()
    yymm = "????"
    nnn = "0??"
    glob = f"????-202?{yymm}-Statement-{nnn}.pdf"
    for file in sorted(desktop.glob(glob)):
        with open(file, "rb") as fin:
            report(fin)


if __name__ == "__main__":
    main()
