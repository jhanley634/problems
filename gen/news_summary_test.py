from pathlib import Path
import unittest

from datasets import Dataset, load_dataset
from huggingface_hub import hf_hub_download
import huggingface_hub

from gen.news_summary import Summarizer


class SummarizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Summarizer()

    def test_summarize_newsweek(self):
        # self.s.add_doc("hello world")

        # url = "https://www.newsweek.com/americas-most-responsible-companies-2022"
        # self.s.add_doc_url(url)

        txt_file = Path("/tmp/cache/americas-most-responsible-companies-2022.txt")
        self.assertEqual(
            "a list of America's most Responsible Companies is being compiled by newsweek."
            " the list includes 499 of the largest",  # publified
            self.s.add_doc_file(txt_file, limit=27),
        )

    def test_summarize_deal(self):
        # https://www.nytimes.com/2023/08/10/us/politics/iran-us-prisoner-swap.html
        self.assertEqual(
            "five americans will eventually be allowed to leave the country"
            " in exchange for a $6 billion grant from the united states",
            self.s.add_doc_file(Path("/tmp/deal.txt")),
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
