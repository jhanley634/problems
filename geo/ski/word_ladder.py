#! /usr/bin/env python
from collections import namedtuple
import re

from sortedcontainers import SortedList


class Node(namedtuple("Node", "prefix, suffix, word")):
    ...


class WordLadder:
    def __init__(self, length: int = 3, words_file="/usr/share/dict/words"):
        letters_re = re.compile(r"^[a-zA-Z]+$")
        with open(words_file) as fin:
            self.words = set(
                word.lower()
                for word in fin.read().splitlines()
                if len(word) == length and letters_re.match(word)
            )
        self.nodes = SortedList()
        for word in self.words:
            for i in range(len(word)):
                prefix = word[:i]
                suffix = word[i + 1 :]
                self.nodes.add(Node(prefix, suffix, word))


if __name__ == "__main__":
    WordLadder()
