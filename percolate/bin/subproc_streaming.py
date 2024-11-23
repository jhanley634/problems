#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
from select import PIPE_BUF, select
from subprocess import PIPE, Popen
import datetime as dt
import io
import os

import typer


def streaming_subproc(cmd: list[str]) -> Generator[str]:
    timeout = dt.timedelta(seconds=5)

    with Popen(cmd, stdout=PIPE) as proc:
        assert proc.stdout
        stdout = io.TextIOWrapper(proc.stdout)
        fd = stdout.fileno()
        os.set_blocking(fd, False)
        buf = ""
        temp = "sentinel"
        while proc.poll() is None and temp:
            select([fd], [], [], timeout.total_seconds())
            temp = stdout.read(PIPE_BUF)
            buf += temp

            start, end = 0, 0
            while start > -1:
                end = buf.index("\n", start) + 1
                if end:
                    yield buf[start:end]
                start = end
            buf = buf[start:]

        if buf:
            yield buf

        # Now drain the last few lines from the wrapper, until EOF.
        yield from stdout

        proc.terminate()
        proc.wait()


def parent() -> None:
    repo_top = Path(__file__ + "/../../..").resolve()
    os.chdir(repo_top)

    cmd = "bash percolate/bin/subproc_slow_output.sh 3 1".split()
    for line1 in streaming_subproc(cmd):
        line = line1.rstrip("\n")
        print(f"]] {line} [[")


if __name__ == "__main__":
    typer.run(parent)
