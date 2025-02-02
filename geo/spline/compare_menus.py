#! /usr/bin/env python

from pathlib import Path
import io
import re

import pdftotext
import requests

temp = Path("/tmp/menu")


dining = "https://www.palisadestahoe.com/-/media/palisades-tahoe/pdfs/dining"
urls = [
    dining
    + "/rocker-brunch-2425.pdf?rev=5fc1fbfbb77b4762b082fc6f2f61d9c4&hash=8BD85290FC47D250EAD86521A404F9CE",
    dining
    + "/rocker-lunch-2425-(2).pdf?rev=3ed7b5d7e94d41d488d29773422f49af&hash=429FC56D0F58CB6D05C35F3967164228",
    dining
    + "/rocker-dinner-2425-(2).pdf?rev=81707816d5164e1db5aa67fcfaaa6031&hash=8F45357D16DA78887A8559EA682C8366",
]


def main() -> None:
    temp.mkdir(exist_ok=True)
    if not (temp / "dinner.txt").exists():
        _fetch_menus()


def _fetch_menus() -> None:
    for url in urls:
        out_file = _get_out_file(url)
        response = requests.get(url)
        with open(out_file, "wb") as f:
            f.write(response.content)

        pdf = pdftotext.PDF(io.BytesIO(response.content))
        print(len(pdf), out_file)
        with open(out_file.with_suffix(".txt"), "w") as f:
            f.write("\n\n".join(pdf))


def _get_out_file(url: str) -> Path:
    pat = re.compile(r"pdfs/dining/rocker-(\w+)-2425")

    m = pat.search(url)
    assert m

    name = m.group(1)
    return temp / f"{name}.pdf"


if __name__ == "__main__":
    main()
