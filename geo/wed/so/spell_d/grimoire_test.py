#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from random import randint
import io
import unittest

from graph_tool.draw import graph_draw
from graph_tool.generation import random_graph

from geo.wed.so.spell_d.grimoire import Grimoire


def generate_grimoire(n: int = 2) -> Grimoire:
    pages = list(map(str, reversed(range(n))))
    return Grimoire(io.StringIO(f"{n}\n" + "\n".join(pages) + "\n"))


def gen_random_grimoire(n: int = 2) -> Grimoire:
    gr = generate_grimoire(n)
    gr.g = random_graph(n, deg_sampler=lambda: (1, 1))
    return gr


def generate_random_grimoire(n: int = 2) -> Grimoire:
    pages = list(range(1, n)) + [0]
    i = n // 3
    j = 2 * i
    shuffle_slice(pages, i, j)
    pages[j:] = sorted(pages[j:])
    pages[j:] = [pages[-1]] + pages[j:-1]
    print(pages)
    return Grimoire(io.StringIO(f"{n}\n" + "\n".join(map(str, pages)) + "\n"))


def shuffle_slice(a: list[int], start: int, end: int) -> None:
    for i in reversed(range(start + 1, end)):
        j = randint(start, i)
        a[i], a[j] = a[j], a[i]


class GrimoireTest(unittest.TestCase):
    def test_longest_spell(self) -> None:
        gen_random_grimoire()

        gr = generate_grimoire()
        self.assertEqual("2\n0\n1\n", gr.serialize())
        self.assertEqual(2, gr.longest_spell())

        gr = generate_grimoire(6)
        self.assertEqual(6, gr.longest_spell())

        gr = generate_random_grimoire(15)
        graph_draw(gr.g, output="/tmp/k/gr.png")
        self.assertEqual(15, gr.longest_spell())
