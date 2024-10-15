#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291086/longest-spell-to-cast-from-pages-of-spellbook-follow-up
import io

from graph_tool import Graph, topology


class Grimoire:
    def __init__(self, in_file: io.TextIOWrapper) -> None:
        """Deserialize a graph.

        First line of text gives `n`, the number of nodes.
        Then we see `n` distinct 0-origin node names, each in the range 0 through n-1.
        """
        n = int(in_file.readline())
        pairs = [(i, int(in_file.readline())) for i in range(n)]
        self.g = Graph(g=pairs)

    def serialize(self) -> str:
        n = len(self.g)
        lines = [str(self.g.vertex_index[self.g.vertex(i)]) for i in range(n)]
        return "\n".join([f"{n}"] + lines) + "\n"

    def longest_spell(self) -> int:
        """Returns the longest spell that can be cast from the pages of the grimoire."""
        for c in topology.all_circuits(self.g):
            print(c)
        return len(self.g)
