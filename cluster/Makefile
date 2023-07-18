
# Copyright 2021 John Hanley. MIT licensed.

ACTIVATE = source activate problems

OUT = \
  jutland/out/x \

all: $(OUT)

SPATIAL=3D_spatial_network.txt
JUTLAND_IN = https://archive.ics.uci.edu/ml/machine-learning-databases/00246/$(SPATIAL)

jutland/out/x: /tmp/$(SPATIAL)
	cd .. && cluster/jutland/bin/report.py

/tmp/$(SPATIAL):
	cd /tmp && wget -q $(JUTLAND_IN)
