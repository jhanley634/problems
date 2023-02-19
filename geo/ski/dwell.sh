#! /usr/bin/env bash

# Copyright 2023 John Hanley. MIT licensed.

set -e -x

for f in ~/Desktop/gpx/*.gpx; do
    time geo/ski/dwell.py --infile $f
done
