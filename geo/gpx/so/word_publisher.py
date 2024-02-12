#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from pathlib import Path
from typing import Generator
import io

from requests_cache import CachedSession
import redis

from geo.gpx.so.tokenizer_simple import get_simple_words


def get_words(url: str) -> Generator[str, None, None]:
    for line in get_document(url).lower().splitlines():
        for word in get_simple_words(line):
            yield word


def get_document(url: str, expire: int = 86400) -> str:
    session = CachedSession(cache_name="/tmp/requests_cache", expire_after=expire)
    return no_bom(session.get(url).text)


def no_bom(s: str) -> str:
    b = io.BytesIO(s.encode())
    with io.TextIOWrapper(b, encoding="utf-8-sig", newline="\r\n") as f:
        return f.read()
    # return s.lstrip("\ufeff")


def main(verbose: bool = False) -> None:
    tom = "https://www.gutenberg.org/ebooks/74.txt.utf-8"
    huck = "https://www.gutenberg.org/ebooks/76.txt.utf-8"

    assert 421_351 == len(get_document(tom))
    assert 602_756 == len(get_document(huck))

    tom_cnt = Counter(get_words(tom))
    assert 3_923 == tom_cnt["the"]

    huck_cnt = Counter(get_words(huck))
    assert 5_026 == huck_cnt["the"]

    if verbose:
        print(huck_cnt.most_common(8))


if __name__ == "__main__":
    main()
