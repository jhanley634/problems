# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from pprint import pp
import re
import unittest

from datasets import Dataset, load_dataset
from html2text import html2text
from huggingface_hub import hf_hub_download
import requests

from gen.news_summary import Summarizer, get_cache_filespec


def _remove(pattern: str, subst: str, s: str, flags: int = re.NOFLAG) -> str:
    t = re.sub(pattern, subst, s, flags=flags)

    # If regex failed to match, then say so.
    # if not len(t) < len(s):
    #    print(s)
    # assert len(t) < len(s), (len(t), len(s), pattern)

    return t


_default_url = (
    "https://web.archive.org/web/20211202143633"
    "/https://www.newsweek.com/americas-most-responsible-companies-2022"
)


def get_article_text_file(url: str = _default_url) -> Path:
    html_fspec = get_cached_html_file(url)
    text = html2text(html_fspec.read_text())
    text = _remove(r"^[\s\S]+ Comments\n\n## ", "", text)
    text = _remove(r"Nancy Cooper.+$", "", text, flags=re.DOTALL).strip()
    base = html_fspec.stem
    txt_fspec = Path(f"/tmp/{base}.txt")
    txt_fspec.write_text(text)
    return txt_fspec


def get_cached_html_file(url: str, verbose: bool = False) -> Path:
    fspec = Path(get_cache_filespec(url))
    if not fspec.exists():
        ua = "Wget/1.21.4"
        resp = requests.get(url, headers={"User-Agent": ua})
        resp.raise_for_status()
        ct = resp.headers["Content-Type"]
        assert "text/html; charset=utf-8" == str(ct).lower(), ct
        assert "utf-8" == str(resp.encoding).lower(), resp.encoding
        if verbose:
            pp(dict(resp.headers))
        fspec.write_bytes(resp.content)
    return fspec


class SummarizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Summarizer()

    def unused_test_summarize_newsweek(self) -> None:
        self.assertEqual(
            "newsweek has expanded our list to include 499 of the largest public corporations."
            " the companies on our list are in dozens of",
            self.s.add_doc_file(get_article_text_file(), limit=27),
        )

    def unused_test_summarize_deal(self) -> None:
        html_fspec = get_cached_html_file(
            "https://www.nytimes.com/2023/08/10/us/politics/iran-us-prisoner-swap.html"
        )
        text = html2text(html_fspec.read_text())
        text = _remove(r"^[\s\S]+Supported by\n\nSKIP ADVERTISEMENT\n\n# ", "", text)
        text = _remove(r"Michael [ \w]+ from Washington[\s\S]+$", "", text)
        text = _remove(r"Share full article[\s\S]+$", "", text)
        self.assertEqual(
            "five american detainees will eventually be allowed to leave Iran"
            " in exchange for gaining access to $6 billion for humanitarian",
            self.s.add_doc(text),
        )

    def test_load_dataset(self) -> None:
        billsum = load_dataset("billsum", split="ca_test")
        self.assertIsInstance(billsum, Dataset)
        self.assertEqual(
            ["text", "summary", "title"],
            list(billsum.features.keys()),
        )
        self.assertEqual(1237, billsum.num_rows)

    def test_hf_datasets(self) -> None:
        # self.assertGreater(len(list(huggingface_hub.list_datasets())), 51_512)

        # hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json")
        fleurs = "fleurs.py"
        fspec = Path(
            hf_hub_download(
                repo_id="google/fleurs", filename=fleurs, repo_type="dataset"
            )
        )
        self.assertTrue(fspec.exists())
        self.assertEqual(fleurs, fspec.name)
