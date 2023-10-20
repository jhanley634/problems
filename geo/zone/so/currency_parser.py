# Copyright 2023 John Hanley. MIT licensed.
#
# from https://stackoverflow.com/questions/77333261/make-a-string-cleaner-in-python


import re
import unittest

from bs4 import BeautifulSoup, Tag


class TestCurrencyParser(unittest.TestCase):
    def test_parse(self):
        doc1 = """
<span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
 <span>
  11 €
 </span>
 <span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
  <span>
   20 €
  </span>
 </span>
 <span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
  <span>
   10 500 €
  </span>
 </span>
</span>
"""
        # and now let's try that again, this time properly nested:
        doc2 = """
<span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
 <span>
  11 €
 </span>
</span>
<span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
 <span>
  20 €
 </span>
</span>
<span class="sc-7ebdc9db-1 dAVCtE _137P- _35DXM P4PEa" data-qa-id="aditem_price">
 <span>
  10 500 €
 </span>
</span>
"""
        class_sc_re = re.compile(r"^sc-7ebd.*")
        inputs = [
            (doc1, [34, 4, 8]),  # initial entry is too long, due to unfortunate nesting
            (doc2, [4, 4, 8]),  # proper nesting yields sensible currency figures
        ]
        for doc, expected in inputs:
            soup = BeautifulSoup(doc, "html.parser")
            spans = soup.find_all("span", class_=class_sc_re)
            self.assertEqual(expected, list(map(get_span_text_length, spans)))


def get_span_text_length(tag: Tag) -> int:
    assert isinstance(tag, Tag)
    assert tag.name == "span"

    s = tag.text.strip()
    assert s.endswith("€")

    return len(s)
