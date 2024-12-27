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
  result = []

  # Start traversal from the root of the heap
  current_index = 0  

  while len(result) < len(lst):
    if current_index not in visited_indices:
      # Add the current node's value to the result and mark it as visited
      result.append(lst[current_index])
      visited_indices.add(current_index)
    # Replace the current node value with value of either left, right or parent node
    if parent(current_index) < min(left_child(current_index), right_child(current_index)):
      lst[current_index] = min(left_child(current_index), right_child(current_index))
      current_index = (current_index - 1) // 2  # Move to the parent node
    elif left_child(current_index) < right_child(current_index):
      lst[current_index] = min(right_child(current_index), parent(current_index))
      current_index = 2 * current_index + 1  # Move to the left child
    else:
      lst[current_index] = min(left_child(current_index), parent(current_index))
      current_index = 2 * current_index + 2  # Move to the right child

  return result