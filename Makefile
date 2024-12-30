
# Copyright 2021 John Hanley. MIT licensed.

export PATH := $(PATH):$(HOME)/miniconda3/bin
ACTIVATE = source activate problems

all:
	@echo Hello, world!

.venv:
	which uv || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv --python=python3.13

install: .venv
	sort -o requirements.txt{,}
	$(ACTIVATE) && uv pip compile --upgrade --quiet requirements.txt -o infra/requirements.lock
	$(ACTIVATE) && uv pip install -r infra/requirements.lock
	$(ACTIVATE) && pre-commit install

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
C2021 = 'Copyright 202[1-5] John Hanley\. MIT licensed\.'
audit:
	find . -type f | grep -v $(EXCLUDE) | grep $(INCLUDE) | sort | xargs egrep $(L) $(C2021) || true
	infra/audit.py
