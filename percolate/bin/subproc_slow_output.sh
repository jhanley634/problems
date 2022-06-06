#! /usr/bin/env bash

# Testing helper, slowly produces N lines of output.
#
# Copyright 2022 John Hanley. MIT licensed.

N=${1:-30}
DELAY=${2:-1}

i=0
while [ $i -lt $N ]
do
  ((i++))
  echo $(date +%s) $(date) line $i
  sleep $DELAY
done
