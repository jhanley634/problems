#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from paddleocr import PaddleOCR
from PIL import Image
import pytesseract as tess
import requests


def ocr_text() -> None:
    psm = 6
    url = "https://www.pgdp.net/projects/projectID60973d0cc23f5/063.png"
    temp = Path("~/Desktop").expanduser()
    img_path = temp / Path(url).name
    if not img_path.exists():
        img_path.write_bytes(requests.get(url).content)

    img = Image.open(img_path)
    s = tess.image_to_string(img, config=f"--psm {psm}")
    print(s)

    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    result = ocr.ocr(img_path.read_bytes(), cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

    model = ocr_predictor(pretrained=True)
    doc = DocumentFile.from_images([img_path])
    result = model(doc)
    print(result.render())


if __name__ == "__main__":
    ocr_text()
