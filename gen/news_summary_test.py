from pathlib import Path
from pprint import pp
import os
import re
import unittest

from datasets import Dataset, load_dataset
from html2text import html2text
from huggingface_hub import hf_hub_download
import huggingface_hub
import requests

from gen.news_summary import Summarizer, get_cache_filespec


def _remove(pattern: str, subst: str, s: str, flags: int = re.NOFLAG) -> str:
    t = re.sub(pattern, subst, s, flags=flags)

    # If regex failed to match, then say so.
    if not len(t) < len(s):
        print(s)
    assert len(t) < len(s), (len(t), len(s), pattern)

    return t


def get_article_text_file(
    url: str = "https://www.newsweek.com/americas-most-responsible-companies-2022",
) -> Path:
    html_fspec = get_cached_html_file(url)
    text = html2text(html_fspec.read_text())
    text = _remove(r"^[\s\S]+ Comments", "", text)
    text = _remove(r"Nancy Cooper.+$", "", text, flags=re.DOTALL).strip()
    base, _ = os.path.splitext(html_fspec)
    txt_fspec = Path(f"{base}.txt")
    txt_fspec.write_text(text)
    return txt_fspec


def get_cached_html_file(url: str, verbose=False) -> Path:
    fspec = get_cache_filespec(url)
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

    def test_summarize_newsweek(self) -> None:
        print(6)
        print(self.s.add_doc_file(get_article_text_file().read_text(), limit=27))
        print(7)

        self.assertEqual(
            "## America's Most Responsible Companies 2022 * * * * * * * * * * * * * * * * *"
            "a list of America's most Responsible Companies is being compiled by newsweek."
            " the list includes 499 of the largest",  # publified
            self.s.add_doc_file(get_article_text_file().read_text(), limit=27),
        )

    def test_summarize_deal(self):
        fspec = get_cached_html_file(
            "https://www.nytimes.com/2023/08/10/us/politics/iran-us-prisoner-swap.html"
        )
        self.assertEqual(
            "five americans will eventually be allowed to leave the country"
            " in exchange for a $6 billion grant from the united states",
            self.s.add_doc_file(fspec),
        )

    def test_load_dataset(self):
        billsum = load_dataset("billsum", split="ca_test")
        self.assertIsInstance(billsum, Dataset)
        self.assertEqual(
            ["text", "summary", "title"],
            list(billsum.features.keys()),
        )
        self.assertEqual(1237, billsum.num_rows)

    def test_hf_datasets(self) -> None:
        self.assertGreater(len(list(huggingface_hub.list_datasets())), 51_512)

        # hf_hub_download(repo_id="lysandre/arxiv-nlp", filename="config.json")
        fleurs = "fleurs.py"
        fspec = Path(
            hf_hub_download(
                repo_id="google/fleurs", filename=fleurs, repo_type="dataset"
            )
        )
        self.assertTrue(fspec.exists())
        self.assertEqual(fleurs, fspec.name)
