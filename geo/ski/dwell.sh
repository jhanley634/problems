#! /usr/bin/env bash

set -e -x

for f in ~/Desktop/gpx/*.gpx; do
    time geo/ski/dwell.py --infile $f
done
