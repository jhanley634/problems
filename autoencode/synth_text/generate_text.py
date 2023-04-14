# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

_desktop = Path("~/Desktop").expanduser()


class GenerateSyntheticTextImage:
    def __init__(self, width: int = 32, height: int = 32, out_dir: Path = _desktop):
        self.width = width
        self.height = height
        self.out_dir = out_dir.expanduser()

    def generate(self, id_: int = 1001, text: str = "A") -> None:
        d = ImageDraw(Image())
        d.text((0, 0), "hi")
