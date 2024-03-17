#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291064/longest-spell-to-cast-from-pages-of-spellbook
import io


class Grimoire:
    def __init__(self, in_file: io.TextIOWrapper):
        n = int(in_file.readline())
        self.pages = [int(in_file.readline()) for _ in range(n)]

    def serialize(self) -> str:
        lines = list(map(str, self.pages))
        return "\n".join([f"{len(self.pages)}"] + lines) + "\n"

    def longest_spell(self) -> int:
        """Returns the longest spell that can be cast from the pages."""
        return len(self.pages)
