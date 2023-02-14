#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from typing import Optional
import datetime as dt

from gpxpy.gpx import GPX
import gpxpy
import polars as pl
import typer


def main(infile="~/Desktop/gpx/2022-07-14-1234-pizza.gpx"):
    infile = Path(infile).expanduser()
    with open(infile) as fin:
        gpx = gpxpy.parse(fin)
        df = pl.DataFrame(get_breadcrumbs(gpx))
        print(df)


def get_breadcrumbs(gpx: GPX, precision=6):
    prev: Optional[dt.datetime] = None
    for t, track in enumerate(gpx.tracks):
        for s, segment in enumerate(track.segments):
            for point in segment.points:
                prev = prev or point.time
                delta = point.time - prev  # type: ignore
                lat = round(point.latitude, precision)
                lng = round(point.longitude, precision)
                print(t, s, delta, point.time, f"   {lat:.6f}  {lng:.6f}")
                yield dict(stamp=point.time, lat=lat, lng=lng, delta=delta)
                prev = point.time


if __name__ == "__main__":
    typer.run(main)
