# Copyright 2023 John Hanley. MIT licensed.
from collections import defaultdict
from collections.abc import Generator
from functools import partial
from io import StringIO
from typing import TextIO


def hamming_distance(a: str, b: str) -> int:
    # https://en.wikipedia.org/wiki/Hamming_distance
    assert len(a) == len(b)
    return sum(x != y for x, y in zip(a, b))


class Word(str):
    def __init__(self, word: str):
        assert word.isalpha(), word
        super().__init__()


class Proto(str):
    """A prototype word, with exactly one "_" underscore wildcard."""

    def __init__(self, text: str):
        assert "_" in text, text
        assert text.count("_") == 1
        assert text.replace("_", "").isalpha()
        super().__init__()


class WordLadder:
    def __init__(
        self,
        length: int = 3,
        input_words: list[str] | str = "/usr/share/dict/words",
    ):
        self.words: defaultdict[Proto, set[Word]] = defaultdict(set)
        if isinstance(input_words, str):
            with open(input_words) as fin:
                self._store_sorted_words(length, fin)
        else:
            self._store_sorted_words(length, StringIO("\n".join(input_words)))

    def _store_sorted_words(self, length: int, fin: TextIO) -> None:
        for prototype, word in sorted(self._read_words(length, fin)):
            self.words[prototype].add(word)

    @classmethod
    def _read_words(
        cls, length: int, fin: TextIO
    ) -> Generator[tuple[Proto, Word], None, None]:
        for line in map(str.rstrip, fin):
            if len(line) == length and line.isalpha():
                word = Word(line.lower())
                for prototype in cls._gen_prototypes(word):
                    yield prototype, word

    @staticmethod
    def _gen_prototypes(word: Word) -> Generator[Proto, None, None]:
        for i in range(len(word)):
            prefix = word[:i]
            suffix = word[i + 1 :]
            yield Proto(f"{prefix}_{suffix}")

    def find_path(self, start: Word | str, end: Word | str) -> list[Word]:
        paths = sorted(self.bfs_paths(Word(start), Word(end)), key=len) + [[]]
        return paths[0]

    def bfs_paths(self, start: Word, end: Word) -> Generator[list[Word], None, None]:
        """Generates candidate acyclic paths from start to end."""
        assert start.isalpha()
        assert end.isalpha()
        positive_infinity = 999
        best: defaultdict[str, int] = defaultdict(lambda: positive_infinity)
        queue = [(start, [start])]
        while queue:
            node, path = queue.pop(0)
            for prototype in self._gen_prototypes(node):
                for word in self._ordered(self.words[prototype] - set(path), end):
                    if word == end:
                        yield path + [end]
                    elif best[word] > len(path):
                        best[word] = len(path)
                        queue.append((word, path + [word]))

    @staticmethod
    def _ordered(neighbors: set[Word], end: Word) -> list[Word]:
        distance_to_goal = partial(hamming_distance, end)
        return sorted(sorted(neighbors), key=distance_to_goal)
