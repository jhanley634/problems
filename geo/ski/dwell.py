#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
import datetime as dt

from geopy import Point
from geopy.distance import great_circle
from gpxpy.gpx import GPX
from typing_extensions import Any
import gpxpy
import polars as pl
import typer

GPX_DIR = Path("~/Desktop/gpx").expanduser()


def main(infile: str = f"{GPX_DIR}/2022-07-14-1234-pizza.gpx") -> None:
    infile_ = Path(infile).expanduser()
    with open(infile_) as fin:
        gpx = gpxpy.parse(fin)
        df = pl.DataFrame(get_rows(gpx))
        print(df)


def get_rows(gpx: GPX) -> Generator[dict[Any, Any], None, None]:
    g = get_breadcrumbs(gpx)
    cum = 0
    first_row = next(g)
    first_loc = Point(first_row["lat"], first_row["lng"])
    for row in g:
        cum += row["delta_x"]
        d = dict(
            elapsed=(row["stamp"] - first_row["stamp"]).total_seconds(),
            cum=cum,
            crow_fly=great_circle(Point(row["lat"], row["lng"]), first_loc).meters,
        )
        yield {**row, **d}


def get_breadcrumbs(
    gpx: GPX, precision: int = 6, verbose: bool = False
) -> Generator[dict[Any, Any], None, None]:
    prev_time: dt.datetime | None = None
    prev_loc: Point | None = None
    for track in gpx.tracks:
        for s, segment in enumerate(track.segments):
            for point in segment.points:
                prev_time = prev_time or point.time
                delta_t = point.time - prev_time  # type: ignore
                elapsed = max(0.001, delta_t.total_seconds())
                lat = round(point.latitude, precision)
                lng = round(point.longitude, precision)
                loc = Point(lat, lng)
                delta_x = great_circle(prev_loc, loc).meters if prev_loc else 0
                if verbose:
                    print(s, delta_t, point.time, f"   {lat:.6f}  {lng:.6f}")
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
