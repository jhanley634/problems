#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78555544/extract-text-in-between-2-dates-of-identical-format-with-python
from collections.abc import Generator
import re

input_text = """
02/04/2024 Funds Transfer 56.00 1,805.12
TOP-UP TO WALLET! :
84343571729
02/04/2024 Bill Payment 1,000.00 805.12
UHJN-5520380040396554 : I-BANK
03/04/2024 Payments / Collections 10.08 795.04
HU INSURANCE UK
G0003406201 56171304 2024-04-17
G3406201
04/04/2024 FAST Payment / Receipt 12,000.00 12,795.04
INVEST
20240404CIBBSTSTBRT3273519
OTHER
04/04/2024 Bill Payment 333.00 12,462.04
GBU -09890340922 : I-BANK
30/04/2024 Interest Earned 0.18 2,385.42
"""
date_pattern = r"\d{2}/\d{2}/\d{4}"


def get_transactions(text: str) -> Generator[list[str], None, None]:
    pat = re.compile(rf"({date_pattern}.*?)(?={date_pattern}|\Z)", re.DOTALL)
    for xctn in pat.findall(text):
        yield xctn.splitlines()


if __name__ == "__main__":
    list(map(print, get_transactions(input_text)))
    print()
    for xctn in get_transactions(input_text):
        print(xctn)
