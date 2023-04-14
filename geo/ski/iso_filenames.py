#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
import datetime as dt
import shutil

from tqdm import tqdm
import typer

GPX_DIR = Path("~/Desktop/gpx").expanduser()
DOWNLOADS = Path("~/Downloads").expanduser()


def copy_all(src_dir: Path = DOWNLOADS, dst_dir: Path = GPX_DIR) -> None:
    """Copy all GPX files from src_dir to dst_dir, renaming to ISO8601 filenames."""
    src_dir = Path(src_dir).expanduser()
    for path in tqdm(sorted(src_dir.glob("*.gpx"))):
        shutil.copy2(path, dst_dir / iso(path).name)


def iso(path: Path) -> Path:
    prefix = "-".join(path.stem.split("-")[:4])
    suffix = path.name.removeprefix(prefix).replace(" ", "")
    try:
        stamp = dt.datetime.strptime(prefix, "%d-%b-%Y-%H%M").strftime("%Y-%m-%d-%H%M")
    except ValueError:
        stamp = prefix
    return path.with_name(f"{stamp}{suffix}")


__name__ == "__main__" and typer.run(copy_all)  # type: ignore [func-returns-value]
