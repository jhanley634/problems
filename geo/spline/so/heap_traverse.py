#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/294859/traversal-heap-sort-no-extractions

import heapq


def heap_sort(lst):
    """
    Performs a heap sort iteratively by traversing all nodes of the heap, visiting nodes with smaller values first and adding the values to sorted result list.

    Args:
      lst (list): The input list to be sorted.
    Returns:
      list: A sorted list containing elements of the input list in ascending order.

    Approach:
    - Convert the input list into a min-heap
    - Traverse and process the heap iteratively:
      - Maintain a set to track indices that have already been processed.
      - Replace the value at the current node with the value of either the left child, right child or parent, depending on specific conditions.
    - Accumulate results in a separate list as each node is processed.
    """

    def left_child(i):
        """
        Returns the value of the left child of the node at index i, or infinity if out of bounds.
        """
        return float("inf") if 2 * i + 1 >= len(lst) else lst[2 * i + 1]

    def right_child(i):
        """
        Returns the value of the right child of the node at index i, or infinity if out of bounds.
        """
        return float("inf") if 2 * i + 2 >= len(lst) else lst[2 * i + 2]

    def parent(i):
        """
        Returns the value of parent of the node at index i, or infinity if the node is the root.
        """
        return lst[(i - 1) // 2] if i > 0 else float("inf")

    heapq.heapify(lst)  # Build a min-heap from input list

    # A set to keep track of visited indices (nodes)
    visited_indices = set()

    # List to store the sorted result
    sorted_result = []

    # Start traversal from the root of the heap
    j = 0

    while len(sorted_result) < len(lst):

        if j not in visited_indices:
            # Add the current node's value to the result and mark it as visited
            sorted_result.append(lst[j])
            visited_indices.add(j)

        # Replace the current node value with value of either left, right or parent node
        if parent(j) < min(
            left_child(j),
            right_child(j),
        ):
            lst[j] = min(
                left_child(j),
                right_child(j),
            )
            j = (j - 1) // 2  # Move to the parent node
        elif left_child(j) < right_child(j):
            lst[j] = min(
                right_child(j),
                parent(j),
            )
            j = 2 * j + 1  # Move to the left child
        else:
            lst[j] = min(
                left_child(j),
                parent(j),
            )
            j = 2 * j + 2  # Move to the right child

    return sorted_result
