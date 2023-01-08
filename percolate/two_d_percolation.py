
# Copyright 2021 John Hanley. MIT licensed.
import matplotlib.pyplot as plt
import networkit as nk
import numpy as np


class Perc:
    """A percolation graph."""
    # (or, a percolation matrix, if you prefer, given the Manhattan layout)

    def __init__(self, width=6, height=5):
        self.width = width
        self.height = height
        self.g = self._get_initial_graph()

    def node_num(self, x, y):
        if (0 <= x < self.width
                and 0 <= y < self.height):
            return self.width * y + x
        raise ValueError(f'({x}, {y}) is out of bounds')

    # https://en.wikipedia.org/wiki/Von_Neumann_neighborhood
    cardinal_directions = [  # N, E, S, W
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    def _node_nbrhd(self, x, y):
        for nx, ny, *_ in self._x_y_nbrhd(x, y):
            yield self.node_num(nx, ny)

    def _x_y_nbrhd(self, x, y):
        for dx, dy in self.cardinal_directions:
            # Valid point? Or did we wander out of bounds?
            # Edge nodes only have 3 nbrs, corners have just 2.
            if (0 <= x + dx < self.width
                    and 0 <= y + dy < self.height):
                yield x + dx, y + dy, dx, dy

    def _get_initial_nodes(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def _get_initial_graph(self):
        g = nk.Graph(n=self.width * self.height)
        for x, y in self._get_initial_nodes():
            node_a = self.node_num(x, y)
            for node_b in self._node_nbrhd(x, y):
                if not g.hasEdge(node_a, node_b):
                    g.addEdge(node_a, node_b)
        return g

    def plot(self, alpha=0.1):
        x = []
        y = []
        edge_x = []
        edge_y = []
        for px, py in self._get_initial_nodes():
            x.append(px)
            y.append(py)
            # Compare current Point with Neighbor.
            for nx, ny, dx, dy in self._x_y_nbrhd(px, py):
                if self.g.hasEdge(
                        self.node_num(px, py),
                        self.node_num(nx, ny)):

                    edge_x.append(px + alpha * dx)
                    edge_x.append(nx - alpha * dx)
                    edge_y.append(py + alpha * dy)
                    edge_y.append(ny - alpha * dy)

                    # Now declare a discontinuity between line segments.
                    edge_x.append(np.nan)
                    edge_y.append(np.nan)

        fig, ax = plt.subplots()
        plt.plot(x, y, 'o')
        plt.plot(edge_x, edge_y)
        # return fig, ax
