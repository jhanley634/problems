
# Copyright 2021 John Hanley. MIT licensed.

ACTIVATE = source activate problems

all:
	@echo Hello, world!

VERIFY = $(ACTIVATE) && infra/verify_imports.py && flake8

verify:
	$(VERIFY)
update-verify:
	time conda env update
	$(VERIFY)

perc:
	$(ACTIVATE) && percolate/bin/viz.py

# After `make jupyter`,
# navigate down to: percolate/notebooks/percolation_visualization.ipynb
jupyter:
	$(ACTIVATE) && env PYTHONPATH=../.. jupyter notebook
