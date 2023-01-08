# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75038373/find-all-possible-modifications-to-a-graph
import unittest

from numpy.testing import assert_array_equal
import numpy as np

from vision.graph_edit.graph_edit import GraphEdit, all_mods, as_array


class GraphEditTest(unittest.TestCase):
    def setUp(self):
        self.g = GraphEdit(
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

    def test_graph_edit(self):
        g = self.g
        self.assertEqual(5, self.g.num_nodes)
        self.assertEqual(2, g[0, 1])
        g[0, 1] = 3
        self.assertEqual(3, g[0, 1])
        del g.edit[(0, 1)]
        self.assertEqual(2, g[0, 1])

    def test_non_square(self):
        with self.assertRaises(AssertionError):
            GraphEdit(np.array([[0, 0], [1, 1], [2, 2]]))

    def test_all_mods(self):
        g = GraphEdit(np.array([[0, 0], [1, 0]]))
        assert_array_equal(
            np.array([[0, 0], [1, 0]]),
            as_array(g),
        )

        expected = [
            np.array([[0, 1], [1, 0]]),
            np.array([[0, 2], [1, 0]]),
            np.array([[0, 0], [0, 0]]),
            np.array([[0, 0], [2, 0]]),
        ]

        for ex, actual in zip(expected, map(as_array, all_mods(g))):
            assert_array_equal(ex, actual)
