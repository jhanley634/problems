#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import json

import numpy as np
import requests


def main():
    assert "Hello!" == requests.get("http://localhost:5000/hello").text.rstrip()

    url = "http://localhost:5000/mean"
    headers = {"Content-Type": "application/json"}
    data = np.array([1, 2, 6])
    jsn = json.dumps(dict(shape=data.shape, data=data.tolist()))
    resp = requests.post(url, headers=headers, data=jsn)
    ct_mean = resp.json()["mean"]
    assert 3 == ct_mean


if __name__ == "__main__":
    main()
