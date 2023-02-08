#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from flask import Flask, request

from insta_flask.demo.central_tendency import ct_mean, ct_median

app = Flask(__name__)


@app.route("/hello")
def hello():
    return "Hello!\n"


@app.route("/mean", methods=["POST"])
def mean():
    arg = request.json
    print(arg)
    return f"mean: {ct_mean(arg)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
