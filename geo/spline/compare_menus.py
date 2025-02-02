#! /usr/bin/env python

from pathlib import Path
import re

import requests

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
    temp = Path("/tmp/menu")
    temp.mkdir(exist_ok=True)
    pat = re.compile(r"pdfs/dining/rocker-(\w+)-2425")
    for url in urls:
        m = pat.search(url)
        assert m
        name = m.group(1)
        out_file = temp / f"{name}.pdf"
        print(out_file)
        response = requests.get(url)
        with open(out_file, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    main()
