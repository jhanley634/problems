#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
