#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291086/longest-spell-to-cast-from-pages-of-spellbook-follow-up
import io

from graph_tool import Graph


class Grimoire:
    def __init__(self, in_file: io.TextIOWrapper):
        """Deserialize a graph, from its specified contest format.

        First line of text gives `n`, the number of nodes.
        Then we see `n` distinct 1-origin node names, each in the range 1 through n.
        """
        n = int(in_file.readline())
        pairs = [(i, int(in_file.readline()) - 1) for i in range(n)]
        self.g = Graph(g=pairs)

    def serialize(self) -> str:
        n = len(self.g)
        lines = [str(1 + self.g.vertex_index[self.g.vertex(i)]) for i in range(n)]
        return "\n".join([f"{n}"] + lines) + "\n"

    def longest_spell(self) -> int:
        """Returns the longest spell that can be cast from the pages of the grimoire."""
        return len(self.g)
