#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path

from gpxpy.gpx import GPX
import gpxpy
import typer


def main(infile="/tmp/k/14-Jul-2022-1234-pizza.gpx"):
    infile = Path(infile)
    with open(infile) as fin:
        gpx = gpxpy.parse(fin)
        report(gpx)


def report(gpx: GPX, prec=6):
    prev = None
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                prev = prev or point.time
                delta = point.time - prev
                lat = round(point.latitude, prec)
                lng = round(point.longitude, prec)
                print(delta, str(point.time), f"   {lat:.6f}  {lng:.6f}")
                prev = point.time


if __name__ == "__main__":
    typer.run(main)
