# Copyright 2024 John Hanley. MIT licensed.
from geo.htmx import db


class Author(db.Model):  # type: ignore [misc]
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    books = db.relationship("Book", backref="author")

    def repr(self) -> str:
        return "<Author: {}>".format(self.books)


class Book(db.Model):  # type: ignore [misc]
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    title = db.Column(db.String)
