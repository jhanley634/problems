#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import numpy as np


class GraphEdit:
    """A digraph with many base edge weights plus a handful of edited weights."""

    def __init__(self, edge: np.ndarray):
        a, b = edge.shape
        assert a == b, f"Expected square matrix, got {a}x{b}"
        self.edge = edge  # We treat these as immutable weights.
        self.edit = {}
        self._verify_no_self_loops()

    def _verify_no_self_loops(self):
        for i in range(self.num_nodes):
            assert self[i, i] == 0, f"self-loop at node {i}"

    @property
    def num_nodes(self):
        return len(self.edge)

    def __getitem__(self, item):
        return self.edit.get(item, self.edge[item])

    def __setitem__(self, item, value):
        self.edit[item] = value


def as_array(g: GraphEdit) -> np.ndarray:
    return np.array([[g[i, j] for j in range(g.num_nodes)] for i in range(g.num_nodes)])


def all_mods(g: GraphEdit):
    """Generates all possible single-edge modifications to the graph."""
    orig_edit = g.edit.copy()
    for i in range(g.num_nodes):
        for j in range(g.num_nodes):
            if i == j:  # not an edge -- we don't support self-loops
                continue
            valid_weights = {0, 1, 2} - {g[i, j]}
            for w in valid_weights:
                g.edit = {**orig_edit, (i, j): w}
                yield g
    g.edit = orig_edit
