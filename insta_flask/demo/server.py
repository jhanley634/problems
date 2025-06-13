#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
# mypy: disable-error-code=no-untyped-def
from flask import Flask, request
import numpy as np

from insta_flask.demo.central_tendency import ct_mean, ct_median

app = Flask(__name__)


@app.route("/hello")
def hello() -> str:
    return "Hello!\n"


@app.route("/mean", methods=["POST"])
def mean() -> dict[str, float]:

    # Argument 1 to "dict" has incompatible type "Any | None";
    # expected "SupportsKeysAndGetItem[Any, Any]"  [arg-type]
    d = dict(request.json)  # type: ignore [arg-type]
    shape = d["shape"]
    data = np.asarray(d["data"]).reshape(shape)

    return {"mean": ct_mean(data)}


def median() -> dict[str, float]:
    d = request.json or {}  # make it clear that None is prohibited, for mypy's benefit
    shape = d["shape"]
    data = np.asarray(d["data"]).reshape(shape)

    return {"median": ct_median(data)}


app.add_url_rule("/median", view_func=median, methods=["POST"])


if __name__ == "__main__":
    app.run(host="0.0.0.0")  # , debug=True
