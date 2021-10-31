
# Copyright 2021 John Hanley. MIT licensed.
from hashlib import sha3_224
from pathlib import Path

import requests


class WebImage:
    """Offers cached access to images from the web."""

    def __init__(self, url, fname='shapes.jpg', temp=Path('/tmp')):
        self.url = url
        pfx = 'img' + sha3_224(url.encode()).hexdigest()[:4]
        self.fspec = temp / f'{pfx}_{fname}'

    def image(self):
        if not self.fspec.exists():
            resp = requests.get(self.url)
            resp.raise_for_status()
            with open(self.fspec, 'wb') as fout:
                fout.write(resp.content)
        return f'{self.fspec}'
