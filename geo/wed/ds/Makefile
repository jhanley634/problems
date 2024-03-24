
# Copyright 2024 John Hanley. MIT licensed.

SHELL := bash
ENV := caret
BIN := $(shell dirname $(CONDA_EXE))
ACTIVATE = source $(BIN)/activate $(ENV)

all:
	black .
	$(ACTIVATE) && time env PYTHONPATH=../../..:. ./austin_garbage.py
	isort .
	ruff check
