#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import re


def audit_ip_notices(folder: Path) -> None:
    assert folder.is_dir()
    skip_re = re.compile(r"^($|#! /usr/bin/env)")
    for f in folder.glob("**/*.py"):
        assert f.is_file(), f
        with open(f) as fin:
            line = ""
            while skip_re.search(line):
                line = next(fin)
            assert line.startswith("# Copyright 20"), f
            assert line.endswith(" John Hanley. MIT licensed.\n"), f


if __name__ == "__main__":
    audit_ip_notices(Path("."))
