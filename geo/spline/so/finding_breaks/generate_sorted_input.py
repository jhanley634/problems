#! /usr/bin/env python
# from https://stackoverflow.com/questions/79195892/most-efficient-way-to-get-unique-elements-from-sorted-list


from random import choices


def generate_sorted_values(n: int = 1_000_000, distinct_values: int = 12) -> list[int]:
    """Returns a sorted list of random non-negative integers."""
    population = range(distinct_values)
    xs = choices(population, k=n)
    return sorted(xs)


if __name__ == "__main__":
    print(generate_sorted_values(40))
