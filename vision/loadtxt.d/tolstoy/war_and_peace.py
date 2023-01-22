#! /usr/bin/env python

# https://codereview.stackexchange.com/questions/282549/performant-text-file-reading-in-scheme
from pathlib import Path
from time import time

import requests

temp = Path("/tmp")
moby = "https://www.gutenberg.org/files/2701/2701-0.txt"


def read_war_and_peace(url="https://www.gutenberg.org/ebooks/2600.txt.utf-8"):
    cache = temp / Path(url).name
    if not cache.exists():
        resp = requests.get(url)
        cache.write_text(resp.text)
    print(cache.stat().st_size)
    with open(cache) as fin:
        return fin.read()


if __name__ == "__main__":
    t0 = time()
    print(len(read_war_and_peace()), time() - t0)
