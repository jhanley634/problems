#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2022 John Hanley. MIT licensed.
#
# example usage:
#   vision/preview/preview.py -- --pattern=*.jpg
#
from pathlib import Path

import streamlit as st
import typer

DESKTOP = Path("~/Desktop")
cli = typer.Typer()


@cli.command()
def preview_images(folder: Path = DESKTOP, pattern: str = "*.png") -> None:
    folder = folder.expanduser()
    assert folder.is_dir(), folder
    images = [Path(f).name for f in sorted(folder.glob(pattern))]
    if len(images) < 2:
        images.append("<<<")
    if len(images) < 2:
        images = [">>>"] + images
    assert len(images) >= 2
    st.set_page_config(layout="wide")

    choice = folder / st.select_slider("file", options=images)
    if choice.exists():
        st.image(f"{choice}", use_column_width=True)

    st.markdown("----")
    st.write("- " + "\n- ".join(images))


if __name__ == "__main__":
    cli(standalone_mode=False)
