#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
"""
Verifies that packages load without error, e.g. due to missing deps.
"""
from collections import Counter  # noqa F401 ignore "imported but unused"
from collections import namedtuple  # noqa F401
from distutils.core import setup  # noqa F401
from glob import glob  # noqa F401
from hashlib import blake2b  # noqa F401
from hashlib import sha3_224  # noqa F401
from pathlib import Path  # noqa F401
from pprint import pp  # noqa F401
from queue import PriorityQueue  # noqa F401
from random import randrange  # noqa F401
from random import seed  # noqa F401
from select import PIPE_BUF, select  # noqa F401
from shutil import copyfile  # noqa F401
from sqlite3 import Connection  # noqa F401
from subprocess import PIPE, Popen  # noqa F401
import datetime  # noqa F401
import io  # noqa F401
import os  # noqa F401
import re  # noqa F401
import subprocess  # noqa F401
import unittest  # noqa F401

from glom import glom  # noqa F401
from ipyleaflet import AwesomeIcon, Map, Marker, basemaps  # noqa F401
from numpy import loadtxt  # noqa F401
from numpy import nan  # noqa F401
from numpy.random import default_rng  # noqa F401
from osmnx.graph import graph_from_place  # noqa F401
from palettable.colorbrewer import qualitative  # noqa F401
from pandas_profiling import ProfileReport  # noqa F401
from PIL.Image import Image  # noqa F401
from PIL.ImageDraw import ImageDraw  # noqa F401
from sklearn.ensemble import RandomForestRegressor  # noqa F401
from sklearn.linear_model import LinearRegression  # noqa F401
from tqdm import tqdm  # noqa F401
from uszipcode import SearchEngine  # noqa F401
import click  # noqa F401
import cv2  # noqa F401
import gpxpy  # noqa F401
import matplotlib.pyplot  # noqa F401
import networkit  # noqa F401
import numpy  # noqa F401
import osmnx  # noqa F401
import pandas  # noqa F401
import pyarrow  # noqa F401
import pyarrow.parquet  # noqa F401
import pydeck  # noqa F401
import requests  # noqa F401
import seaborn  # noqa F401
import sklearn.datasets  # noqa F401
import sklearn.metrics  # noqa F401
import sklearn.model_selection  # noqa F401
import streamlit  # noqa F401
import typer  # noqa F401

from autoencode.util.projection import _hash_col, feature_subset  # noqa F401
from cluster.jutland.dataset import Dataset  # noqa F401
from feature_sel.ozone.ozone import COLS, get_df  # noqa F401
from percolate.bin.slider_pair_state import prev  # noqa F401
from percolate.two_d_percolation import Perc  # noqa F401
from vision.find_shape.find_ngons import BLACK, urls  # noqa F401
from vision.find_shape.web_image import WebImage  # noqa F401
from web.wiki.history import HistoryScraper  # noqa F401
