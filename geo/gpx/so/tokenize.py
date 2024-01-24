#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/289102/tokenize-a-file

from collections import Counter
from sys import stdin
import inspect
import pprint

import spacy


def spacy_wordlist() -> None:
    nlp = spacy.load("en_core_web_sm")
    seen = set()
    cnt = Counter()

    for line in stdin:
        doc = (word for word in nlp(line.strip()) if word.is_alpha)

        for token in doc:
            cnt[token.text] += 1
            if token.text not in seen:
                seen.add(token.text)
                print(token.text)

    pprint.pp(cnt)


if __name__ == "__main__":
    spacy_wordlist()
