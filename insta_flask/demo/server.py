#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# mypy: disable-error-code=no-untyped-def
from flask import Flask, request
import numpy as np

from insta_flask.demo.central_tendency import ct_mean, ct_median

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello!\n"


@app.route("/mean", methods=["POST"])
def mean():
    d = request.json
    shape = d["shape"]
    data = np.asarray(d["data"]).reshape(shape)

    return dict(mean=ct_mean(data))


def median() -> dict[str, float]:
    d = request.json
    shape = d["shape"]
    data = np.asarray(d["data"]).reshape(shape)

    return dict(median=ct_median(data))


app.add_url_rule("/median", view_func=median, methods=["POST"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
