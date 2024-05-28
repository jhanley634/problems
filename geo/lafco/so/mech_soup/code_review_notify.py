#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Pops up a TK window when there are recent CR changes.
"""
from pathlib import Path
from random import randrange
from time import sleep
from tkinter import ttk
import datetime as dt
import re
import tkinter as tk

from tabulate import tabulate
import pandas as pd

from geo.lafco.so.mech_soup.code_review import scrape

ans_mod_re = re.compile(
    r"^(answered|asked|modified) (\d+) (sec|min|hour|day|week|month)s? ago$"
)


def _get_multiplier(unit: str) -> int:
    if unit == "day":
        return 60 * 24
    if unit == "hour":
        return 60
    if unit == "sec":
        return 1
    return 1


log = Path("/tmp/code-review.log")


def _get_previous_elapsed_minutes(default: int = 999) -> int:
    try:
        with open(log) as fin:
            last_line = fin.readlines()[-1]
            return int(last_line.split()[2])
    except FileNotFoundError:
        pass
    return default


ymd_hms_fmt = "%Y-%m-%d %H:%M:%S"


def _is_new(modified: str) -> bool:
    m = ans_mod_re.match(modified)
    assert m, modified
    elapsed_minutes = int(m.group(2)) * _get_multiplier(m.group(3))
    prev = _get_previous_elapsed_minutes()

    with open(log, "a") as fout:
        now = dt.datetime.now().strftime(ymd_hms_fmt)
        print(f"{now}   {elapsed_minutes} minutes ago", file=fout)

    return elapsed_minutes < prev


def notify(delay: int = 60, jitter: int = 30) -> None:
    while True:
        now = dt.datetime.now().strftime(ymd_hms_fmt)
        print("\r", end=f"{now}  ", flush=True)
        sleep(delay + randrange(0, jitter))
        sleep(1)
        df = pd.DataFrame(scrape())
        if _is_new(df[:1].modified[0]):
            txt = tabulate(df.to_records(index=False), maxcolwidths=98)
            popup_display(txt)


def popup_display(txt: str) -> None:
    root = tk.Tk()
    root.title("Code Review recent updates")
    courier = ttk.Style()
    courier.configure("Courier.TLabel", font=("Courier", 12))

    ttk.Label(root, text=txt, style="Courier.TLabel").pack()

    tk.Button(root, text="OK", command=root.destroy).pack()
    root.mainloop()


if __name__ == "__main__":
    notify()
