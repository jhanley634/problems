#! /usr/bin/env FLASK_DEBUG=1 python

# Copyright 2023 John Hanley. MIT licensed.

from bs4 import BeautifulSoup
from flask import Flask

from dojo.sudoku.puzzle import Grid

app = Flask(__name__)


def web_page(messy_html: str, title: str = "sudoku") -> str:
    return cleanup(f"<head><title>{title}</head><body>{messy_html}")


def cleanup(messy_html: str) -> str:
    soup = BeautifulSoup(messy_html, "html.parser")
    return soup.prettify()


# Untyped decorator makes function "hello" untyped
@app.route("/hello")  # type: ignore [misc]
def hello() -> str:
    return web_page("<p>Hello world!")


@app.route("/")  # type: ignore [misc]
def top() -> str:
    return web_page("hi")


@app.route("/show/<grid>")  # type: ignore [misc]
def show(grid: str) -> str:
    size = int(len(grid) ** 0.25)
    g = Grid(size=size).from_string(grid)
    return web_page(f"<pre>\n{g}")


@app.route("/edit/<grid>")  # type: ignore [misc]
def edit(grid: str) -> str:
    return f"""
    {grid}
    """


if __name__ == "__main__":
    example = "http://127.0.0.1:5000/show/12--34----------"
    print(f"Try:\n{example}")

    app.run()
