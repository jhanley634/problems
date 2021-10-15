
# Copyright 2021 John Hanley. MIT licensed.

ACTIVATE = source activate problems

OUT = \
  cluster/jutland/out/x \

all: $(OUT)

SPATIAL=3D_spatial_network.txt
JUTLAND_IN = https://archive.ics.uci.edu/ml/machine-learning-databases/00246/$(SPATIAL)

cluster/jutland/out/x: /tmp/$(SPATIAL)

/tmp/$(SPATIAL):
	cd /tmp && wget $(JUTLAND_IN)
