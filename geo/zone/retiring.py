#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator
import re

import pandas as pd

# from lynx -dump of:
# https://www.nytimes.com/2023/11/26/us/politics/congress-retirements-list.html


def get_retiring(
    in_file: str = "/tmp/congress-retirements-list.txt", verbose: bool = False
) -> Generator[dict[str, str], None, None]:
    """Reports on retiring congress folks."""
    rep_re = re.compile(r"(Representative|Senator) (.+), (Republican|Democrat) of (.+)")
    with open(in_file, encoding="ISO-8859-1") as fin:
        for line in fin:
            m = rep_re.search(line)
            if m:
                type_, name, party, state = m.groups()
                yield {"type": type_, "party": party, "state": state, "name": name}
                if verbose:
                    print(f"{party:11} {type_:15} {state:15} {name}")


if __name__ == "__main__":
    df = pd.DataFrame(get_retiring())
    cols = list(map(str, df.columns))
    print(df.sort_values(cols).to_markdown(index=False))
