
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

SHELL = bash -o pipefail

INCLUDE = '\.py$$'
EXCLUDE = '/loadtxt.d/pythran_lib/build/lib.macosx-10.9-x86_64-cpython-310/hello/'
L = --files-without-match
C2022 = 'Copyright 202[123] John Hanley\. MIT licensed\.'
audit:
	@-find . -type f | grep -v $(EXCLUDE) | grep $(INCLUDE) | sort | xargs egrep $(L) $(C2022) || true
