#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/a/294876

import heapq
import random
import timeit

import matplotlib.pyplot as plt
import numpy as np


def heap_sort_custom(lst):
    """
    Performs a custom heap sort iterative algorithm without changing the size of the heap. Unlike in standard heap sort, no extractions are performed

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

    orig_input = lst.copy()
    heapq.heapify(lst)  # Build a min-heap from input list

    # A set to keep track of visited indices
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

    assert sorted_result == sorted(orig_input)
    return sorted_result


def sort_using_heap(arr):
    heapq.heapify(arr)
    result = []
    while arr:
        result.append(heapq.heappop(arr))
    return result


def heapsort(arr):
    def sift_down(arr, n, i):
        elem = arr[i]
        while True:
            l = 2 * i + 1
            if l >= n:
                arr[i] = elem
                return
            r = 2 * i + 2
            c = l
            if r < n and arr[l] < arr[r]:
                c = r
            if elem >= arr[c]:
                arr[i] = elem
                return
            arr[i] = arr[c]
            i = c

    n = len(arr)
    for i in range(n // 2, -1, -1):
        sift_down(arr, n, i)
    for i in range(n - 1, 0, -1):
        t = arr[i]
        arr[i] = arr[0]
        arr[0] = t
        sift_down(arr, i, 0)
    return arr


def nsmallest(arr):
    heapq.heapify(arr)
    return heapq.nsmallest(len(arr), arr)


def makedata(n):
    res = list(range(n))
    random.seed(a=n)
    random.shuffle(res)
    return res


def sample(n, fn):
    data = makedata(n)
    assert fn(data.copy()) == sorted(data)
    return timeit.timeit(lambda: fn(data[:]), number=10)


def plot(ax, a, fn, color):
    ax.plot([sample(n, fn) for n in a], color=color, label=fn.__name__)


def main() -> None:
    a = [pow(2, i) for i in range(1, 17)]
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)

    for color, fn in [
        ("blue", heap_sort_custom),
        ("red", heapsort),
        ("green", sort_using_heap),
        ("purple", nsmallest),
        ("orange", sorted),
    ]:
        plot(ax, a, fn, color)

    ax.set_yscale("log")
    ax.set_xscale("log")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
