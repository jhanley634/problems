# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator

import numpy as np
import numpy.typing as npt


class GraphEdit:
    """A digraph with many base edge weights plus a handful of edited weights."""

    def __init__(
        self,
        edge: npt.NDArray[np.int_],
        edit: dict[tuple[int, int], int] | None = None,
        verify: bool = False,
    ) -> None:
        a, b = edge.shape
        assert a == b, f"Expected square matrix, got {a}x{b}"
        self.edge = edge  # We treat these as immutable weights.
        self.edit = edit or {}
        if verify:
            self._verify_no_self_loops()  # Changes the ctor cost from O(1) to O(n).

    def _verify_no_self_loops(self) -> None:
        for i in range(self.num_nodes):
            assert self[i, i] == 0, f"self-loop at node {i}"

    @property
    def num_nodes(self) -> int:
        return len(self.edge)

    def __getitem__(self, item: tuple[int, int]) -> int:
        return self.edit.get(item, self.edge[item])

    def __setitem__(self, item: tuple[int, int], value: int) -> None:
        self.edit[item] = value


def as_array(g: GraphEdit) -> npt.NDArray[np.int_]:
    return np.array([[g[i, j] for j in range(g.num_nodes)] for i in range(g.num_nodes)])


def all_single_mods(g: GraphEdit) -> Generator[GraphEdit]:
    """Generates all possible single-edge modifications to the graph."""
    orig_edit = g.edit.copy()
    for i in range(g.num_nodes):
        for j in range(g.num_nodes):
            if i == j:  # not an edge -- we don't support self-loops
                continue
            valid_weights = {0, 1, 2} - {g[i, j]}
            for w in sorted(valid_weights):
                yield GraphEdit(g.edge, {**orig_edit, (i, j): w})


def all_mods(g: GraphEdit, depth: int) -> Generator[GraphEdit]:
    assert depth >= 1
    if depth == 1:
        yield from all_single_mods(g)
    else:
        for gm in all_single_mods(g):
            yield from all_mods(gm, depth - 1)


def all_double_mods(g: GraphEdit) -> Generator[GraphEdit]:
    """Generates all possible double-edge modifications to the graph."""
    yield from all_mods(g, 2)
