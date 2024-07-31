#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import io

from matplotlib import pyplot as plt
from PIL import Image
from requests_cache import CachedSession

# https://www.prokerala.com/news/photos/philippines-albay-volcano-eruption-327315.html
chile = "https://www.mountainprofessor.com/images/osorno-volcano-Chile2.jpg"
philippines, volcano = (
    "https://files.prokerala.com/news/photos/imgs/1024/albay-jan-25-2018-a-fishing-boat-sails-as-mayon-640225.jpg",
    "https://www.worldatlas.com/r/w1200/upload/2f/9b/57/shutterstock-787922728.jpg",
)
moon = (
    "https://web.archive.org/web/20240512195553/https://c.pxhere.com"
    "/photos/20/86/volcano_erupting_full_moon_mountain_mt_merapi_indonesia_eruption_lava-1084711.jpg!d"
)


def get_image(url: str) -> Image.Image:
    cache_dir = Path("/tmp/k")
    cache_dir.mkdir(exist_ok=True)

    session = CachedSession(cache_name=f"{cache_dir}/requests_cache", expire_after=7200)
    buf = io.BytesIO(session.get(url).content)
    return Image.open(buf)


def show_volcano(url: str = volcano) -> None:
    fig, ax = plt.subplots()
    img = get_image(url)
    ax.imshow(img)

    assert (1100, 734) == img.size
    assert (-0.5, 1099.5) == ax.get_xlim()
    assert (733.5, -0.5) == ax.get_ylim()

    plt.show()


if __name__ == "__main__":
    show_volcano()
