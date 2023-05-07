from inspect import cleandoc
import unittest

from geo.zone.outline_parser import OutlineParser


class TestOutlineParser(unittest.TestCase):
    def test_parse(self) -> None:
        lines = cleandoc(
            """
        1. one
            a. apple
                i. Granny
                ii. Delicious
            b. banana
        2. two
        """
        ).splitlines()
        print(lines)
        self.assertEqual(4, len(list(OutlineParser(lines))))
