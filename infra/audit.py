#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import Path
import re

_skip = {
    "geo/zone/transcript/sync_scripts_spacy_test.py",
    "infra/audit.py",
    "infra/verify_imports.py",
}


def audit_ip_notices(folder: Path) -> None:
    assert folder.is_dir()
    is_test_re = re.compile(r"_test\d?\.py$")
    skip_re = re.compile(r"^($|#! /usr/bin/env)")
    for f in folder.glob("**/*.py"):
        assert f.is_file(), f
        with open(f) as fin:
            line = ""
            while skip_re.search(line):
                line = next(fin)
            assert line.startswith("# Copyright 20"), f
            assert line.endswith(" John Hanley. MIT licensed.\n"), f

            if f"{f}" in _skip:
                continue
            if is_test_re.search(f.name):
                has_test = "import unittest" in f.read_text()
                assert has_test, f
            # if has_test != is_test_re.search(f.name):
            #     print(f)


if __name__ == "__main__":
    audit_ip_notices(Path("."))
