#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import json

import numpy as np
import requests


def main():
    assert "Hello!" == requests.get("http://localhost:5000/hello").text.rstrip()
    check_mean()
    check_median()


headers = {"Content-Type": "application/json"}


def url(path):
    return f"http://localhost:5000/{path}"


def check_mean():
    data = np.array([1, 2, 6])
    jsn = json.dumps(dict(shape=data.shape, data=data.tolist()))
    resp = requests.post(url("/mean"), headers=headers, data=jsn)
    ct_mean = resp.json()["mean"]
    assert 3 == ct_mean


def check_median():
    data = np.array([1, 2, 6])
    jsn = json.dumps(dict(shape=data.shape, data=data.tolist()))
    resp = requests.post(url("/median"), headers=headers, data=jsn)
    ct_median = resp.json()["median"]
    assert 2 == ct_median


if __name__ == "__main__":
    main()
