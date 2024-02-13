#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from time import sleep
from typing import Generator
import re

import redis


def read_words(topic: str = "word-event") -> Counter[str]:
    id_re = re.compile(r"^\w+$")
    for cat, word in word_consumer(topic, category := Counter()):
        assert id_re.match(cat)
        assert id_re.match(word)

    return category


def word_consumer(
    topic: str, category: Counter[str]
) -> Generator[tuple[str, str], None, None]:
    ps = redis.Redis().pubsub()
    ps.subscribe(topic)
    sleep(0.010)
    assert ps.get_message()["type"] == "subscribe"

    while True:
        msg = ps.get_message(timeout=0.1)
        if msg and msg["type"] == "message":
            # assert msg["pattern"] is None
            # assert msg["channel"].decode() == topic

            data = msg["data"].decode()
            print(data.ljust(23), end="\t")
            if data == "request:  EOF":
                print("\nBye!")
                return
            cat, word = data.split(":")  # e.g. "item:     the"
            category[cat] += 1
            yield cat, word.lstrip()


if __name__ == "__main__":
    category = read_words()
    assert 2 == len(category)
    assert 58_470 == category["item"] == category["request"]
