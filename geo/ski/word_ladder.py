from collections import defaultdict
from functools import partial
from typing import Generator, List, Set, TextIO, Tuple


def hamming_distance(a: str, b: str) -> int:
    # https://en.wikipedia.org/wiki/Hamming_distance
    assert len(a) == len(b)
    return sum(x != y for x, y in zip(a, b))


class Word(str):
    def __init__(self, word: str):
        assert word.isalpha(), word
        super().__init__()


class WordLadder:
    def __init__(self, length: int = 3, words_file="/usr/share/dict/words"):
        self.words: defaultdict[str, Set[Word]] = defaultdict(set)
        with open(words_file) as fin:
            for prototype, word in sorted(self._read_words(length, fin)):
                assert "_" in prototype
                self.words[prototype].add(word)

    @classmethod
    def _read_words(
        cls, length: int, fin: TextIO
    ) -> Generator[Tuple[str, Word], None, None]:

        for line in map(str.rstrip, fin):
            if len(line) == length and line.isalpha():
                word = Word(line.lower())
                for prototype in cls._gen_prototypes(word):
                    yield prototype, word

    @staticmethod
    def _gen_prototypes(word: Word) -> Generator[str, None, None]:

        for i in range(len(word)):
            prefix = word[:i]
            suffix = word[i + 1 :]
            yield f"{prefix}_{suffix}"

    def find_path(self, start: Word, end: Word) -> List[Word]:
        paths = sorted(self.bfs_paths(start, end), key=len) + [[]]
        return paths[0]

    def bfs_paths(self, start: Word, end: Word) -> Generator[List[Word], None, None]:
        """Generates candidate acyclic paths from start to end."""
        assert start.isalpha()
        assert end.isalpha()
        POSITIVE_INFINITY = 999
        best: defaultdict[str, int] = defaultdict(lambda: POSITIVE_INFINITY)
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
    def _ordered(neighbors: Set[Word], end: Word) -> List[Word]:
        distance_to_goal = partial(hamming_distance, end)
        return sorted(sorted(neighbors), key=distance_to_goal)
