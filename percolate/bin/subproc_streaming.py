#! /usr/bin/env python
from pathlib import Path
from select import PIPE_BUF, select
from subprocess import PIPE, Popen, check_output, run
import datetime as dt
import os

import typer


def parent():
    repo_top = Path(__file__ + '/../../..').resolve()
    os.chdir(repo_top)
    timeout = dt.timedelta(seconds=5)
    i = 0

    cmd = 'bash percolate/bin/subproc_slow_output.sh 3 1'.split()
    with Popen(cmd, stdout=PIPE, encoding='utf8') as proc:
        fd = proc.stdout.fileno()
        os.set_blocking(fd, False)
        while proc.poll() is None:
            select([fd], [], [], timeout.total_seconds())
            buf = proc.stdout.read(PIPE_BUF)
            print(f'{i}  {buf} {len(buf)}')
            i += 1


if __name__ == '__main__':
    typer.run(parent)
