from pathlib import Path

from huggingface_hub import hf_hub_download
import requests


class Summarizer:
    CACHE_DIR = Path("/tmp/cache")

    @classmethod
    def _get_cache_filespec(cls, url: str) -> Path:
        cls.CACHE_DIR.mkdir(exist_ok=True)

        basename = Path(url).name
        if "." not in basename:
            basename += ".html"
        return cls.CACHE_DIR / basename

    def add_doc_url(self, url: str) -> None:
        fspec = self._get_cache_filespec(url)
        if not fspec.exists():
            ua = "Wget/1.21.4"
            resp = requests.get(url, headers={"User-Agent": ua})
            resp.raise_for_status()
            ct = resp.headers["Content-Type"]
            assert "text/html; charset=UTF-8" == ct, ct
            assert "UTF-8" == resp.encoding, resp.encoding
            # pp(dict(resp.headers))
            fspec.write_bytes(resp.content)

        self.add_doc(fspec.read_text(encoding="UTF-8"))

    def add_doc_file(self, in_file: Path) -> None:
        self.add_doc(in_file.read_text(encoding="UTF-8"))

    def add_doc(self, text: str) -> None:
        hf_hub_download(repo_id="google/pegasus-xsum", filename="config.json")
