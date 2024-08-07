# Copyright 2024 John Hanley. MIT licensed.
# based on https://github.com/codecapsules-io/codecapsules-docs/blob/main/docs/tutorials/build-flask-htmx-app.md
from collections import deque
from collections.abc import Generator
from time import sleep
import datetime as dt

from flask import Response, render_template, request

from geo.htmx import app, db
from geo.htmx.models import Author, Book


@app.route("/", methods=["GET"])  # type: ignore [misc]
def home() -> str:
    books = (
        db.session.query(Book, Author).filter(Book.author_id == Author.author_id).all()
    )
    return render_template("index.html", books=books)


@app.route("/submit", methods=["POST"])  # type: ignore [misc]
def submit() -> str:
    global_book_object = Book()

    title = request.form["title"]
    author_name = request.form["author"]

    author_exists = db.session.query(Author).filter(Author.name == author_name).first()
    print(author_exists)
    # check if author already exists in db
    if author_exists:
        author_id = author_exists.author_id
        book = Book(author_id=author_id, title=title)
        db.session.add(book)
        db.session.commit()
        global_book_object = book
    else:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        book = Book(author_id=author.author_id, title=title)
        db.session.add(book)
        db.session.commit()
        global_book_object = book

    response = f"""
    <tr>
        <td>{title}</td>
        <td>{author_name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_book_object.book_id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_book_object.book_id}"
                class="btn btn-primary">Delete</button>
        </td>
    </tr>
    """
    return response


@app.route("/delete/<int:id>", methods=["DELETE"])  # type: ignore [misc]
def delete_book(id: str) -> str:
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return ""


@app.route("/get-edit-form/<int:id>", methods=["GET"])  # type: ignore [misc]
def get_edit_form(id: str) -> str:
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-book-row/{id}">
  <td><input name="title" value="{book.title}"/></td>
  <td>{author.name}</td>
  <td>
    <button class="btn btn-primary" hx-get="/get-book-row/{id}">
      Cancel
    </button>
    <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
      Save
    </button>
  </td>
    </tr>
    """
    return response


@app.route("/get-book-row/<int:id>", methods=["GET"])  # type: ignore [misc]
def get_book_row(id: str) -> str:
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f"""
    <tr>
        <td>{book.title}</td>
        <td>{author.name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">Delete</button>
        </td>
    </tr>
    """
    return response


@app.route("/update/<int:id>", methods=["PUT"])  # type: ignore [misc]
def update_book(id: str) -> str:
    db.session.query(Book).filter(Book.book_id == id).update(
        {"title": request.form["title"]}
    )
    db.session.commit()

    title = request.form["title"]
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f"""
    <tr>
        <td>{title}</td>
        <td>{author.name}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">Delete</button>
        </td>
    </tr>
    """
    return response


@app.route("/sse", methods=["GET"])  # type: ignore [misc]
def sse() -> Response:
    def event_stream() -> Generator[str, None, None]:
        while messages:
            msg = messages.popleft()
            counter = repr({"time": dt.datetime.now().isoformat(), "counter": msg})
            yield f"event: count\ndata: {counter}\n\n"
            sleep(2)

    messages = deque(["one", "two", "three", "four", "five"])
    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/sse-jq", methods=["GET"])  # type: ignore [misc]
def sse_jq() -> str:
    return render_template("sse.html")
