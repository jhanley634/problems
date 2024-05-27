# Copyright 2023 John Hanley. MIT licensed.
# An answer to https://stackoverflow.com/questions/76503323/format-a-string-to-have-same-spaces-as-another-string
from collections.abc import Generator
import unittest


def insert_blanks(input: str, target: str) -> Generator[str, None, None]:
    i = 0
    for tgt in target:
        if tgt == " ":
            yield " "
        else:
            yield input[i]
            i += 1


class InsertBlanksTest(unittest.TestCase):
    def test_insert_blanks(self) -> None:
        text = "abcabcabcabc"
        target = "foofoo foo fo o"
        self.assertEqual(
            "abcabc abc ab c",
            "".join(insert_blanks(text, target)),
        )
