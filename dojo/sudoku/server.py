#! /usr/bin/env FLASK_DEBUG=1 python

# Copyright 2023 John Hanley. MIT licensed.

from bs4 import BeautifulSoup
from flask import Flask

from dojo.sudoku.puzzle import Grid

app = Flask(__name__)


def web_page(messy_html: str, title="sudoku") -> str:
    return cleanup(f"<head><title>{title}</head><body>{messy_html}")


def cleanup(messy_html: str, title="sudoku") -> str:
    soup = BeautifulSoup(messy_html, "html.parser")
    return soup.prettify()


@app.route("/hello")
def hello() -> str:
    return web_page("<p>Hello world!")


@app.route("/")
def top() -> str:
    return web_page("hi")


@app.route("/show/<grid>")
def show(grid: str) -> str:
    size = int(len(grid) ** 0.25)
    g = Grid(size=size).from_string(grid)
    return web_page(f"<pre>\n{g}")


@app.route("/edit/<grid>")
def edit(grid: str) -> str:
    form = """
    """
    return form


if __name__ == "__main__":
    example = "http://127.0.0.1:5000/show/12--34----------"
    print(f"Try:\n{example}")

    app.run()
