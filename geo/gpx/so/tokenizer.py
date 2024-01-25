#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/289102/tokenize-a-file

from collections import Counter
from pathlib import Path
from pprint import pp
from typing import TextIO

import spacy
import spacy.tokens
import typer


def spacy_wordlist(fin: TextIO) -> None:
    nlp = spacy.load("en_core_web_sm")
    seen = set()
    cnt = Counter()

    for line in fin:
        doc = (word for word in nlp(line.lower().strip()) if word.is_alpha)

        for token in doc:
            cnt[token.text] += 1
            if token.text not in seen:
                seen.add(token.text)
                print(token.text)

    print("\n".join(sorted(seen)))
    pp(cnt)


def main(in_file: Path) -> None:
    with open(in_file) as fin:
        spacy_wordlist(fin)


if __name__ == "__main__":
    typer.run(main)
