# Copyright 2023 John Hanley. MIT licensed.
from collections import defaultdict
from functools import partial
from io import StringIO
from typing import Generator, List, Set, TextIO, Tuple

from sortedcontainers import SortedList

from geo.ski.word_ladder import hamming_distance


class WordLadder:
    def __init__(self, length: int = 3, input_words="/usr/share/dict/words"):
        self.length = length
        self.words: defaultdict[int, Set[int]] = defaultdict(set)
        if isinstance(input_words, str):
            with open(input_words) as fin:
                self.vocabulary = sorted(self._read_words(fin))
        else:
            self.vocabulary = sorted(self._read_words(StringIO("\n".join(input_words))))

    def _read_words(self, fin: TextIO) -> Generator[str, None, None]:
        for line in map(str.rstrip, fin):
            if len(line) == self.length and line.isalpha():
                word = line.lower()
                yield word

    def word_str(self, n: int) -> str:
        return self.vocabulary[n // self.length]

    def prototype_str(self, n: int) -> str:
        w = self.word_str(n)
        j = n % self.length
        return f"{w[:j]}_{w[j:]}"

    def hamming_distance(self, a: int, b: int) -> int:
        w_a = self.word_str(a)
        w_b = self.word_str(b)
        return sum(x != y for x, y in zip(w_a, w_b))

    def _gen_prototypes(self, word: int) -> Generator[int, None, None]:
        for j in range(self.length):
            yield word + j

    def find_path(self, start: str, end: str) -> List[str]:
        def as_int(s: str) -> int:
            return self.vocabulary.index(s) * self.length

        paths = sorted(self.bfs_paths(as_int(start), as_int(end)), key=len) + [[]]
        return paths[0]

    def bfs_paths(self, start: int, end: int) -> Generator[List[int], None, None]:
        """Generates candidate acyclic paths from start to end."""
        assert self.word_str(start).isalpha()
        assert self.word_str(end).isalpha()
        positive_infinity = 999
        best: defaultdict[int, int] = defaultdict(lambda: positive_infinity)
        queue = [(start, [start])]
        while queue:
            node, path = queue.pop(0)
            for prototype in self._gen_prototypes(node):
                for word in self._ordered(
                    self._adjacent_words(set([prototype]) - set(path), end), end
                ):
                    if word == end:
                        yield path + [end]
                    elif best[word] > len(path):
                        best[word] = len(path)
                        queue.append((word, path + [word]))

    def _adjacent_words(self, proto: int, end: int) -> Set[int]:
        return []
        if False:
            while (
                i < len(self.pfx_nodes)
                and self.pfx_nodes[i].prefix == node.prefix
                and j < len(self.sfx_nodes)
                and self.sfx_nodes[j].suffix == node.suffix
            ):
                other = self.pfx_nodes[i]
                i += 1
                j += 1
                if other.word == node.word:
                    continue
                if other.prefix == node.prefix and other.suffix == node.suffix:
                    g.add_node(other.word)
                    g.add_edge(other.word, node.word)

    def _is_adjacent(self, a: int, b: int) -> bool:
        assert a % self.length == 0
        assert b % self.length == 0

    def _ordered(self, neighbors: Set[int], end: int) -> List[int]:
        distance_to_goal = partial(hamming_distance, end)
        return sorted(sorted(neighbors), key=distance_to_goal)
