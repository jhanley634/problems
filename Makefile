
ACTIVATE = source activate problems

all:
	@echo Hello, world!

perc:
	$(ACTIVATE) && percolate/bin/viz.py
