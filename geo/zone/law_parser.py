#! /usr/bin/env python
from pathlib import Path

from bs4 import BeautifulSoup
import typer


class LawParser:
    """Scans leginfo.legislature.ca.gov zoning code
    to identify the proper indent level."""

    def __init__(self, path: Path):
        assert path.exists()
        assert path.suffix == ".html"
        self.markdown: Path = path.with_suffix(".md")
        self.soup = BeautifulSoup(path.read_text(), features="html.parser")

    def parse(self) -> None:
        soup = self.soup.find_all("html")
        print(len(soup), type(soup))
        for i, tag in enumerate(soup):
            with open(f"/tmp/{i}.html", "w") as fout:
                fout.write(str(tag))


def main(input_html_file: Path) -> None:
    LawParser(input_html_file).parse()


typer.run(main)
