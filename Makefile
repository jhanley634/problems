
# Copyright 2021 John Hanley. MIT licensed.

export PATH := $(PATH):$(HOME)/miniconda3/bin
ACTIVATE = source activate problems

all:
	@echo Hello, world!

IGNORE_TZ = env PYARROW_IGNORE_TIMEZONE=1 PYGAME_HIDE_SUPPORT_PROMPT=1
VERIFY = $(ACTIVATE) && $(IGNORE_TZ) infra/verify_imports.py && flake8

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

COVERAGE = --cov --cov-report=term-missing --import-mode=importlib
test:
	$(ACTIVATE) && pytest $(COVERAGE)  geo/
	$(ACTIVATE) && python -m unittest  $$(find . -name '*_test.py' | sort) ; isort . ; black -S geo/
	$(ACTIVATE) && mypy --no-namespace-packages --ignore-missing-imports cluster/ [abd-uw-z]*/
SHELL = bash -o pipefail

INCLUDE = '\.py$$'
EXCLUDE = '/loadtxt.d/pythran_lib/build/lib.macosx-10.9-x86_64-cpython-310/hello/'
L = --files-without-match
C2022 = 'Copyright 202[1234] John Hanley\. MIT licensed\.'
audit:
	infra/audit.py
	@-find . -type f | grep -v $(EXCLUDE) | grep $(INCLUDE) | sort | xargs egrep $(L) $(C2022) || true
