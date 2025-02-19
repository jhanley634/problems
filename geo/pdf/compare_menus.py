#! /usr/bin/env python
# Copyright 2025 John Hanley. MIT licensed.


from pathlib import Path
import io
import re

from pdf2image import convert_from_path
from PIL import Image
import pdftotext
import pytesseract as tess
import requests

temp = Path("/tmp/menu")


dining = "https://www.palisadestahoe.com/-/media/palisades-tahoe/pdfs/dining"
urls = [
    dining
    + "/rocker-brunch-2425.pdf?rev=5fc1fbfbb77b4762b082fc6f2f61d9c4&hash=8BD85290FC47D250EAD86521A404F9CE",
    dining
    + "/rocker-lunch-2425-(2).pdf?rev=3ed7b5d7e94d41d488d29773422f49af&hash=429FC56D0F58CB6D05C35F3967164228",
    dining
    + "/rocker-dinner-2425-(2).pdf?rev=81707816d5164e1db5aa67fcfaaa6031&hash=8F45357D16DA78887A8559EA682C8366",
]


def main() -> None:
    temp.mkdir(exist_ok=True)
    if not (temp / "dinner.txt").exists():
        _fetch_menus()
    for meal in ["brunch", "lunch", "dinner"]:
        _ocr(temp / f"{meal}.pdf")


def _fetch_menus() -> None:
    for url in urls:
        out_file = _get_out_file(url)
        response = requests.get(url)
        with open(out_file, "wb") as f:
            f.write(response.content)

        pdf = pdftotext.PDF(io.BytesIO(response.content))
        print(len(pdf), out_file)
        with open(out_file.with_suffix(".txt"), "w") as f:
            f.write("\n\n".join(pdf))


def _get_out_file(url: str) -> Path:
    pat = re.compile(r"pdfs/dining/rocker-(\w+)-2425")

    m = pat.search(url)
    assert m

    name = m.group(1)
    return temp / f"{name}.pdf"


def _ocr(pdf_file: Path) -> None:
    psm = 12
    image_file = _convert_pdf_to_image(pdf_file)
    image = Image.open(image_file)
    assert (1700, 2200) == image.size
    assert "PNG" == image.format

    text = tess.image_to_string(image, config=f"--psm {psm}")
    with open(f"{temp / pdf_file.stem}_ocr.txt", "w") as fout:
        fout.write(text)


def _convert_pdf_to_image(pdf_file: Path) -> Path:
    image_file = pdf_file.with_suffix(".png")
    images = convert_from_path(pdf_file, first_page=1, last_page=1)
    gray_image = images[0].quantize(2)  # binarize

    gray_image.save(image_file, "PNG")
    return image_file


if __name__ == "__main__":
    main()
