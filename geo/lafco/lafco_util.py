# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import re

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
import pandas as pd
import sqlalchemy as sa

LAFCO_DIR = Path("/Users/jhanley/Desktop/lafco")


_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine  # noqa: PLW0603
    db_file = Path("/tmp/apn.db")
    _engine = _engine or sa.create_engine(f"sqlite:///{db_file}")
    assert isinstance(_engine, Engine)
    return _engine


def get_session() -> Session:
    return Session(get_engine())


def _clean_column_name(name: str) -> str:
    """Converts raw multi-word column name to a clean identifier."""
    xlate = str.maketrans(" ./", "___", "()?")
    name = name.replace("$", "").strip().translate(xlate).lower()
    name = re.sub(r"__+", "_", name)
    assert re.search(r"^[a-z0-9_]+$", name), name
    return name


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={col: _clean_column_name(col) for col in df.columns})


def _with_dashes(apn: str) -> str:
    """Inserts dashes into a 9-digit APN.

    >>> _with_dashes("063492490")
    '063-492-490'
    """
    assert apn.startswith(("063", "113")), apn
    assert 9 == len(apn), apn
    return f"{apn[:3]}-{apn[3:6]}-{apn[6:]}"
