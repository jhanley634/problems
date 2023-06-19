# Copyright 2023 John Hanley. MIT licensed.
# An answer to https://stackoverflow.com/questions/76503323/format-a-string-to-have-same-spaces-as-another-string
import unittest


def insert_blanks(input, target):
    i = 0
    for tgt in target:
        if tgt == " ":
            yield " "
        else:
            yield input[i]
            i += 1


class InsertBlanksTest(unittest.TestCase):
    def test_insert_blanks(self):
        input = "abcabcabcabc"
        target = "foofoo foo fo o"
        self.assertEqual(
            "abcabc abc ab c",
            "".join(insert_blanks(input, target)),
        )
