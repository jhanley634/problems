#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/289724/digit-ocr-using-tesseract

from pathlib import Path
from typing import Any
import re

from numpy.typing import NDArray
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"tesseract"


def apply_tesseract(image_path: Path, psm: int) -> tuple[NDArray[Any], str]:
    image = cv2.imread(f"{image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    assert np.max(image) <= 255
    h, w = image.shape
    both = np.concatenate((_get_hello(h), image), axis=1)
    text = pytesseract.image_to_string(both, config=f"--psm {psm} digits")
    return image, text


def _get_hello(height: int, word: str = "Hello") -> NDArray[np.int_]:
    font = cv2.FONT_HERSHEY_PLAIN
    bottom_left = 6, height - 3
    font_scale = 1.35
    font_color = (0, 0, 0)
    thickness = 1
    line_type = cv2.LINE_AA

    img = 255 * np.ones((height, 70), dtype=np.uint8)
    cv2.putText(
        img, word, bottom_left, font, font_scale, font_color, thickness, line_type
    )

    return img


def display_images_with_text(images: list[NDArray[Any]], texts: list[str]) -> None:
    num_images = len(images)
    num_rows = min(3, num_images)
    num_cols = (num_images + num_rows - 1) // num_rows

    fig, axes = plt.subplots(
        num_rows, num_cols, figsize=(12, 8), subplot_kw={"xticks": [], "yticks": []}
    )

    for i, (image, text) in enumerate(zip(images, texts)):
        ax = axes[i // num_cols, i % num_cols] if num_rows > 1 else axes[i % num_cols]
        ax.imshow(image)
        ax.axis("off")
        ax.set_title(text)

    plt.show()


def main(folder_path: Path) -> None:
    images = []
    texts = []
    # Page Segmentation Modes:
    # 6: Assume a single uniform block of text.
    # 7: Treat the image as a single text line.
    # 8: Treat the image as a single word.
    # 13: Treat the image as a single text line,
    #     bypassing hacks that are Tesseract-specific.
    for psm in [6, 7]:
        for filename in folder_path.glob("ocr*.png"):
            image, text = apply_tesseract(folder_path / filename, psm)
            images.append(image)
            match = "" if _is_match(text.rstrip(), filename.name) else "X"
            texts.append(f"{match} [{psm}]: {text}")

    display_images_with_text(images, texts)


_filename_re = re.compile(r"ocr-\d+-(\d+)\.png")


def _is_match(text: str, filename: str) -> bool:
    expected = None
    if len(text) >= 15:
        expected = "986368798212196"
    m = _filename_re.match(f"{filename}")  # extracts Ground Truth value
    if m:
        expected = m[1]
    print(f"{filename}\t{expected}\t{text}")
    return text == expected


if __name__ == "__main__":
    folder_path = Path("~/Desktop/").expanduser()
    main(folder_path)
