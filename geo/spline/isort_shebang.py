#! /usr/bin/env python
"""
Investigates the circumstances in which isort can move a shebang around.
"""
from pathlib import Path
from random import shuffle
from subprocess import check_call

TEMP = Path("/tmp/isort.d")

IMPORTS = [
    "from collections.abc import Generator",
    "from pathlib import Path",
    "import datetime as dt",
    "import os",
    "import re",
    "import subprocess",
    "from glom import glom",
    "from requests import Response",
    "import click",
    "import requests",
    "",
    "",
    "",
]


def create_and_sort_source_code_files(k: int = 20) -> None:
    TEMP.mkdir(exist_ok=True)
    (TEMP / "out").mkdir(exist_ok=True)
    shebang = "#! /usr/bin/env python\n"
    fn = "\ndef add(a, b): return a + b\n"

    for i in range(k):
        print(i, end="\t")
        perm = IMPORTS.copy()
        shuffle(perm)
        prog = [shebang] + perm + [fn]
        for folder in [TEMP, TEMP / "out"]:
            with open(folder / f"perm-{i:03d}.py", "w") as fout:
                fout.write("\n".join(prog))
    print()

    for _ in range(3):  # We quickly settle upon a fixpoint.
        check_call(["black", f"{TEMP}/out"])
        check_call(["isort", "--float-to-top", f"{TEMP}/out"])


if __name__ == "__main__":
    create_and_sort_source_code_files()
