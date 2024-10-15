# Copyright 2021 John Hanley. MIT licensed.
from hashlib import sha3_224
from pathlib import Path

import requests

_tmp = Path("/tmp")


class WebImage:
    """Offers cached access to images from the web."""

    def __init__(self, url: str, filename: str = "shapes.jpg", temp: Path = _tmp) -> None:
        self.url = url
        digest = sha3_224(url.encode()).hexdigest()[:4]
        self.fspec = temp / f"img{digest}_{filename}"

    def image(self) -> str:
        if not self.fspec.exists():
            resp = requests.get(self.url)
            resp.raise_for_status()
            with open(self.fspec, "wb") as fout:
                fout.write(resp.content)
        return f"{self.fspec}"
