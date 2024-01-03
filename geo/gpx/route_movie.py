#! /usr/bin/env python
#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path
from typing import Generator
import datetime as dt

from geopy import Point
from gpxpy.gpx import GPX
import gpxpy

from geo.gpx.route_viz import _display, _get_chosen_gpx_path
from geo.ski.dwell import get_breadcrumbs


def main() -> None:
    in_file = Path("~/Desktop/gpx.d/2023-12-07T22:20:02Z-willows-walk.gpx").expanduser()

    df = _get_df(in_file)

    # _display(_get_df(_get_chosen_gpx_path()))


def _get_gpx_points(in_file: Path) -> Generator[Point, None, None]:
    # Similar to _get_breadcrumbs()
    with open(in_file) as fin:
        gpx: GPX = gpxpy.parse(fin)
        for row in gpx.tracks:
            for segment in row.segments:
                for pt in segment.points:
                    stamp: dt.datetime = pt.time
                    stamp = stamp.replace(tzinfo=None).astimezone(dt.timezone.utc)
                    yield dict(
                        stamp=stamp,
                        lat=round(pt.latitude, 6),
                        lng=round(pt.longitude, 6),
                        elevation=round(pt.elevation, 2),
                    )


if __name__ == "__main__":
    main()
