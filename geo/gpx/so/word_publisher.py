#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from operator import itemgetter
from pathlib import Path
from time import time
from typing import Generator
import io
import json
import re

from requests_cache import CachedSession
import redis

from geo.gpx.so.tokenizer_simple import get_simple_words


def get_words(url: str) -> Generator[str, None, None]:
    for line in get_document(url).lower().splitlines():
        for word in get_simple_words(line):
            yield word


def get_document(url: str, expire: int = 86400) -> str:
    session = CachedSession(cache_name="/tmp/requests_cache", expire_after=expire)
    return no_bom(dumb_quotes(session.get(url).text))


def no_bom(s: str) -> str:
    b = io.BytesIO(s.encode())
    with io.TextIOWrapper(b, encoding="utf-8-sig", newline="\r\n") as f:
        return f.read()
    # return s.lstrip("\ufeff")


def dumb_quotes(s: str) -> str:
    clean = str.maketrans(
        "™_—éê•",
        "  -ee*",
    )
    single = re.compile("[‘’]")
    double = re.compile("[“”]")
    return double.sub('"', single.sub("'", s)).translate(clean)


def main() -> None:
    tom = "https://www.gutenberg.org/ebooks/74.txt.utf-8"
    huck = "https://www.gutenberg.org/ebooks/76.txt.utf-8"

    assert 421_351 == len(get_document(tom))
    assert 602_756 == len(get_document(huck))
    assert 8_002 == get_document(tom).index('"Tom!"')

    both = words_in_common(
        Counter(get_words(tom)),
        Counter(get_words(huck)),
    )
    publish(both, tom, huck)


def publish(both: Counter[str], tom: str, huck: str, topic: str = "word-event") -> None:
    # This takes 13.6 seconds to publish, or .250 msec ignoring redis.

    r = redis.Redis()
    tom_cnt = both.copy()
    huck_cnt = both.copy()
    t0 = time()
    print("Publishing...")
    assert tom_cnt["xyzzy"] == 0

    for word in get_words(tom):
        if tom_cnt[word] > 0:
            tom_cnt[word] -= 1
            r.publish(topic, word)

    for word in get_words(huck):
        if huck_cnt[word] > 0:
            huck_cnt[word] -= 1
            r.publish(topic, word)

    print(f"elapsed: {time()-t0:.3f} sec")


def words_in_common(tom_cnt: Counter[str], huck_cnt: Counter[str]) -> Counter[str]:
    assert 3_985 == tom_cnt["the"]
    assert 3_190 == tom_cnt["and"]
    assert 7_528 == len(tom_cnt)

    assert 5_101 == huck_cnt["the"]
    assert 6_440 == huck_cnt["and"]
    assert 6_363 == len(huck_cnt)

    both = Counter(
        {
            word: min(tom_cnt[word], huck_cnt[word])
            for word in (tom_cnt.keys() & huck_cnt.keys())
        }
    )
    # Now finesse the sort order, popular first then finally
    # alphabetic hapax legomena, exploiting stable sort.
    both = Counter({k: v for k, v in sorted(both.items(), key=itemgetter(1, 0))})
    both = Counter(
        {k: v for k, v in sorted(both.items(), key=itemgetter(1), reverse=True)}
    )
    assert 3_594 == len(both)
    assert tom_cnt["the"] == both["the"]
    assert tom_cnt["and"] == both["and"]

    with open(Path("/tmp/both.json"), "w") as fout:
        json.dump(both, fout, indent=2)
    return both


if __name__ == "__main__":
    main()
