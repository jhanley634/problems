#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import io
import unittest

from geo.wed.so.spell_d.grimoire import Grimoire


def generate_grimoire() -> Grimoire:
    return Grimoire(io.StringIO("1\n1\n"))


class GrimoireTest(unittest.TestCase):
    def test_longest_spell(self) -> None:
        g = generate_grimoire()
        self.assertEqual("1\n1\n", g.serialize())
        self.assertEqual(1, g.longest_spell())
