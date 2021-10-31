#! /usr/bin/env python
# Copyright 2021 John Hanley. MIT licensed.
"""
Verifies that packages load without error, e.g. due to missing deps.
"""
# ignore F401 "imported but unused"
from PIL import Image  # noqa F401
from ruamel.yaml import YAML  # noqa F401
import autoPyTorch  # noqa F401
import dask  # noqa F401
import fasteners  # noqa F401
import geopandas  # noqa F401
import geopy  # noqa F401
import isort  # noqa F401
import openml  # noqa F401
import palettable  # noqa F401
import pandas as pd  # noqa F401
import psutil  # noqa F401
import pyarrow  # noqa F401
import pydeck  # noqa F401
import pynisher  # noqa F401
import scipy  # noqa F401
import sklearn  # noqa F401
import streamlit  # noqa F401
