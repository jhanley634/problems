#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from typing import Optional
import datetime as dt

from geopy import Point
from geopy.distance import great_circle
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
    prev_time: Optional[dt.datetime] = None
    prev_loc: Optional[Point] = None
    for t, track in enumerate(gpx.tracks):
        for s, segment in enumerate(track.segments):
            for point in segment.points:
                prev_time = prev_time or point.time
                delta_t = point.time - prev_time  # type: ignore
                elapsed = max(0.001, delta_t.total_seconds())
                lat = round(point.latitude, precision)
                lng = round(point.longitude, precision)
                loc = Point(lat, lng)
                delta_x = great_circle(prev_loc, loc).meters if prev_loc else 0
                print(t, s, delta_t, point.time, f"   {lat:.6f}  {lng:.6f}")
                yield dict(
                    stamp=point.time,
                    lat=lat,
                    lng=lng,
                    delta_t=delta_t,
                    delta_x=delta_x,
                    speed=delta_x / elapsed,
                )
                prev_time = point.time
                prev_loc = loc


if __name__ == "__main__":
    typer.run(main)
