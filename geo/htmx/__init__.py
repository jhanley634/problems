# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def _get_persistent_path() -> Path:
    p = os.getenv(
        "PERSISTENT_STORAGE_DIR",
        Path(__file__).parent.resolve(),
    )
    return Path(p)


db_path = _get_persistent_path() / "htmx.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)
