from pathlib import Path
from pprint import pp
import unittest

from datasets import Dataset, load_dataset
from html2text import html2text
from huggingface_hub import hf_hub_download
import huggingface_hub
import requests

from gen.news_summary import Summarizer


class SummarizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Summarizer()

    def test_summarize_newsweek(self):
        url = "https://www.newsweek.com/americas-most-responsible-companies-2022"
        fspec = self.get_cached_url(url)
        text = html2text(fspec.read_text())
        fspec.write_text(text)
        self.assertEqual(
            "a list of America's most Responsible Companies is being compiled by newsweek."
            " the list includes 499 of the largest",  # publified
            self.s.add_doc_file(fspec, limit=27),
        )

    def get_cached_url(self, url: str, verbose=False) -> Path:
        fspec = self.s._get_cache_filespec(url)
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

    def test_summarize_deal(self):
        fspec = self.get_cached_url(
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
