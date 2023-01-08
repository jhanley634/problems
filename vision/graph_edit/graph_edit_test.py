# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75038373/find-all-possible-modifications-to-a-graph
import unittest

import numpy as np

from vision.graph_edit.graph_edit import GraphEdit


class GraphEditTest(unittest.TestCase):
    def test_graph_edit(self):
        g = GraphEdit(
            np.array(
                [
                    [0, 2, 1, 2, 0],
                    [1, 0, 1, 0, 0],
                    [0, 2, 0, 0, 0],
                    [1, 0, 1, 0, 2],
                    [1, 2, 0, 0, 0],
                ],
                dtype=np.uint8,
            )
        )
        self.assertEqual(2, g[0, 1])
        g[0, 1] = 3
        self.assertEqual(3, g[0, 1])
        del g.edit[(0, 1)]
        self.assertEqual(2, g[0, 1])

        print(g.edge.dtype)
