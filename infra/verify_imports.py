#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
"""
Verifies that packages load without error, e.g. due to missing deps.
"""
from abc import ABC  # noqa F401
from collections import Counter  # noqa F401
from collections import defaultdict  # noqa F401
from collections import deque  # noqa F401
from collections import namedtuple  # noqa F401
from collections.abc import Generator  # noqa F401
from dataclasses import dataclass  # noqa F401
from distutils.core import setup  # noqa F401
from enum import Enum, auto  # noqa F401
from functools import lru_cache  # noqa F401
from functools import partial  # noqa F401
from functools import partialmethod  # noqa F401
from functools import total_ordering  # noqa F401
from glob import glob  # noqa F401
from hashlib import blake2b  # noqa F401
from hashlib import sha3_224  # noqa F401
from inspect import cleandoc  # noqa F401
from io import BytesIO  # noqa F401
from io import StringIO  # noqa F401
from io import TextIOWrapper  # noqa F401
from itertools import pairwise  # noqa F401
from math import ceil  # noqa F401
from math import sqrt  # noqa F401
from operator import attrgetter  # noqa F401
from pathlib import Path  # noqa F401
from pprint import pp  # noqa F401
from queue import PriorityQueue  # noqa F401
from random import randrange  # noqa F401
from random import seed  # noqa F401
from select import PIPE_BUF, select  # noqa F401
from shutil import copyfile  # noqa F401
from sqlite3 import Connection  # noqa F401
from subprocess import check_output  # noqa F401
from subprocess import PIPE, Popen  # noqa F401
from threading import Thread  # noqa F401
from time import time  # noqa F401
from time import sleep, strftime  # noqa F401
from typing import Any  # noqa F401
from typing import Generator  # noqa F401
from typing import Optional  # noqa F401
from typing import TextIO  # noqa F401
from typing import Tuple  # noqa F401
from typing import Iterable, Iterator, NamedTuple, Self  # noqa F401
from urllib.parse import urlparse  # noqa F401
import contextlib  # noqa F401
import datetime  # noqa F401
import dis  # noqa F401
import gc  # noqa F401
import inspect  # noqa F401
import io  # noqa F401
import json  # noqa F401
import logging  # noqa F401
import os  # noqa F401
import random  # noqa F401
import re  # noqa F401
import shutil  # noqa F401
import struct  # noqa F401
import subprocess  # noqa F401
import sys  # noqa F401
import unittest  # noqa F401

from bs4 import BeautifulSoup  # noqa F401
from bs4 import Tag  # noqa F401
from datasets import Dataset, load_dataset  # noqa F401
from flask import Flask  # noqa F401
from flask import request  # noqa F401
from geopy import Point  # noqa F401
from geopy.distance import great_circle  # noqa F401
from glom import glom  # noqa F401
from gpxpy.gpx import GPX  # noqa F401
from gpxpy.gpx import GPXTrackSegment  # noqa F401
from html2text import html2text  # noqa F401
from huggingface_hub import hf_hub_download  # noqa F401
from hypothesis import given  # noqa F401
from ipyleaflet import AwesomeIcon, Map, Marker, basemaps  # noqa F401
from markdownify import markdownify  # noqa F401
from memory_profiler import profile  # noqa F401
from numba import njit  # noqa F401
from numba import int_, jit  # noqa F401
from numpy import dtype  # noqa F401
from numpy import loadtxt  # noqa F401
from numpy import nan  # noqa F401
from numpy.random import default_rng  # noqa F401
from numpy.testing import assert_array_equal  # noqa F401
from osmnx.graph import graph_from_place  # noqa F401
from palettable.colorbrewer import qualitative  # noqa F401
# ignore F401 "imported but unused"
from PIL import Image, ImageDraw  # noqa F401
from PIL.Image import Image  # noqa F401
from PIL.ImageDraw import ImageDraw  # noqa F401
from polars import Utf8  # noqa F401
from pyAudioAnalysis import ShortTermFeatures, audioBasicIO  # noqa F401
from pydub import AudioSegment  # noqa F401
from pygame import Rect, Surface, Vector2  # noqa F401
from requests import Response  # noqa F401
from roman import InvalidRomanNumeralError  # noqa F401
from roman import fromRoman  # noqa F401
from scipy.fft import rfft, rfftfreq  # noqa F401
from scipy.spatial.distance import pdist, squareform  # noqa F401
from sklearn.ensemble import RandomForestRegressor  # noqa F401
from sklearn.linear_model import LinearRegression  # noqa F401
from sklearn.model_selection import GridSearchCV  # noqa F401
from sklearn.neighbors import KernelDensity  # noqa F401
from sortedcontainers import SortedList  # noqa F401
from spacy import Language  # noqa F401
from spacy.cli import download  # noqa F401
from spacy.tokens import Span  # noqa F401
from streamlit_image_coordinates import streamlit_image_coordinates  # noqa F401
from tqdm import tqdm  # noqa F401
from transformers import T5ForConditionalGeneration, T5Tokenizer  # noqa F401
from typer import Option  # noqa F401
from typing_extensions import Annotated  # noqa F401
from uszipcode import SearchEngine  # noqa F401
import click  # noqa F401
import cv2  # noqa F401
import geopandas  # noqa F401
import gpxpy  # noqa F401
import huggingface_hub  # noqa F401
import hypothesis.strategies  # noqa F401
import matplotlib  # noqa F401
import matplotlib.pyplot  # noqa F401
import networkit  # noqa F401
import networkx  # noqa F401
import numpy  # noqa F401
import numpy.typing  # noqa F401
import osmnx  # noqa F401
import pandas  # noqa F401
import polars  # noqa F401
import pyarrow  # noqa F401
import pyarrow.parquet  # noqa F401
import pydeck  # noqa F401
import pygame  # noqa F401
import pyspark.context  # noqa F401
import pyspark.pandas  # noqa F401
import regex  # noqa F401
import requests  # noqa F401
import seaborn  # noqa F401
import sklearn.datasets  # noqa F401
import sklearn.metrics  # noqa F401
import sklearn.model_selection  # noqa F401
import spacy  # noqa F401
import sqlalchemy  # noqa F401
import sqlalchemy.orm  # noqa F401
import streamlit  # noqa F401
import sympy  # noqa F401
import typer  # noqa F401
import unidecode  # noqa F401

from autoencode.util.projection import _hash_col, feature_subset  # noqa F401
from cluster.jutland.dataset import Dataset  # noqa F401
from dojo.sudoku.puzzle import Grid  # noqa F401
from dojo.sudoku.puzzle import solve  # noqa F401
from feature_sel.ozone.ozone import COLS, get_df  # noqa F401
from gen.news_summary import Summarizer  # noqa F401
from gen.news_summary import get_cache_filespec  # noqa F401
from gen.news_summary_test import get_article_text_file  # noqa F401
from geo.greenwave.demo import Car, City, Obstacle  # noqa F401
from geo.ski.dwell import GPX_DIR  # noqa F401
from geo.ski.iso_filenames import GPX_DIR, copy_all, iso  # noqa F401
from geo.ski.word_ladder2 import WordLadder  # noqa F401
from geo.ski.word_ladder_test import _get_months  # noqa F401
from geo.zone.law_parser import LawParser  # noqa F401
from geo.zone.outline_parser import OutlineParser  # noqa F401
from geo.zone.outline_parser import Level, _reverse_enumerate  # noqa F401
from insta_flask.demo.central_tendency import ct_mean, ct_median  # noqa F401
from percolate.bin.slider_pair_state import prev  # noqa F401
from percolate.two_d_percolation import Perc  # noqa F401
from vision.find_shape.find_ngons import BLACK, urls  # noqa F401
from vision.find_shape.web_image import WebImage  # noqa F401
from web.wiki.history import HistoryScraper  # noqa F401
