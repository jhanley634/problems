#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import numpy as np


class GraphEdit:
    """A digraph with many base edge weights plus a handful of edited weights."""

    def __init__(self, edge: np.ndarray):
        a, b = edge.shape
        assert a == b, f"Expected square matrix, got {a}x{b}"
        self.edge = edge
        self.edit = {}

    def __getitem__(self, item):
        return self.edit.get(item, self.edge[item])

    def __setitem__(self, item, value):
        self.edit[item] = value
