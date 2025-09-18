#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

"""Django's command-line utility for administrative tasks."""

import os
import sys

from django.core.management import execute_from_command_line


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.poll.poll.settings")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
