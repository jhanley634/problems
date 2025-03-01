#! /usr/bin/env python
# Copyright 2025 John Hanley. MIT licensed.

from collections.abc import Generator
from datetime import UTC
from pathlib import Path
from typing import Any
import datetime as dt

from pdftotext import PDF
import pandas as pd


def get_lines(file: Path) -> Generator[str]:
    in_preamble = True
    with open(file, "rb") as fin:
        for page in PDF(fin):
            for line in page.splitlines():
                if line and not in_preamble:
                    yield line
                if line.startswith("AUTOMATIC PAYMENT - THANK YOU"):
                    in_preamble = False


def get_triples(file: Path, year: int = 2024) -> Generator[dict[str, Any]]:
    day = dt.datetime.now(UTC)
    vendor = ""
    amt = 0.0
    gl = get_lines(file)
    for _ in gl:
        try:
            mm_dd = next(gl)
            day = dt.datetime.strptime(f"{year}/{mm_dd} +0000", "%Y/%m/%d %z")
            vendor = next(gl)
            amt = float(next(gl))
        except ValueError:
            pass
        except StopIteration:
            break
        if amt:
            yield {
                "day": f"{day.date()}",
                "amt": amt,
                "vendor": vendor,
            }
            amt = 0.0


def main() -> None:
    statements = Path("~/Desktop").expanduser() / '2025/statements'
    yymm = "????"
    nnn = "0??"
    glob = f"????-202?{yymm}-Statement-{nnn}.pdf"
    for file in sorted(statements.glob(glob)):
        df = pd.DataFrame(get_triples(file))
        print(f"\n\n{file.name}\n")
        print(df.sort_values(by=["vendor", "amt", "day"]))


if __name__ == "__main__":
    main()
