#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

import gpxpy
import pandas as pd
import typer


def directions(in_file="/tmp/10-Jul-2022-1714.gpx"):
    in_file = Path(in_file).expanduser()
    with open(in_file) as fin:
        _show(gpxpy.parse(fin))


def _get_points(segment):
    for pt in segment.points:
        yield dict(
            time=pt.time, lat=pt.latitude, lon=pt.longitude, elevation=pt.elevation
        )


def _show(gpx):
    df = pd.DataFrame(_get_points(gpx.tracks[0].segments[0]))
    print(df)


if __name__ == "__main__":
    typer.run(directions)
