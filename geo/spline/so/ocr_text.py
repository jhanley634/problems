#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path

from PIL import Image
import pytesseract as tess
import requests


def ocr_text() -> None:
    psm = 6
    url = "https://www.pgdp.net/projects/projectID60973d0cc23f5/063.png"
    temp = Path("~/Desktop").expanduser()
    img_file = temp / Path(url).name
    if not img_file.exists():
        img_file.write_bytes(requests.get(url).content)

    img = Image.open(img_file)
    s = tess.image_to_string(img, config=f"--psm {psm}")
    print(s)


if __name__ == "__main__":
    ocr_text()
