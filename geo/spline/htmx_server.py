#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

persistent_path = Path(
    os.getenv("PERSISTENT_STORAGE_DIR", Path(__file__).parent.resolve())
)

app = Flask(__name__)

db_path = persistent_path / "htmx.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()


db.init_app(app)

if __name__ == "main":
    with app.app_context():
        db.create_all()
    app.run()
