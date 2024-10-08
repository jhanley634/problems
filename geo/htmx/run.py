#! /usr/bin/env FLASK_DEBUG=1 python
# Copyright 2024 John Hanley. MIT licensed.
# based on https://codecapsules.io/tutorial/building-a-full-stack-application-with-flask-and-htmx
from geo.htmx import app, db, models, views
from geo.htmx.scrape import populate_books_table

assert models
assert views


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_books_table()

    app.run()
