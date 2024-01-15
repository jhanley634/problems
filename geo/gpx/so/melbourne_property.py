#!/usr/bin/env python3
# Copyright 2024 John Hanley. MIT licensed.

# from https://stackoverflow.com/questions/77768127/accessing-nested-element-using-beautifulsoup

from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag
import typer

url = "https://gist.github.com/sachinruk/9b0aaf5c134aa398f7f201c2b298210a"
raw = (
    "https://gist.githubusercontent.com/sachinruk/9b0aaf5c134aa398f7f201c2b298210a"
    "/raw/2b255fe028f723ed2afbfa7e2679cd0de56b4685/property.html"
)


def parse(in_file: Path) -> None:
    hrule = "=" * 60
    soup = BeautifulSoup(in_file.read_text(), "html.parser")
    tag = soup.find("ol", {"class": "messageList", "id": "messageList"})
    assert isinstance(tag, Tag)
    ol: Tag = tag
    for li in ol.find_all("li"):
        print(f"\n\n{hrule}\n\n{li}")


if __name__ == "__main__":
    print(raw)
    typer.run(parse)
