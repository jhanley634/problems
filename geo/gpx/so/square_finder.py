#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from dataclasses import dataclass
# based on https://stackoverflow.com/questions/77902878/problem-with-opencv-to-recognize-numbers-and-digits-on-video
from pathlib import Path
from pprint import pp
import io

from beartype import beartype
from PIL import Image, ImageEnhance, ImageOps
from requests_cache import CachedSession
import cv2
import numpy as np
import pandas as pd
import pytesseract


@beartype
def get_image(url: str = "https://i.stack.imgur.com/bhrAt.png") -> Image.Image:
    cache_dir = Path("/tmp/k/url")
    session = CachedSession(cache_name=f"{cache_dir}/requests_cache", expire_after=7200)
    buf = io.BytesIO(session.get(url).content)
    return Image.open(buf)


@beartype
def main() -> None:
    img = ImageOps.grayscale(get_image())
    assert (1671, 928) == img.size
    assert "L" == img.mode

    a = np.array(img.getdata(), dtype=np.uint8).reshape(tuple(reversed(img.size)))
    print(a.shape, a.dtype, a.min(), a.max())

    thresh = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(a, (x, y), (x + w, y + h), (36, 255, 12), 2)

    img = Image.fromarray(thresh)
    print(img)
    img.show()


@dataclass
class Foo:
    def __init__(self):
        self._open: float = 2.718

    @property
    def open(self) -> float:
        return self._open

    @open.setter
    def open(self, value: float) -> None:
        if value < 0.0:
            raise ValueError("Open value must be positive.")
        self._open = value


if __name__ == "__main__":
    f = Foo()
    assert 2.718 == f.open
    f.open = 3.14
    assert 3.14 == f.open

    # main()
