#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import io
import unittest

from geo.wed.so.spell_d.grimoire import Grimoire


def generate_grimoire(n: int = 2) -> Grimoire:
    nums = reversed(range(1, n + 1))
    pages = map(str, nums)
    return Grimoire(io.StringIO(f"{n}\n" + "\n".join(pages) + "\n"))


class GrimoireTest(unittest.TestCase):
    def test_longest_spell(self) -> None:
        g = generate_grimoire()
        self.assertEqual("2\n1\n2\n", g.serialize())
        self.assertEqual(2, g.longest_spell())
