#! /usr/bin/env python
from collections import namedtuple
from operator import attrgetter
import re

from networkx import Graph
from sortedcontainers import SortedList
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx


class Node(namedtuple("Node", "prefix, suffix, word")):
    ...


class WordLadder:
    def __init__(self, length: int = 3, words_file="/usr/share/dict/words"):
        letters_re = re.compile(r"^[a-zA-Z]+$")
        with open(words_file) as fin:
            self.words = {
                word.lower()
                for word in fin.read().splitlines()
                if len(word) == length and letters_re.match(word)
            }
        self.pfx_nodes = SortedList()
        self.sfx_nodes = SortedList(key=attrgetter("suffix"))
        for word in self.words:
            for i in range(len(word)):
                prefix = word[:i]
                suffix = word[i + 1 :]
                node = Node(prefix, suffix, word)
                self.pfx_nodes.add(node)
                self.sfx_nodes.add(node)
        self.g = self._create_graph()

    def _create_graph(self):
        g = Graph()
        for node in tqdm(self.pfx_nodes):
            g.add_node(node.word)
            i = self.pfx_nodes.bisect_left(node)
            j = self.sfx_nodes.bisect_left(node)
            assert self.pfx_nodes[i] == node
            assert self.sfx_nodes[j].suffix == node.suffix
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
        return g

    def find_path(self, start: str, end: str):
        p = nx.shortest_path(self.g, start, end)
        assert isinstance(p, list)
        return p

    def display_graph(self):
        self._display(self.g)

    def display_spanning_tree(self):
        self._display(nx.maximum_spanning_tree(self.g))

    @staticmethod
    def _display(graph):
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos, edge_color="grey", alpha=0.5)
        nx.draw_networkx_labels(graph, pos, font_size=16, font_family="sans-serif")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    WordLadder()
