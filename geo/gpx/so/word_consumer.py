#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from pathlib import Path
from time import sleep
from typing import Generator
import re

from sqlalchemy import text
from sqlalchemy.orm import Session
from tqdm import tqdm
import redis
import sqlalchemy as sa


def read_words(topic: str = "word-event") -> Counter[str]:
    id_re = re.compile(r"^\w+$")
    category: Counter[str]
    for cat, word in word_consumer(topic, category := Counter()):
        assert id_re.match(cat)
        assert id_re.match(word)

    return category


def word_consumer(
    topic: str,
    category: Counter[str],
    verbose: bool = False,
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
            if verbose:
                print(data.ljust(23), end="\t")
            if data == "request:  EOF":
                print("\nBye!")
                return
            cat, word = data.split(":")  # e.g. "item:     the"
            category[cat] += 1
            yield cat, word.lstrip()


def create_engine() -> sa.engine:
    DB_FILE = Path("/tmp/words.db")
    DB_URL = f"sqlite:///{DB_FILE}"
    return sa.create_engine(DB_URL)


def create_table() -> None:
    ddl = text(
        """
        CREATE TABLE  IF NOT EXISTS  word (
            id INTEGER PRIMARY KEY,
            category TEXT,
            word TEXT
        )"""
    )
    with Session(engine) as sess:
        sess.execute(ddl)


def populate_rows() -> None:
    ins = text("INSERT INTO word (category, word) VALUES (:cat, :word)")

    with Session(engine) as sess:
        category: Counter[str]
        for cat, word in tqdm(word_consumer("word-event", category := Counter())):
            sess.execute(ins, dict(cat=cat, word=word))
        sess.commit()
        print(len(category), category)


if __name__ == "__main__":
    engine = create_engine()
    create_table()
    populate_rows()
    # category = read_words()
    # assert 2 == len(category)
    # assert 58_470 == category["item"] == category["request"]
