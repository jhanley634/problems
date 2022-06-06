#! /usr/bin/env python
from pathlib import Path
from select import PIPE_BUF, select
from subprocess import PIPE, Popen
import datetime as dt
import io
import os

import typer


def streaming_subproc(cmd):
    timeout = dt.timedelta(seconds=5)

    with Popen(cmd, stdout=PIPE) as proc:
        stdout = io.TextIOWrapper(proc.stdout)
        fd = stdout.fileno()
        os.set_blocking(fd, False)
        buf = 'sentinel'
        while proc.poll() is None and len(buf) > 0:
            select([fd], [], [], timeout.total_seconds())
            buf = stdout.read(PIPE_BUF)
            if len(buf):
                yield buf
        proc.terminate()
        proc.wait()


def parent():
    repo_top = Path(__file__ + '/../../..').resolve()
    os.chdir(repo_top)

    cmd = 'bash percolate/bin/subproc_slow_output.sh 3 1'.split()
    for line in streaming_subproc(cmd):
        line = line.rstrip('\n')
        print(f']] {line} [[')


if __name__ == '__main__':
    typer.run(parent)
