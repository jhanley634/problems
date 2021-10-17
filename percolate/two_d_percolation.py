
import networkit as nk


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
            return self.height * y + x
        raise ValueError(f'({x}, {y}) is out of bounds')

    # https://en.wikipedia.org/wiki/Von_Neumann_neighborhood
    cardinal_directions = [  # N, E, S, W
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    def _nbrhd(self, x, y):
        for dx, dy in self.cardinal_directions:
            try:
                yield self.node_num(x + dx, y + dy)
            except ValueError:
                pass  # edge nodes only have 3 nbrs, corners have just 2

    def _get_initial_nodes(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def _get_initial_graph(self):
        g = nk.Graph(n=self.width * self.height)
        for x, y in self._get_initial_nodes():
            node_a = self.node_num(x, y)
            for node_b in self._nbrhd(x, y):
                g.addEdge(node_a, node_b)  # We add each edge twice, but that's OK.
