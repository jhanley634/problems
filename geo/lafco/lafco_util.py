# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import re

import pandas as pd

LAFCO_DIR = Path("/Users/jhanley/Desktop/lafco")


def _clean_column_name(name: str) -> str:
    """Converts raw multi-word column name to a clean identifier."""
    xlate = str.maketrans(" .", "__")
    name = name.replace("$", "").strip().translate(xlate).lower()
    assert re.search(r"^[a-z0-9_]+$", name), name
    return name


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={col: _clean_column_name(col) for col in df.columns})
