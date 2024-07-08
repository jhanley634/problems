#! /usr/bin/env bash
# Copyright 2024 John Hanley. MIT licensed.

CSV=/tmp/fibo.csv
HDR="type,n,msec"
echo ${HDR}  > ${CSV}

for N in {0..50..10}; do
    geo/lafco/so/iterative_fibo.py ${N}
done |
  sed -u -e 's;^Code block ;;' -e 's;took: ;;' -e 's; ms$;;' |
  tr -u -d "'" |
  tr -u ' ' ',' |
  tee -a ${CSV}

geo/lafco/so/iterative_fibo_plot.py ${CSV}
