#! /usr/bin/env python
import re


class WordLadder:
    def __init__(self, length: int = 3, words_file="/usr/share/dict/words"):
        letters_re = re.compile(r"^[a-zA-Z]+$")
        with open(words_file) as fin:
            self.words = set(
                word.lower()
                for word in fin.read().splitlines()
                if len(word) == length and letters_re.match(word)
            )


if __name__ == "__main__":
    WordLadder()
