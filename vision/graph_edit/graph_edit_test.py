# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75038373/find-all-possible-modifications-to-a-graph
import unittest

from numpy.testing import assert_array_equal
import numpy as np

from .graph_edit import GraphEdit, all_double_mods, all_mods, all_single_mods, as_array


class GraphEditTest(unittest.TestCase):
    def setUp(self) -> None:
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

    def test_graph_edit(self) -> None:
        g = self.g
        self.assertEqual(5, self.g.num_nodes)
        self.assertEqual(2, g[0, 1])
        g[0, 1] = 3
        self.assertEqual(3, g[0, 1])
        del g.edit[(0, 1)]
        self.assertEqual(2, g[0, 1])

    def test_non_square(self) -> None:
        with self.assertRaises(AssertionError):
            GraphEdit(np.array([[0, 0], [1, 1], [2, 2]]))

    def test_all_single_mods(self) -> None:
        g = GraphEdit(np.array([[0, 0], [1, 0]]))

        self.assertEqual(4, len(list(all_single_mods(g))))

        expected = [
            np.array([[0, 1], [1, 0]]),
            np.array([[0, 2], [1, 0]]),
            np.array([[0, 0], [0, 0]]),
            np.array([[0, 0], [2, 0]]),
        ]

        for ex, actual in zip(
            expected,
            map(as_array, all_single_mods(g)),
        ):
            assert_array_equal(ex, actual)

            # Now verify that original graph is untouched.
            assert_array_equal(
                np.array([[0, 0], [1, 0]]),
                as_array(g),
            )

    def test_all_double_mods(self) -> None:
        g = GraphEdit(np.array([[0, 0], [1, 0]]))

        self.assertEqual(16, len(list(all_double_mods(g))))

        expected = [
            np.array([[0, 0], [1, 0]]),
            np.array([[0, 2], [1, 0]]),
            np.array([[0, 1], [0, 0]]),
            np.array([[0, 1], [2, 0]]),
            np.array([[0, 0], [1, 0]]),  # note the duplicate
            np.array([[0, 1], [1, 0]]),
            np.array([[0, 2], [0, 0]]),  # and it continues on in this vein
        ]

        for ex, actual in zip(
            expected,
            map(as_array, all_double_mods(g)),
        ):
            assert_array_equal(ex, actual)

    def test_many_mods(self) -> None:
        self.assertEqual(40, len(list(all_single_mods(self.g))))
        self.assertEqual(1_600, len(list(all_double_mods(self.g))))
        self.assertEqual(1_600, len(list(all_mods(self.g, 2))))
        self.assertEqual(64_000, len(list(all_mods(self.g, 3))))
        # self.assertEqual(2_560_000, len(list(all_mods(self.g, 4))))  # takes 16 seconds
