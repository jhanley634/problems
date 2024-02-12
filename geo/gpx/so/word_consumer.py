#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from time import sleep

import redis


def word_consumer(topic: str = "word-event") -> Counter[str]:
    ps = redis.Redis().pubsub()
    ps.subscribe(topic)
    sleep(0.010)
    assert ps.get_message()["type"] == "subscribe"

    category: Counter[str] = Counter()
    while True:
        msg = ps.get_message(timeout=0.1)
        if msg:
            assert msg["type"] in ("message", "subscribe")
            assert msg["pattern"] is None
            assert msg["channel"].decode() == topic

            data = msg["data"].decode()
            print(data.ljust(23), end="\t")
            if data == "request:  EOF":
                print("\nBye!")
                return category
            cat, word = data.split(":")
            category[cat] += 1


if __name__ == "__main__":
    category = word_consumer()
    assert 2 == len(category)
    assert 58_470 == category["item"] == category["request"]
